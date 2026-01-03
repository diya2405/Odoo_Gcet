from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import db, Employee, Attendance, LeaveRequest, Payroll
from datetime import datetime, date, time, timedelta
from werkzeug.utils import secure_filename
import os

employee_bp = Blueprint('employee', __name__)

@employee_bp.route('/profile')
@login_required
def employee_profile():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    
    employee = current_user.employee_profile
    if not employee:
        flash('Employee profile not found!', 'error')
        return redirect(url_for('auth.logout'))
    
    return render_template('employee/profile.html', employee=employee)

@employee_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    
    employee = current_user.employee_profile
    if not employee:
        flash('Employee profile not found!', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        try:
            # Update editable fields
            employee.phone = request.form.get('phone', '')
            employee.address = request.form.get('address', '')
            
            # Handle profile picture upload
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file and file.filename != '':
                    filename = secure_filename(f"{current_user.employee_id}_{file.filename}")
                    file_path = os.path.join('uploads', filename)
                    file.save(file_path)
                    employee.profile_picture = filename
            
            employee.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Error updating profile. Please try again.', 'error')
    
    return render_template('employee/edit_profile.html', employee=employee)

@employee_bp.route('/attendance')
@login_required
def attendance():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    
    employee = current_user.employee_profile
    
    # Get current month's attendance
    today = date.today()
    start_of_month = today.replace(day=1)
    
    attendance_records = Attendance.query.filter(
        Attendance.employee_id == employee.id,
        Attendance.date >= start_of_month
    ).order_by(Attendance.date.desc()).all()
    
    # Get today's attendance
    todays_attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
    # Calculate monthly statistics
    total_present = sum(1 for a in attendance_records if a.status == 'present')
    total_absent = sum(1 for a in attendance_records if a.status == 'absent')
    total_half_days = sum(1 for a in attendance_records if a.status == 'half_day')
    total_hours = sum(a.hours_worked or 0 for a in attendance_records)
    
    context = {
        'employee': employee,
        'attendance_records': attendance_records,
        'todays_attendance': todays_attendance,
        'stats': {
            'present': total_present,
            'absent': total_absent,
            'half_days': total_half_days,
            'total_hours': round(total_hours, 1)
        }
    }
    
    return render_template('employee/attendance.html', **context)

@employee_bp.route('/check_in', methods=['POST'])
@login_required
def check_in():
    if current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})
    
    employee = current_user.employee_profile
    today = date.today()
    
    # Check if already checked in today
    existing_attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
    if existing_attendance and existing_attendance.check_in_time:
        return jsonify({'success': False, 'message': 'Already checked in today'})
    
    try:
        current_time = datetime.now().time()
        
        if existing_attendance:
            # Update existing record
            existing_attendance.check_in_time = current_time
            existing_attendance.status = 'present'
        else:
            # Create new attendance record
            attendance = Attendance(
                employee_id=employee.id,
                date=today,
                check_in_time=current_time,
                status='present'
            )
            db.session.add(attendance)
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Checked in successfully', 'time': current_time.strftime('%H:%M:%S')})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error during check-in'})

@employee_bp.route('/check_out', methods=['POST'])
@login_required
def check_out():
    if current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})
    
    employee = current_user.employee_profile
    today = date.today()
    
    attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
    if not attendance or not attendance.check_in_time:
        return jsonify({'success': False, 'message': 'Please check in first'})
    
    if attendance.check_out_time:
        return jsonify({'success': False, 'message': 'Already checked out today'})
    
    try:
        current_time = datetime.now().time()
        attendance.check_out_time = current_time
        
        # Calculate hours worked
        attendance.calculate_hours_worked()
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'message': 'Checked out successfully',
            'time': current_time.strftime('%H:%M:%S'),
            'hours_worked': round(attendance.hours_worked, 2)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Error during check-out'})

@employee_bp.route('/leave_requests')
@login_required
def leave_requests():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    
    employee = current_user.employee_profile
    
    leave_requests = LeaveRequest.query.filter_by(
        employee_id=employee.id
    ).order_by(LeaveRequest.created_at.desc()).all()
    
    return render_template('employee/leave_requests.html', 
                         employee=employee, 
                         leave_requests=leave_requests)

@employee_bp.route('/apply_leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    
    employee = current_user.employee_profile
    
    if request.method == 'POST':
        try:
            leave_type = request.form.get('leave_type')
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
            reason = request.form.get('reason')
            
            if start_date > end_date:
                flash('Start date cannot be after end date!', 'error')
                return render_template('employee/apply_leave.html', employee=employee)
            
            if start_date < date.today():
                flash('Cannot apply for leave in the past!', 'error')
                return render_template('employee/apply_leave.html', employee=employee)
            
            # Create leave request
            leave_request = LeaveRequest(
                employee_id=employee.id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason
            )
            leave_request.calculate_days()
            
            db.session.add(leave_request)
            db.session.commit()
            
            flash('Leave request submitted successfully!', 'success')
            return redirect(url_for('employee.leave_requests'))
            
        except ValueError:
            flash('Invalid date format!', 'error')
        except Exception as e:
            db.session.rollback()
            flash('Error submitting leave request. Please try again.', 'error')
    
    return render_template('employee/apply_leave.html', employee=employee)

@employee_bp.route('/payroll')
@login_required
def payroll():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    
    employee = current_user.employee_profile
    
    payroll_records = Payroll.query.filter_by(
        employee_id=employee.id
    ).order_by(Payroll.created_at.desc()).all()
    
    return render_template('employee/payroll.html', 
                         employee=employee, 
                         payroll_records=payroll_records)