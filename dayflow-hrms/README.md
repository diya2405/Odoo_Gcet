# Dayflow - Human Resource Management System

**Every workday, perfectly aligned.**

## Overview

Dayflow is a comprehensive Human Resource Management System (HRMS) built with Flask that digitizes and streamlines core HR operations. The system provides role-based access for administrators and employees, enabling efficient management of employee profiles, attendance tracking, leave management, and payroll visibility.

## Features

### Core Functionality
- **Secure Authentication**: Sign Up / Sign In with role-based access
- **Employee Profile Management**: View and edit personal information
- **Attendance Tracking**: Daily check-in/check-out with automatic time calculation
- **Leave Management**: Apply for leave, track status, admin approval workflow
- **Payroll Visibility**: View salary details and payroll history
- **Admin Dashboard**: Comprehensive management tools for HR officers

### User Roles
- **Admin/HR Officer**: Full system access, employee management, approvals
- **Employee**: Personal data access, attendance marking, leave applications

## Technology Stack

- **Backend**: Python Flask Framework
- **Database**: MySQL with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript/jQuery
- **Authentication**: Flask-Login with secure password hashing
- **Architecture**: MVC (Model-View-Controller) pattern

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- XAMPP (recommended for local development)

## Installation

### 1. Clone or Download the Project
```bash
cd dayflow-hrms
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Start MySQL Server
- If using XAMPP: Start Apache and MySQL services
- Default MySQL runs on `localhost:3306`

#### Create Database
```sql
CREATE DATABASE dayflow_hrms;
```

#### Update Database Configuration
Edit `app.py` if needed to match your MySQL credentials:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dayflow_hrms'
```

### 5. Initialize Database Tables
```bash
python app.py
```
The application will automatically create all necessary tables on first run.

### 6. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## Default Access

### Create Admin Account
1. Visit `http://localhost:5000/auth/signup`
2. Fill in the registration form
3. Select "Admin/HR" as the role
4. Complete registration

### Create Employee Account
1. Use the same signup process
2. Select "Employee" as the role
3. Complete registration

## Project Structure

```
dayflow-hrms/
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── uploads/                        # File uploads directory
├── app/
│   ├── models.py                   # Database models
│   ├── routes/
│   │   ├── auth.py                # Authentication routes
│   │   ├── main.py                # Main dashboard routes
│   │   ├── employee.py            # Employee-specific routes
│   │   └── admin.py               # Admin-specific routes
│   ├── templates/
│   │   ├── base.html              # Base template
│   │   ├── auth/                  # Authentication templates
│   │   ├── employee/              # Employee templates
│   │   └── admin/                 # Admin templates
│   └── static/
│       ├── css/
│       │   └── style.css          # Custom styles
│       ├── js/
│       │   └── script.js          # Custom JavaScript
│       └── images/                # Static images
```

## Database Schema

### Users Table
- User authentication and role management
- Links to employee profiles

### Employees Table
- Personal information, job details, salary
- Profile pictures and documents

### Attendance Table
- Daily check-in/check-out records
- Hours calculation and status tracking

### Leave Requests Table
- Leave applications with approval workflow
- Admin comments and status updates

### Payroll Table
- Salary calculations, allowances, deductions
- Pay period tracking

## Key Features Explanation

### Authentication System
- Secure password hashing with Werkzeug
- Role-based access control
- Session management with Flask-Login

### Attendance Management
- Real-time check-in/check-out via AJAX
- Automatic hours calculation
- Monthly statistics and reporting

### Leave Management
- Multiple leave types (Paid, Sick, Unpaid)
- Date range validation
- Admin approval workflow with comments

### Admin Dashboard
- Employee overview and statistics
- Attendance monitoring
- Leave request approvals
- Payroll management

## Usage Guide

### For Employees
1. **Login**: Use your credentials to access the system
2. **Dashboard**: View quick stats and recent activity
3. **Attendance**: Mark daily check-in/check-out
4. **Leave Requests**: Apply for time off and track status
5. **Profile**: View and update personal information
6. **Payroll**: View salary details and history

### For Administrators
1. **Dashboard**: Monitor overall system statistics
2. **Employee Management**: Add, view, and edit employee records
3. **Attendance**: Monitor and update attendance records
4. **Leave Approvals**: Review and process leave requests
5. **Payroll**: Manage employee salary and payroll records

## Security Features

- Password strength validation
- Secure session management
- Role-based access controls
- SQL injection protection via SQLAlchemy
- CSRF protection (can be enhanced)

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in `app.py`
   - Verify database exists

2. **Template Not Found**
   - Check file paths in templates directory
   - Ensure template extends base.html correctly

3. **Static Files Not Loading**
   - Verify static files are in correct directories
   - Check Flask static folder configuration

4. **Permission Errors**
   - Ensure uploads directory has write permissions
   - Check file permissions in project directory

## Future Enhancements

- Email notifications for leave approvals
- Advanced reporting and analytics
- Document management system
- Integration with payroll systems
- Mobile responsive improvements
- API endpoints for external integrations

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper testing
4. Submit pull request with detailed description

## Support

For issues and support:
- Check the troubleshooting section
- Review error logs in console
- Ensure all dependencies are properly installed

## License

This project is developed for educational and demonstration purposes. Please ensure compliance with your organization's policies before deployment in production environments.

---

**Dayflow HRMS - Every workday, perfectly aligned.**