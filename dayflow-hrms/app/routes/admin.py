from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import (db, User, Employee, Attendance, LeaveRequest, Payroll, 
                        SalaryComponent, TimeOffType, LeaveAllocation,
                        create_salary_components_for_employee, allocate_leave_for_employee,
                        initialize_timeoff_types)
from datetime import datetime, date, timedelta
from sqlalchemy import func, or_
from decimal import Decimal
import calendar

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
            
            # Update salary if provided
            salary = request.form.get('salary')
            if salary:
                employee.salary = Decimal(salary)
            
            # Update date of birth
            dob = request.form.get('date_of_birth')
            if dob:
                employee.date_of_birth = datetime.strptime(dob, '%Y-%m-%d').date()
            
            # Update hire date
            hire_date = request.form.get('hire_date')
            if hire_date:
                employee.hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
            
            employee.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Employee updated successfully!', 'success')
            return redirect(url_for('admin.employee_detail', employee_id=employee_id))
            
        except ValueError:
            flash('Invalid input data!', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Error updating employee. Please try again.', 'error')
    
    return render_template('admin/edit_employee.html', employee=employee)

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
        'admin_comment': leave_request.admin_comment
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
    
    query = Payroll.query
    
    if employee_id:
        query = query.filter(Payroll.employee_id == employee_id)
    
    payroll_records = query.order_by(Payroll.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get all employees for filter
    employees = Employee.query.all()
    
    return render_template('admin/payroll.html',
                         payroll_records=payroll_records,
                         employees=employees,
                         selected_employee=employee_id)

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
            pay_period_start = datetime.strptime(request.form.get('pay_period_start'), '%Y-%m-%d').date()
            pay_period_end = datetime.strptime(request.form.get('pay_period_end'), '%Y-%m-%d').date()
            basic_salary = Decimal(request.form.get('basic_salary'))
            allowances = Decimal(request.form.get('allowances', '0'))
            deductions = Decimal(request.form.get('deductions', '0'))
            overtime_hours = float(request.form.get('overtime_hours', '0'))
            overtime_rate = Decimal(request.form.get('overtime_rate', '0'))
            tax_deductions = Decimal(request.form.get('tax_deductions', '0'))
            
            payroll = Payroll(
                employee_id=employee_id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end,
                basic_salary=basic_salary,
                allowances=allowances,
                deductions=deductions,
                overtime_hours=overtime_hours,
                overtime_rate=overtime_rate,
                tax_deductions=tax_deductions
            )
            
            payroll.calculate_net_pay()
            
            db.session.add(payroll)
            db.session.commit()
            
            flash('Payroll record created successfully!', 'success')
            return redirect(url_for('admin.payroll'))
            
        except ValueError:
            flash('Invalid input data!', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Error creating payroll record. Please try again.', 'error')
    
    employees = Employee.query.all()
    return render_template('admin/create_payroll.html', employees=employees)

@admin_bp.route('/payroll/<int:payroll_id>')
@login_required
@admin_required
def get_payroll(payroll_id):
    payroll = Payroll.query.get_or_404(payroll_id)
    return jsonify({
        'id': payroll.id,
        'employee_name': payroll.employee.full_name,
        'employee_id': payroll.employee.user.employee_id,
        'department': payroll.employee.department,
        'position': payroll.employee.position,
        'pay_period': f"{payroll.pay_period_start.strftime('%Y-%m-%d')} to {payroll.pay_period_end.strftime('%Y-%m-%d')}",
        'basic_salary': float(payroll.basic_salary),
        'allowances': float(payroll.allowances),
        'overtime_pay': float(payroll.overtime_hours * payroll.overtime_rate),
        'gross_salary': float(payroll.gross_pay) if payroll.gross_pay else 0,
        'deductions': float(payroll.deductions),
        'tax_deductions': float(payroll.tax_deductions),
        'total_deductions': float(payroll.deductions + payroll.tax_deductions),
        'net_salary': float(payroll.net_pay) if payroll.net_pay else 0,
        'payment_status': 'paid',
        'created_at': payroll.created_at.strftime('%Y-%m-%d')
    })

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