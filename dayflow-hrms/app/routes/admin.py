from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from flask_login import login_required, current_user
from app.models import (db, User, Employee, Attendance, LeaveRequest, Payroll, 
                        SalaryComponent, TimeOffType, LeaveAllocation,
                        create_salary_components_for_employee, allocate_leave_for_employee,
                        initialize_timeoff_types)
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_, and_
from decimal import Decimal
from werkzeug.utils import secure_filename
import calendar
import os

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('main.employee_dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/profile')
@login_required
@admin_required
def admin_profile():
    employee = current_user.employee_profile
    return render_template('admin/profile.html', employee=employee)

@admin_bp.route('/employees')
@login_required
@admin_required
def employees():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    department = request.args.get('department', '')
    
    query = Employee.query.join(User)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Employee.first_name.contains(search),
                Employee.last_name.contains(search),
                User.employee_id.contains(search),
                User.email.contains(search)
            )
        )
    
    if department:
        query = query.filter(Employee.department == department)
    
    employees = query.order_by(Employee.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get all departments for filter
    departments = db.session.query(Employee.department).distinct().all()
    departments = [dept[0] for dept in departments if dept[0]]
    
    return render_template('admin/employees.html', 
                         employees=employees, 
                         departments=departments,
                         search=search,
                         current_department=department)

@admin_bp.route('/employee/<int:employee_id>')
@login_required
@admin_required
def employee_detail(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    # Get recent attendance
    recent_attendance = Attendance.query.filter_by(
        employee_id=employee_id
    ).order_by(Attendance.date.desc()).limit(10).all()
    
    # Get leave requests
    leave_requests = LeaveRequest.query.filter_by(
        employee_id=employee_id
    ).order_by(LeaveRequest.created_at.desc()).limit(5).all()
    
    # Get payroll records
    payroll_records = Payroll.query.filter_by(
        employee_id=employee_id
    ).order_by(Payroll.created_at.desc()).limit(3).all()
    
    return render_template('admin/employee_detail.html',
                         employee=employee,
                         recent_attendance=recent_attendance,
                         leave_requests=leave_requests,
                         payroll_records=payroll_records)

@admin_bp.route('/employee/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_employee():
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            personal_email = request.form.get('personal_email')
            phone = request.form.get('phone')
            department = request.form.get('department')
            position = request.form.get('position')
            monthly_wage = request.form.get('monthly_wage')
            
            # Optional fields
            date_of_birth = request.form.get('date_of_birth')
            hire_date = request.form.get('hire_date', date.today().strftime('%Y-%m-%d'))
            gender = request.form.get('gender')
            marital_status = request.form.get('marital_status')
            nationality = request.form.get('nationality', 'Indian')
            address = request.form.get('address')
            
            # Validate required fields
            if not all([first_name, last_name, email, monthly_wage]):
                flash('First name, last name, email, and monthly wage are required!', 'error')
                return render_template('admin/add_employee.html')
            
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered!', 'error')
                return render_template('admin/add_employee.html')
            
            # Auto-generate employee ID
            hire_year = datetime.strptime(hire_date, '%Y-%m-%d').year
            company_code = "OI"  # Odoo India - You can make this configurable
            employee_id = User.generate_employee_id(company_code, first_name, last_name, hire_year)
            
            # Auto-generate password
            auto_password = User.generate_random_password()
            
            # Create user
            user = User(
                employee_id=employee_id,
                email=email,
                role='employee',
                is_verified=True,
                password_changed=False
            )
            user.set_password(auto_password)
            
            db.session.add(user)
            db.session.flush()
            
            # Create employee profile
            employee = Employee(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                personal_email=personal_email,
                department=department,
                position=position,
                monthly_wage=Decimal(monthly_wage),
                salary=Decimal(monthly_wage),  # For backward compatibility
                address=address,
                gender=gender,
                marital_status=marital_status,
                nationality=nationality,
                hire_date=datetime.strptime(hire_date, '%Y-%m-%d').date()
            )
            
            if date_of_birth:
                employee.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
            
            db.session.add(employee)
            db.session.flush()
            
            # Create salary components
            create_salary_components_for_employee(employee.id, Decimal(monthly_wage))
            
            # Allocate leaves
            allocate_leave_for_employee(employee.id)
            
            db.session.commit()
            
            flash(f'Employee created successfully! Employee ID: {employee_id}, Temporary Password: {auto_password}', 'success')
            flash('Please share these credentials with the employee. They must change the password on first login.', 'info')
            return redirect(url_for('admin.employee_detail', employee_id=employee.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating employee: {str(e)}', 'error')
    
    return render_template('admin/add_employee.html')

@admin_bp.route('/employee/<int:employee_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    
    if request.method == 'POST':
        try:
            # Update employee details
            employee.first_name = request.form.get('first_name')
            employee.last_name = request.form.get('last_name')
            employee.phone = request.form.get('phone')
            employee.address = request.form.get('address')
            employee.department = request.form.get('department')
            employee.position = request.form.get('position')
            
            # Update date of birth
            dob = request.form.get('date_of_birth')
            if dob:
                employee.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
            
            # Update hire date
            hire_date = request.form.get('hire_date')
            if hire_date:
                employee.hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
            
            # Update working days per week
            working_days = request.form.get('working_days_per_week')
            if working_days:
                employee.working_days_per_week = int(working_days)
            
            # Update monthly wage and salary components
            monthly_wage = request.form.get('monthly_wage')
            if monthly_wage:
                employee.monthly_wage = Decimal(monthly_wage)
                employee.salary = Decimal(monthly_wage)  # Keep for backward compatibility
                
                # Delete existing salary components for this employee
                SalaryComponent.query.filter_by(employee_id=employee_id).delete()
                
                # Calculate and save salary components
                monthly_wage_float = float(monthly_wage)
                
                # 1. Basic Salary (50% of wage)
                basic_salary = round(monthly_wage_float * 0.50, 2)
                basic_component = SalaryComponent(
                    employee_id=employee_id,
                    component_name='Basic Salary',
                    component_type='earning',
                    computation_type='percentage',
                    value=50,
                    base_component='wage',
                    calculated_amount=basic_salary,
                    is_active=True
                )
                db.session.add(basic_component)
                
                # 2. HRA (50% of basic)
                hra = round(basic_salary * 0.50, 2)
                hra_component = SalaryComponent(
                    employee_id=employee_id,
                    component_name='House Rent Allowance',
                    component_type='earning',
                    computation_type='percentage',
                    value=50,
                    base_component='basic',
                    calculated_amount=hra,
                    is_active=True
                )
                db.session.add(hra_component)
                
                # 3. Standard Allowance (fixed)
                standard_allowance = Decimal(request.form.get('standard_allowance', '4167'))
                standard_component = SalaryComponent(
                    employee_id=employee_id,
                    component_name='Standard Allowance',
                    component_type='earning',
                    computation_type='fixed',
                    value=standard_allowance,
                    calculated_amount=standard_allowance,
                    is_active=True
                )
                db.session.add(standard_component)
                
                # 4. Performance Bonus (8.33% of wage)
                performance_bonus = round(monthly_wage_float * 0.0833, 2)
                perf_component = SalaryComponent(
                    employee_id=employee_id,
                    component_name='Performance Bonus',
                    component_type='earning',
                    computation_type='percentage',
                    value=8.33,
                    base_component='wage',
                    calculated_amount=performance_bonus,
                    is_active=True
                )
                db.session.add(perf_component)
                
                # 5. LTA (8.333% of wage)
                lta = round(monthly_wage_float * 0.08333, 2)
                lta_component = SalaryComponent(
                    employee_id=employee_id,
                    component_name='Leave Travel Allowance',
                    component_type='earning',
                    computation_type='percentage',
                    value=8.333,
                    base_component='wage',
                    calculated_amount=lta,
                    is_active=True
                )
                db.session.add(lta_component)
                
                # 6. Fixed Allowance (remaining amount)
                fixed_allowance = monthly_wage_float - (basic_salary + hra + float(standard_allowance) + performance_bonus + lta)
                if fixed_allowance > 0:
                    fixed_component = SalaryComponent(
                        employee_id=employee_id,
                        component_name='Fixed Allowance',
                        component_type='earning',
                        computation_type='fixed',
                        value=round(fixed_allowance, 2),
                        calculated_amount=round(fixed_allowance, 2),
                        is_active=True
                    )
                    db.session.add(fixed_component)
                
                # Deductions
                # 7. Provident Fund (% of basic)
                pf_rate = Decimal(request.form.get('pf_rate', '12'))
                pf_amount = round(basic_salary * (float(pf_rate) / 100), 2)
                pf_component = SalaryComponent(
                    employee_id=employee_id,
                    component_name='Provident Fund',
                    component_type='deduction',
                    computation_type='percentage',
                    value=pf_rate,
                    base_component='basic',
                    calculated_amount=pf_amount,
                    is_active=True
                )
                db.session.add(pf_component)
                
                # 8. Professional Tax (fixed)
                professional_tax = Decimal(request.form.get('professional_tax', '200'))
                pt_component = SalaryComponent(
                    employee_id=employee_id,
                    component_name='Professional Tax',
                    component_type='deduction',
                    computation_type='fixed',
                    value=professional_tax,
                    calculated_amount=professional_tax,
                    is_active=True
                )
                db.session.add(pt_component)
            
            employee.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Employee and salary information updated successfully!', 'success')
            return redirect(url_for('admin.employee_detail', employee_id=employee_id))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Invalid input data: {str(e)}', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating employee: {str(e)}', 'error')
    
    # GET request - load existing salary components if any
    salary_components = SalaryComponent.query.filter_by(employee_id=employee_id, is_active=True).all()
    
    return render_template('admin/edit_employee.html', 
                         employee=employee,
                         salary_components=salary_components)

@admin_bp.route('/employee/<int:employee_id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_employee_status(employee_id):
    """Toggle employee active/inactive status"""
    employee = Employee.query.get_or_404(employee_id)
    user = employee.user
    
    if not user:
        flash('No user account associated with this employee!', 'error')
        return redirect(url_for('admin.employee_detail', employee_id=employee_id))
    
    # Prevent admin from deactivating themselves
    if user.id == current_user.id:
        flash('You cannot deactivate your own account!', 'error')
        return redirect(url_for('admin.employee_detail', employee_id=employee_id))
    
    try:
        # Toggle the is_active status
        user.is_active = not user.is_active
        db.session.commit()
        
        status = 'activated' if user.is_active else 'deactivated'
        flash(f'User account {status} successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user status: {str(e)}', 'error')
    
    return redirect(url_for('admin.employee_detail', employee_id=employee_id))

@admin_bp.route('/employee/<int:employee_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_employee(employee_id):
    """Delete employee and associated user account"""
    employee = Employee.query.get_or_404(employee_id)
    user = employee.user
    
    if not user:
        flash('No user account associated with this employee!', 'error')
        return redirect(url_for('admin.employees'))
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'error')
        return redirect(url_for('admin.employee_detail', employee_id=employee_id))
    
    try:
        employee_name = employee.full_name
        employee_id_str = user.employee_id
        
        # Delete user (will cascade delete employee due to relationship)
        db.session.delete(user)
        db.session.commit()
        
        flash(f'Employee {employee_name} (ID: {employee_id_str}) deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting employee: {str(e)}', 'error')
        return redirect(url_for('admin.employee_detail', employee_id=employee_id))
    
    return redirect(url_for('admin.employees'))

@admin_bp.route('/attendance')
@login_required
@admin_required
def attendance():
    date_str = request.args.get('date', date.today().strftime('%Y-%m-%d'))
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        selected_date = date.today()
    
    # Get all employees with their attendance for the selected date
    employees = db.session.query(Employee, Attendance).outerjoin(
        Attendance,
        (Employee.id == Attendance.employee_id) & (Attendance.date == selected_date)
    ).all()
    
    # Calculate statistics
    total_employees = Employee.query.count()
    present_count = Attendance.query.filter_by(date=selected_date, status='present').count()
    absent_count = Attendance.query.filter_by(date=selected_date, status='absent').count()
    leave_count = Attendance.query.filter_by(date=selected_date, status='leave').count()
    half_day_count = Attendance.query.filter_by(date=selected_date, status='half_day').count()
    
    stats = {
        'total': total_employees,
        'present': present_count,
        'absent': absent_count,
        'leave': leave_count,
        'half_day': half_day_count,
        'not_marked': total_employees - (present_count + absent_count + leave_count + half_day_count)
    }
    
    return render_template('admin/attendance.html',
                         employees=employees,
                         selected_date=selected_date,
                         stats=stats)

@admin_bp.route('/update_attendance', methods=['POST'])
@login_required
@admin_required
def update_attendance():
    try:
        employee_id = request.form.get('employee_id')
        attendance_date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        status = request.form.get('status')
        remarks = request.form.get('remarks', '')
        
        # Find or create attendance record
        attendance = Attendance.query.filter_by(
            employee_id=employee_id,
            date=attendance_date
        ).first()
        
        if attendance:
            attendance.status = status
            attendance.remarks = remarks
            attendance.updated_at = datetime.utcnow()
        else:
            attendance = Attendance(
                employee_id=employee_id,
                date=attendance_date,
                status=status,
                remarks=remarks
            )
            db.session.add(attendance)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error updating attendance'})

@admin_bp.route('/leave_requests')
@login_required
@admin_required
def leave_requests():
    status_filter = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    
    query = LeaveRequest.query
    
    if status_filter != 'all':
        query = query.filter(LeaveRequest.status == status_filter)
    
    leave_requests = query.order_by(LeaveRequest.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get all employees for filter
    employees = Employee.query.all()
    
    # Get counts for statistics
    pending_count = LeaveRequest.query.filter_by(status='pending').count()
    approved_count = LeaveRequest.query.filter_by(status='approved').count()
    rejected_count = LeaveRequest.query.filter_by(status='rejected').count()
    
    return render_template('admin/leave_requests.html',
                         leave_requests=leave_requests,
                         current_status=status_filter,
                         employees=employees,
                         pending_count=pending_count,
                         approved_count=approved_count,
                         rejected_count=rejected_count)

@admin_bp.route('/leave_request/<int:request_id>')
@login_required
@admin_required
def get_leave_request(request_id):
    leave_request = LeaveRequest.query.get_or_404(request_id)
    
    # Get certificate filename if exists
    certificate_filename = None
    if leave_request.certificate_path:
        certificate_filename = os.path.basename(leave_request.certificate_path)
    
    return jsonify({
        'id': leave_request.id,
        'employee_name': leave_request.employee.full_name,
        'employee_id': leave_request.employee.user.employee_id,
        'department': leave_request.employee.department,
        'leave_type': leave_request.leave_type,
        'start_date': leave_request.start_date.strftime('%Y-%m-%d'),
        'end_date': leave_request.end_date.strftime('%Y-%m-%d'),
        'days_requested': leave_request.days_requested,
        'reason': leave_request.reason,
        'status': leave_request.status,
        'admin_comment': leave_request.admin_comment,
        'certificate_path': leave_request.certificate_path,
        'certificate_filename': certificate_filename
    })

@admin_bp.route('/update_leave_status', methods=['POST'])
@login_required
@admin_required
def update_leave_status():
    try:
        data = request.get_json()
        request_id = data.get('request_id')
        new_status = data.get('status')
        
        leave_request = LeaveRequest.query.get_or_404(request_id)
        leave_request.status = new_status
        leave_request.approved_by = current_user.id
        leave_request.updated_at = datetime.utcnow()
        
        # If approved, mark attendance as leave
        if new_status == 'approved':
            current_date = leave_request.start_date
            while current_date <= leave_request.end_date:
                attendance = Attendance.query.filter_by(
                    employee_id=leave_request.employee_id,
                    date=current_date
                ).first()
                
                if attendance:
                    attendance.status = 'leave'
                    attendance.remarks = f"Approved leave: {leave_request.leave_type}"
                else:
                    attendance = Attendance(
                        employee_id=leave_request.employee_id,
                        date=current_date,
                        status='leave',
                        remarks=f"Approved leave: {leave_request.leave_type}"
                    )
                    db.session.add(attendance)
                
                current_date += timedelta(days=1)
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'Leave request {new_status} successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/leave_request/<int:request_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_leave_request(request_id):
    try:
        leave_request = LeaveRequest.query.get_or_404(request_id)
        admin_comment = request.form.get('admin_comment', '')
        
        leave_request.status = 'approved'
        leave_request.admin_comment = admin_comment
        leave_request.approved_by = current_user.id
        leave_request.updated_at = datetime.utcnow()
        
        # Mark attendance as leave for the requested dates
        current_date = leave_request.start_date
        while current_date <= leave_request.end_date:
            attendance = Attendance.query.filter_by(
                employee_id=leave_request.employee_id,
                date=current_date
            ).first()
            
            if attendance:
                attendance.status = 'leave'
                attendance.remarks = f"Approved leave: {leave_request.leave_type}"
            else:
                attendance = Attendance(
                    employee_id=leave_request.employee_id,
                    date=current_date,
                    status='leave',
                    remarks=f"Approved leave: {leave_request.leave_type}"
                )
                db.session.add(attendance)
            
            current_date += timedelta(days=1)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Leave request approved successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error approving leave request'})

@admin_bp.route('/leave_request/<int:request_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_leave_request(request_id):
    try:
        leave_request = LeaveRequest.query.get_or_404(request_id)
        admin_comment = request.form.get('admin_comment', '')
        
        leave_request.status = 'rejected'
        leave_request.admin_comment = admin_comment
        leave_request.approved_by = current_user.id
        leave_request.updated_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Leave request rejected'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error rejecting leave request'})

@admin_bp.route('/payroll')
@login_required
@admin_required
def payroll():
    page = request.args.get('page', 1, type=int)
    employee_id = request.args.get('employee_id', type=int)
    pay_period = request.args.get('pay_period')
    year = request.args.get('year', type=int)
    
    query = Payroll.query
    
    if employee_id:
        query = query.filter(Payroll.employee_id == employee_id)
    
    if pay_period:
        # pay_period format is 'YYYY-MM', filter by matching year and month
        year_month = pay_period.split('-')
        if len(year_month) == 2:
            year_val, month_val = int(year_month[0]), int(year_month[1])
            query = query.filter(
                db.extract('year', Payroll.pay_period_start) == year_val,
                db.extract('month', Payroll.pay_period_start) == month_val
            )
    elif year:
        query = query.filter(db.extract('year', Payroll.pay_period_start) == year)
    
    payroll_records = query.order_by(Payroll.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Calculate statistics
    all_payrolls = Payroll.query.all()
    total_payroll = sum(float(p.net_pay or 0) for p in all_payrolls)
    employees_paid = len(set(p.employee_id for p in all_payrolls if p.payment_status and p.payment_status.lower() == 'paid'))
    pending_payments = len([p for p in all_payrolls if p.payment_status and p.payment_status.lower() == 'pending'])
    average_salary = total_payroll / len(all_payrolls) if all_payrolls else 0
    
    # Get all employees for filter
    employees = Employee.query.all()
    
    # Get unique pay periods and years
    pay_periods = db.session.query(
        db.func.strftime('%Y-%m', Payroll.pay_period_start).label('period')
    ).distinct().order_by('period').all()
    pay_periods = [p[0] for p in pay_periods]
    
    years = db.session.query(
        db.func.strftime('%Y', Payroll.pay_period_start).label('year')
    ).distinct().order_by('year').all()
    years = [int(y[0]) for y in years]
    
    return render_template('admin/payroll.html',
                         payroll_records=payroll_records,
                         employees=employees,
                         selected_employee=employee_id,
                         selected_pay_period=pay_period,
                         selected_year=year,
                         pay_periods=pay_periods,
                         years=years,
                         total_payroll=total_payroll,
                         employees_paid=employees_paid,
                         pending_payments=pending_payments,
                         average_salary=average_salary)

@admin_bp.route('/payroll/generate', methods=['POST'])
@login_required
@admin_required
def generate_payroll():
    """Generate payroll - alias for create_payroll"""
    return create_payroll()

@admin_bp.route('/payroll/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_payroll():
    if request.method == 'POST':
        try:
            employee_id = request.form.get('employee_id')
            
            # Validate employee selection
            if not employee_id:
                flash('Please select an employee', 'error')
                employees = Employee.query.all()
                current_year = datetime.now().year
                return render_template('admin/create_payroll.html', employees=employees, current_year=current_year)
            
            # Get month and year from form
            month = int(request.form.get('month'))
            year = int(request.form.get('year'))
            
            # Calculate pay period start and end dates
            pay_period_start = datetime(year, month, 1).date()
            # Get last day of the month
            if month == 12:
                pay_period_end = datetime(year, 12, 31).date()
            else:
                pay_period_end = (datetime(year, month + 1, 1) - timedelta(days=1)).date()
            
            employee = Employee.query.get_or_404(employee_id)
            
            # Get base salary from form or calculate from employee data
            base_salary_form = request.form.get('base_monthly_salary', '').strip()
            if base_salary_form and float(base_salary_form) > 0:
                base_salary = float(base_salary_form)
            elif employee.monthly_wage and float(employee.monthly_wage) > 0:
                base_salary = float(employee.monthly_wage)
            else:
                flash('Please enter a base monthly salary or configure the employee salary first.', 'error')
                employees = Employee.query.all()
                current_year = datetime.now().year
                return render_template('admin/create_payroll.html', employees=employees, current_year=current_year)
            
            # Get form data with defaults - handle empty strings properly
            basic_salary_val = request.form.get('basic_salary', '').strip()
            basic_salary = Decimal(basic_salary_val if basic_salary_val else str(base_salary * 0.5))
            
            hra_val = request.form.get('hra', '').strip()
            hra = Decimal(hra_val if hra_val else str(float(basic_salary) * 0.5))
            
            standard_allowance = Decimal(request.form.get('standard_allowance', '0').strip() or '0')
            performance_bonus = Decimal(request.form.get('performance_bonus', '0').strip() or '0')
            
            # New fields for increments and bonuses
            increment_amount = Decimal(request.form.get('increment_amount', '0').strip() or '0')
            increment_percentage = Decimal(request.form.get('increment_percentage', '0').strip() or '0')
            special_bonus = Decimal(request.form.get('special_bonus', '0').strip() or '0')
            festival_bonus = Decimal(request.form.get('festival_bonus', '0').strip() or '0')
            other_earnings = Decimal(request.form.get('other_earnings', '0').strip() or '0')
            
            # Deductions
            pf_deduction = Decimal(request.form.get('pf_deduction', '').strip() or str(float(basic_salary) * 0.12))
            professional_tax = Decimal(request.form.get('professional_tax', '200').strip() or '200')
            deductions = Decimal(request.form.get('deductions', '0').strip() or '0')
            tax_deductions = Decimal(request.form.get('tax_deductions', '0').strip() or '0')
            
            # Attendance data - the form sends 'working_days' which is total_working_days
            working_days_from_form = int(request.form.get('working_days', '26').strip() or '26')
            total_working_days = working_days_from_form
            days_present = int(request.form.get('days_present', '').strip() or str(working_days_from_form))
            
            # Calculate unpaid leave days from leave requests
            unpaid_leave_days = 0
            paid_leave_days = 0
            
            # Count unpaid and paid leaves in the pay period
            leave_requests = LeaveRequest.query.filter(
                LeaveRequest.employee_id == employee_id,
                LeaveRequest.status == 'approved',
                or_(
                    and_(LeaveRequest.start_date >= pay_period_start, LeaveRequest.start_date <= pay_period_end),
                    and_(LeaveRequest.end_date >= pay_period_start, LeaveRequest.end_date <= pay_period_end),
                    and_(LeaveRequest.start_date <= pay_period_start, LeaveRequest.end_date >= pay_period_end)
                )
            ).all()
            
            for leave_req in leave_requests:
                # Calculate overlapping days
                overlap_start = max(leave_req.start_date, pay_period_start)
                overlap_end = min(leave_req.end_date, pay_period_end)
                overlap_days = (overlap_end - overlap_start).days + 1
                
                if leave_req.leave_type == 'unpaid':
                    unpaid_leave_days += overlap_days
                else:
                    paid_leave_days += overlap_days
            
            overtime_hours_val = request.form.get('overtime_hours', '0').strip()
            overtime_hours = float(overtime_hours_val if overtime_hours_val else '0')
            
            overtime_rate_val = request.form.get('overtime_rate', '0').strip()
            overtime_rate = Decimal(overtime_rate_val if overtime_rate_val else '0')
            
            payroll = Payroll(
                employee_id=employee_id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end,
                base_monthly_salary=Decimal(base_salary),
                basic_salary=basic_salary,
                hra=hra,
                standard_allowance=standard_allowance,
                performance_bonus=performance_bonus,
                increment_amount=increment_amount,
                increment_percentage=increment_percentage,
                special_bonus=special_bonus,
                festival_bonus=festival_bonus,
                other_earnings=other_earnings,
                pf_deduction=pf_deduction,
                professional_tax=professional_tax,
                deductions=deductions,
                tax_deductions=tax_deductions,
                days_present=days_present,
                total_working_days=total_working_days,
                unpaid_leave_days=unpaid_leave_days,
                paid_leave_days=paid_leave_days,
                overtime_hours=overtime_hours,
                overtime_rate=overtime_rate
            )
            
            # Calculate all pay components
            payroll.calculate_net_pay()
            
            db.session.add(payroll)
            db.session.commit()
            
            flash('Payroll record created successfully!', 'success')
            return redirect(url_for('admin.payroll'))
            
        except ValueError as e:
            flash(f'Invalid input data: {str(e)}', 'error')
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating payroll record: {str(e)}', 'error')
    
    employees = Employee.query.all()
    current_year = datetime.now().year
    return render_template('admin/create_payroll.html', employees=employees, current_year=current_year)

@admin_bp.route('/payroll/<int:payroll_id>')
@login_required
@admin_required
def get_payroll(payroll_id):
    try:
        payroll = Payroll.query.get_or_404(payroll_id)
        return jsonify({
            'id': payroll.id,
            'employee_name': payroll.employee.full_name,
            'employee_id': payroll.employee.user.employee_id,
            'department': payroll.employee.department,
            'position': payroll.employee.position,
            'pay_period': f"{payroll.pay_period_start.strftime('%Y-%m-%d')} to {payroll.pay_period_end.strftime('%Y-%m-%d')}",
            
            # Earnings breakdown
            'base_monthly_salary': float(payroll.base_monthly_salary) if payroll.base_monthly_salary else 0,
            'basic_salary': float(payroll.basic_salary),
            'hra': float(payroll.hra),
            'standard_allowance': float(payroll.standard_allowance),
            'performance_bonus': float(payroll.performance_bonus),
            'lta': float(payroll.lta),
            'fixed_allowance': float(payroll.fixed_allowance),
            'allowances': float(payroll.allowances),
            
            # Increments and Bonuses
            'increment_amount': float(payroll.increment_amount),
            'increment_percentage': float(payroll.increment_percentage),
            'special_bonus': float(payroll.special_bonus),
            'festival_bonus': float(payroll.festival_bonus),
            'other_earnings': float(payroll.other_earnings),
            
            # Overtime
            'overtime_hours': float(payroll.overtime_hours),
            'overtime_rate': float(payroll.overtime_rate),
            'overtime_pay': float(payroll.overtime_hours * payroll.overtime_rate),
            
            # Attendance
            'days_present': payroll.days_present,
            'total_working_days': payroll.total_working_days,
            'unpaid_leave_days': payroll.unpaid_leave_days,
            'paid_leave_days': payroll.paid_leave_days,
            
            # Deductions breakdown
            'pf_deduction': float(payroll.pf_deduction),
            'professional_tax': float(payroll.professional_tax),
            'deductions': float(payroll.deductions),
            'tax_deductions': float(payroll.tax_deductions),
            'unpaid_leave_deduction': float(payroll.unpaid_leave_deduction),
            
            # Totals
            'gross_pay': float(payroll.gross_pay) if payroll.gross_pay else 0,
            'total_deductions': float(payroll.total_deductions) if payroll.total_deductions else 0,
            'net_pay': float(payroll.net_pay) if payroll.net_pay else 0,
            
            'payment_status': payroll.payment_status if payroll.payment_status else 'pending',
            'created_at': payroll.created_at.strftime('%Y-%m-%d')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/payroll/mark_paid', methods=['POST'])
@login_required
@admin_required
def mark_payroll_paid():
    try:
        data = request.get_json()
        payroll_id = data.get('payroll_id')
        
        payroll = Payroll.query.get_or_404(payroll_id)
        # You can add a payment_status field to the model later
        # For now, just return success
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Payroll marked as paid'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/payroll/payslip/<int:payroll_id>')
@login_required
@admin_required
def generate_payslip(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    # This would generate a PDF payslip - for now just return HTML
    return render_template('admin/payslip.html', payroll=payroll)

@admin_bp.route('/download_medical_certificate/<int:leave_request_id>')
@login_required
@admin_required
def download_medical_certificate(leave_request_id):
    """Download medical certificate for a leave request"""
    try:
        leave_request = LeaveRequest.query.get_or_404(leave_request_id)
        
        if not leave_request.certificate_path:
            flash('No medical certificate found for this leave request', 'error')
            return redirect(url_for('admin.leave_requests'))
        
        # Get the file path - handle both relative and absolute paths
        file_path = leave_request.certificate_path
        
        # If it's a relative path, make it absolute
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            flash(f'Medical certificate file not found at: {file_path}', 'error')
            return redirect(url_for('admin.leave_requests'))
        
        # Get directory and filename
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        
        return send_from_directory(directory, filename, as_attachment=True)
        
    except Exception as e:
        flash(f'Error downloading medical certificate: {str(e)}', 'error')
        return redirect(url_for('admin.leave_requests'))