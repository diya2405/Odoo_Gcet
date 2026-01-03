from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory
from flask_login import login_required, current_user
from app.models import db, Employee, Attendance, LeaveRequest, Payroll, Certificate
from datetime import datetime, date, time, timedelta
from werkzeug.utils import secure_filename
import os

employee_bp = Blueprint('employee', __name__)

# Configuration for file uploads
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_DOCUMENT = {'pdf', 'doc', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_size(file):
    """Get file size in bytes"""
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    return size

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
            # Update personal information
            employee.phone = request.form.get('phone', '').strip()
            employee.personal_email = request.form.get('personal_email', '').strip()
            employee.address = request.form.get('address', '').strip()
            employee.gender = request.form.get('gender', '')
            employee.marital_status = request.form.get('marital_status', '')
            employee.nationality = request.form.get('nationality', 'Indian')
            
            # Date of birth
            dob_str = request.form.get('date_of_birth', '')
            if dob_str:
                try:
                    employee.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            # Emergency contact
            employee.emergency_contact_name = request.form.get('emergency_contact_name', '').strip()
            employee.emergency_contact_phone = request.form.get('emergency_contact_phone', '').strip()
            employee.emergency_contact_relationship = request.form.get('emergency_contact_relationship', '').strip()
            
            # Bank details
            employee.bank_name = request.form.get('bank_name', '').strip()
            employee.account_number = request.form.get('account_number', '').strip()
            employee.ifsc_code = request.form.get('ifsc_code', '').strip()
            
            # Government IDs
            employee.pan_no = request.form.get('pan_no', '').strip()
            employee.uan_no = request.form.get('uan_no', '').strip()
            
            # Skills and interests
            employee.skills = request.form.get('skills', '').strip()
            employee.interests = request.form.get('interests', '').strip()
            
            # Handle profile picture upload
            if 'profile_picture' in request.files:
                file = request.files['profile_picture']
                if file and file.filename != '':
                    if allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGE):
                        file_size = get_file_size(file)
                        if file_size <= MAX_FILE_SIZE:
                            # Create uploads directory if not exists
                            uploads_dir = os.path.join('uploads', 'profiles')
                            os.makedirs(uploads_dir, exist_ok=True)
                            
                            # Delete old profile picture if exists
                            if employee.profile_picture:
                                old_file_path = os.path.join(uploads_dir, employee.profile_picture)
                                if os.path.exists(old_file_path):
                                    os.remove(old_file_path)
                            
                            filename = secure_filename(f"{current_user.employee_id}_profile_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}")
                            file_path = os.path.join(uploads_dir, filename)
                            file.save(file_path)
                            employee.profile_picture = filename
                        else:
                            flash('Profile picture size must be less than 10MB!', 'error')
                    else:
                        flash('Invalid file type for profile picture! Allowed: PNG, JPG, JPEG, GIF', 'error')
            
            # Handle resume upload
            if 'resume' in request.files:
                file = request.files['resume']
                if file and file.filename != '':
                    if allowed_file(file.filename, ALLOWED_EXTENSIONS_DOCUMENT):
                        file_size = get_file_size(file)
                        if file_size <= MAX_FILE_SIZE:
                            # Create uploads directory if not exists
                            uploads_dir = os.path.join('uploads', 'documents')
                            os.makedirs(uploads_dir, exist_ok=True)
                            
                            # Delete old resume if exists
                            if employee.resume:
                                old_file_path = os.path.join(uploads_dir, employee.resume)
                                if os.path.exists(old_file_path):
                                    os.remove(old_file_path)
                            
                            filename = secure_filename(f"{current_user.employee_id}_resume_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}")
                            file_path = os.path.join(uploads_dir, filename)
                            file.save(file_path)
                            employee.resume = filename
                        else:
                            flash('Resume size must be less than 10MB!', 'error')
                    else:
                        flash('Invalid file type for resume! Allowed: PDF, DOC, DOCX, TXT', 'error')
            
            employee.updated_at = datetime.utcnow()
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('employee.employee_profile'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'error')
    
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
            
            # Handle medical certificate for sick leave
            certificate_path = None
            if leave_type == 'sick':
                if 'medical_certificate' not in request.files:
                    flash('Medical certificate is required for sick leave!', 'error')
                    return render_template('employee/apply_leave.html', employee=employee)
                
                file = request.files['medical_certificate']
                if file.filename == '':
                    flash('Medical certificate is required for sick leave!', 'error')
                    return render_template('employee/apply_leave.html', employee=employee)
                
                if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_DOCUMENT):
                    file_size = get_file_size(file)
                    if file_size > MAX_FILE_SIZE:
                        flash('File size exceeds 10MB limit!', 'error')
                        return render_template('employee/apply_leave.html', employee=employee)
                    
                    # Create uploads directory for medical certificates
                    uploads_dir = os.path.join('uploads', 'medical_certificates')
                    os.makedirs(uploads_dir, exist_ok=True)
                    
                    # Generate secure filename
                    filename = secure_filename(f"{current_user.employee_id}_medical_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    certificate_path = os.path.join(uploads_dir, filename)
                    file.save(certificate_path)
                else:
                    flash('Invalid file format! Only PDF, DOC, DOCX files are allowed.', 'error')
                    return render_template('employee/apply_leave.html', employee=employee)
            
            # Create leave request
            leave_request = LeaveRequest(
                employee_id=employee.id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                certificate_path=certificate_path
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
            flash(f'Error submitting leave request: {str(e)}', 'error')
    
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


# Certificate Management Routes
@employee_bp.route('/upload_certificate', methods=['POST'])
@login_required
def upload_certificate():
    if current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})
    
    employee = current_user.employee_profile
    
    try:
        if 'certificate_file' not in request.files:
            return jsonify({'success': False, 'message': 'No file selected'})
        
        file = request.files['certificate_file']
        certificate_name = request.form.get('certificate_name', '').strip()
        issuing_organization = request.form.get('issuing_organization', '').strip()
        description = request.form.get('description', '').strip()
        
        if not certificate_name:
            return jsonify({'success': False, 'message': 'Certificate name is required'})
        
        if file and file.filename != '':
            if allowed_file(file.filename, ALLOWED_EXTENSIONS_DOCUMENT):
                file_size = get_file_size(file)
                if file_size <= MAX_FILE_SIZE:
                    # Create uploads directory if not exists
                    uploads_dir = os.path.join('uploads', 'certificates')
                    os.makedirs(uploads_dir, exist_ok=True)
                    
                    filename = secure_filename(f"{current_user.employee_id}_cert_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                    file_path = os.path.join(uploads_dir, filename)
                    file.save(file_path)
                    
                    # Parse dates if provided
                    issue_date = None
                    expiry_date = None
                    issue_date_str = request.form.get('issue_date', '')
                    expiry_date_str = request.form.get('expiry_date', '')
                    
                    if issue_date_str:
                        try:
                            issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            pass
                    
                    if expiry_date_str:
                        try:
                            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            pass
                    
                    # Create certificate record
                    certificate = Certificate(
                        employee_id=employee.id,
                        certificate_name=certificate_name,
                        certificate_file=filename,
                        issue_date=issue_date,
                        expiry_date=expiry_date,
                        issuing_organization=issuing_organization,
                        description=description,
                        file_size=file_size
                    )
                    
                    db.session.add(certificate)
                    db.session.commit()
                    
                    return jsonify({
                        'success': True, 
                        'message': 'Certificate uploaded successfully!',
                        'certificate_id': certificate.id
                    })
                else:
                    return jsonify({'success': False, 'message': 'File size must be less than 10MB'})
            else:
                return jsonify({'success': False, 'message': 'Invalid file type! Allowed: PDF, DOC, DOCX'})
        else:
            return jsonify({'success': False, 'message': 'No file selected'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error uploading certificate: {str(e)}'})


@employee_bp.route('/delete_certificate/<int:certificate_id>', methods=['POST'])
@login_required
def delete_certificate(certificate_id):
    if current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})
    
    employee = current_user.employee_profile
    
    try:
        certificate = Certificate.query.filter_by(
            id=certificate_id,
            employee_id=employee.id
        ).first()
        
        if not certificate:
            return jsonify({'success': False, 'message': 'Certificate not found'})
        
        # Delete file from filesystem
        file_path = os.path.join('uploads', 'certificates', certificate.certificate_file)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete from database
        db.session.delete(certificate)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Certificate deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error deleting certificate: {str(e)}'})


@employee_bp.route('/delete_resume', methods=['POST'])
@login_required
def delete_resume():
    if current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})
    
    employee = current_user.employee_profile
    
    try:
        if not employee.resume:
            return jsonify({'success': False, 'message': 'No resume found'})
        
        # Delete file from filesystem
        file_path = os.path.join('uploads', 'documents', employee.resume)
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Update database
        employee.resume = None
        employee.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Resume deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error deleting resume: {str(e)}'})


@employee_bp.route('/download/<file_type>/<filename>')
@login_required
def download_file(file_type, filename):
    """Download uploaded files"""
    try:
        # Get base upload directory (absolute path)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
        
        # Map file types to directories
        file_dirs = {
            'profile': 'profiles',
            'certificate': 'certificates',
            'document': 'documents',
            'medical': 'medical_certificates'
        }
        
        if file_type not in file_dirs:
            flash('Invalid file type', 'error')
            return redirect(url_for('employee.employee_profile'))
        
        # Build the file path
        file_dir = os.path.join(base_dir, file_dirs[file_type])
        
        # Security check - ensure the file exists and is in the correct directory
        file_path = os.path.join(file_dir, secure_filename(filename))
        if not os.path.exists(file_path):
            flash('File not found', 'error')
            return redirect(url_for('employee.employee_profile'))
        
        # Additional security: ensure the resolved path is within the upload directory
        if not os.path.abspath(file_path).startswith(base_dir):
            flash('Access denied', 'error')
            return redirect(url_for('employee.employee_profile'))
        
        return send_from_directory(file_dir, secure_filename(filename), as_attachment=True)
        
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('employee.employee_profile'))
        
        if file_type == 'certificate':
            subdirectory = 'certificates'
        elif file_type == 'resume':
            subdirectory = 'documents'
        elif file_type == 'profile':
            subdirectory = 'profiles'
        else:
            flash('Invalid file type', 'error')
            return redirect(url_for('employee.employee_profile'))
        
        # Full directory path
        directory = os.path.join(base_dir, subdirectory)
        file_path = os.path.join(directory, filename)
        
        if not os.path.exists(file_path):
            flash('File not found', 'error')
            return redirect(url_for('employee.employee_profile'))
        
        return send_from_directory(directory, filename, as_attachment=True)
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect(url_for('employee.employee_profile'))


@employee_bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded files for display (profile pictures)"""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'uploads'))
    return send_from_directory(base_dir, filename)
