from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import db, Employee, Attendance, LeaveRequest, Payroll
from datetime import datetime, date, timedelta
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('main.admin_dashboard'))
        else:
            return redirect(url_for('main.employee_dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/employee_dashboard')
@login_required
def employee_dashboard():
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
    
    employee = current_user.employee_profile
    if not employee:
        return redirect(url_for('auth.logout'))
    
    # Get today's attendance
    today = date.today()
    todays_attendance = Attendance.query.filter_by(
        employee_id=employee.id,
        date=today
    ).first()
    
    # Get recent attendance (last 7 days)
    week_ago = today - timedelta(days=7)
    recent_attendance = Attendance.query.filter(
        Attendance.employee_id == employee.id,
        Attendance.date >= week_ago
    ).order_by(Attendance.date.desc()).limit(7).all()
    
    # Get pending leave requests
    pending_leaves = LeaveRequest.query.filter_by(
        employee_id=employee.id,
        status='pending'
    ).count()
    
    # Get approved leaves this month
    first_of_month = today.replace(day=1)
    approved_leaves = LeaveRequest.query.filter(
        LeaveRequest.employee_id == employee.id,
        LeaveRequest.status == 'approved',
        LeaveRequest.start_date >= first_of_month
    ).count()
    
    # Get latest payroll
    latest_payroll = Payroll.query.filter_by(
        employee_id=employee.id
    ).order_by(Payroll.created_at.desc()).first()
    
    # Calculate total hours worked this month
    total_hours = db.session.query(func.sum(Attendance.hours_worked)).filter(
        Attendance.employee_id == employee.id,
        Attendance.date >= first_of_month,
        Attendance.status.in_(['present', 'half_day'])
    ).scalar() or 0
    
    context = {
        'employee': employee,
        'todays_attendance': todays_attendance,
        'recent_attendance': recent_attendance,
        'pending_leaves': pending_leaves,
        'approved_leaves': approved_leaves,
        'latest_payroll': latest_payroll,
        'total_hours': round(total_hours, 1)
    }
    
    return render_template('employee/dashboard.html', **context)

@main_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin():
        return redirect(url_for('main.employee_dashboard'))
    
    # Get all employees with their current status
    all_employees = Employee.query.all()
    
    # Get today's date
    today = date.today()
    
    # Count employees by status
    present_count = 0
    absent_count = 0
    on_leave_count = 0
    
    for emp in all_employees:
        status = emp.current_status
        if status == 'present':
            present_count += 1
        elif status == 'on_leave':
            on_leave_count += 1
        else:
            absent_count += 1
    
    total_employees = len(all_employees)
    
    # Get pending leave requests
    pending_leaves = LeaveRequest.query.filter_by(status='pending').count()
    
    # Get recent leave requests (last 10)
    recent_leave_requests = LeaveRequest.query.order_by(
        LeaveRequest.created_at.desc()
    ).limit(10).all()
    
    # Department wise summary
    department_summary = db.session.query(
        Employee.department,
        func.count(Employee.id).label('count')
    ).group_by(Employee.department).all()
    
    context = {
        'total_employees': total_employees,
        'present_today': present_count,
        'absent_today': absent_count,
        'on_leave_today': on_leave_count,
        'pending_leaves': pending_leaves,
        'recent_leave_requests': recent_leave_requests,
        'all_employees': all_employees,
        'department_summary': department_summary
    }
    
    return render_template('admin/dashboard.html', **context)

@main_bp.route('/profile')
@login_required
def profile():
    if current_user.is_admin():
        return redirect(url_for('admin.admin_profile'))
    else:
        return redirect(url_for('employee.employee_profile'))