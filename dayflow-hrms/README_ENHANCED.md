# Dayflow - Human Resource Management System 🚀

**Every workday, perfectly aligned.** Complete HRMS with automated employee ID generation, comprehensive salary components, attendance tracking, and intelligent leave management.

## 🌟 Key Features

### 🆔 Automated Employee Management
- **Auto-generated Employee IDs**: `[Company][FirstName][LastName][Year][Serial]` (e.g., OIJODO20220001)
- **Auto-generated Passwords**: Secure random passwords for new employees
- **Complete Profile Management**: Personal info, bank details, government IDs, skills, certifications
- **Manager Hierarchy**: Self-referential employee relationships
- **Real-time Status Indicators**: 🟢 Present, 🟡 Absent, ✈️ On Leave

### 💰 Advanced Salary & Payroll
- **Automated Salary Components**:
  - Basic Salary (50% of wage)
  - House Rent Allowance - HRA (50% of basic)
  - Performance Bonus (8.33% of wage)
  - Leave Travel Allowance - LTA (8.33% of wage)
  - Standard Allowance (calculated to match total wage)
- **Automatic Tax Deductions**:
  - Provident Fund - PF (12% of basic salary)
  - Professional Tax (Fixed ₹200)
- **Attendance-based Payroll**: Auto-adjusts for unpaid leaves and days present
- **Comprehensive Payslips**: Detailed earning and deduction breakdown

### ⏰ Smart Attendance System
- **Easy Check-In/Check-Out**: One-click attendance marking
- **Break Time Tracking**: Accurate work hours calculation
- **Daily/Monthly Reports**: Comprehensive attendance statistics
- **Status Tracking**: Present, Absent, Half-day, On Leave
- **Admin Override**: Manual attendance management

### 📅 Intelligent Leave Management
- **Multiple Leave Types**:
  - **Paid Time Off (PTO)**: 24 days per year
  - **Sick Leave**: 7 days per year (requires medical certificate)
  - **Unpaid Leave**: No limit, salary adjusted
- **Leave Balance Tracking**: Real-time available days per type
- **Approval Workflow**: Submit → Pending → Approved/Rejected
- **Certificate Upload**: Document attachment for sick leave
- **Leave Allocations**: Automatic yearly allocation

### 📊 Admin Dashboard & Analytics
- 📈 Real-time employee statistics
- 👥 Department-wise summaries
- 📝 Pending leave requests overview
- 📅 Daily attendance tracking
- 💰 Payroll management and generation
- 🔍 Advanced search and filtering

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL Server (or SQLite for testing)
- pip (Python package installer)

### Installation Steps

1. **Navigate to project directory**
```bash
cd dayflow-hrms
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize database with all features**
```bash
python init_enhanced_db.py
```

This command will:
- ✅ Create all database tables
- ✅ Initialize default time off types (PTO, Sick Leave, Unpaid Leave)
- ✅ Create admin user account
- ✅ Create sample employee account
- ✅ Setup salary components for all employees
- ✅ Allocate leave balances

4. **Run the application**
```bash
python run.py
```

5. **Access the application**
Open your browser: `http://localhost:5000`

### 🔑 Default Credentials

**Admin Account**:
- **Email**: `admin@dayflow.com`
- **Password**: `Admin@123`
- **Employee ID**: Auto-generated (displayed after init)

**Sample Employee**:
- **Email**: `john.doe@dayflow.com`
- **Password**: Auto-generated (displayed after init)
- **Employee ID**: Auto-generated (displayed after init)

## 📁 Project Structure

```
dayflow-hrms/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models.py                # Database models (User, Employee, Attendance, etc.)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py             # Admin routes (employee mgmt, payroll)
│   │   ├── auth.py              # Authentication (login, logout)
│   │   ├── employee.py          # Employee routes (profile, attendance)
│   │   └── main.py              # Dashboard routes
│   ├── static/
│   │   ├── css/                 # Stylesheets
│   │   ├── js/                  # JavaScript files
│   │   └── images/              # Images and icons
│   └── templates/
│       ├── base.html            # Base template
│       ├── admin/               # Admin templates
│       ├── auth/                # Auth templates (login, signup)
│       └── employee/            # Employee templates
├── instance/                    # Instance-specific files
├── uploads/                     # Uploaded files
│   ├── profiles/                # Profile pictures
│   └── documents/               # Certificates, resumes
├── init_enhanced_db.py          # Enhanced database initialization
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── FEATURE_IMPLEMENTATION.md    # Detailed feature documentation
```

## 🔧 Configuration

### Database Configuration
Edit in `app/__init__.py`:
```python
# MySQL (Production)
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/dayflow_db'

# SQLite (Development/Testing) - Default
SQLALCHEMY_DATABASE_URI = 'sqlite:///dayflow.db'
```

### Company Settings
Edit in `app/routes/admin.py`:
```python
company_code = "OI"  # Change to your company code
```

### Salary Component Customization
Edit in `app/models.py` → `create_salary_components_for_employee()`:
- Adjust Basic Salary percentage (default: 50%)
- Modify HRA percentage (default: 50% of basic)
- Change Performance Bonus percentage (default: 8.33%)
- Update LTA percentage (default: 8.33%)
- Set PF percentage (default: 12%)
- Modify Professional Tax amount (default: ₹200)

## 📚 Complete Feature Documentation

See [FEATURE_IMPLEMENTATION.md](FEATURE_IMPLEMENTATION.md) for:
- ✅ Detailed feature explanations
- ✅ Implementation details
- ✅ Database schema with relationships
- ✅ Complete usage workflows
- ✅ API endpoint documentation
- ✅ Calculation formulas
- ✅ Setup and configuration guide

## 🎯 Usage Guide

### For Administrators:

1. **Login** with admin credentials
2. **Add New Employees**:
   - Navigate to "Employees" → "Add Employee"
   - Fill in employee details
   - System auto-generates Employee ID and Password
   - Share credentials with new employee
3. **Monitor Attendance**:
   - View daily attendance status with status indicators
   - See who's present (🟢), absent (🟡), or on leave (✈️)
4. **Manage Leave Requests**:
   - Review pending leave applications
   - Approve or reject with comments
   - View leave balance for each employee
5. **Generate Payroll**:
   - Select pay period
   - System auto-calculates based on attendance and components
   - Generate payslips for employees
6. **View Analytics**:
   - Dashboard shows real-time statistics
   - Department-wise summaries
   - Attendance trends

### For Employees:

1. **First Login**:
   - Login with provided credentials
   - **Change password** immediately
2. **Daily Routine**:
   - **Check In** when starting work
   - **Check Out** when leaving
   - System calculates hours worked
3. **Apply for Leave**:
   - Navigate to "Time Off" → "Apply Leave"
   - Select leave type and dates
   - Provide reason
   - Upload certificate (for sick leave)
   - Submit for approval
4. **View Information**:
   - Check attendance history
   - View leave balance
   - Review payroll and salary breakdown
   - Update profile information

## 💡 Example: Employee ID Generation

### Format
`[CompanyCode][FirstName][LastName][Year][Serial]`

### Examples
- **John Doe** joining in **2022**: `OIJODO20220001`
  - OI: Odoo India
  - JO: First two letters of "John"
  - DO: First two letters of "Doe"
  - 2022: Year of joining
  - 0001: First employee with this name pattern in 2022

- **Jane Smith** joining in **2022**: `OIJASM20220001`

## 💰 Salary Calculation Example

### For Monthly Wage of ₹50,000:

**Earnings:**
- Basic Salary: ₹25,000 (50% of wage)
- HRA: ₹12,500 (50% of basic)
- Performance Bonus: ₹4,165 (8.33% of wage)
- LTA: ₹4,165 (8.33% of wage)
- Standard Allowance: ₹4,170 (remaining to match wage)
- **Gross Pay**: ₹50,000

**Deductions:**
- Provident Fund: ₹3,000 (12% of basic)
- Professional Tax: ₹200 (fixed)
- **Total Deductions**: ₹3,200

**Net Pay**: ₹46,800

*Note: If employee has unpaid leaves, additional deductions apply*

## 🔐 Security Features

- ✅ **Password Hashing**: Werkzeug secure password hashing
- ✅ **Role-Based Access**: Admin and Employee roles with different permissions
- ✅ **Session Management**: Flask-Login secure sessions
- ✅ **CSRF Protection**: Built-in Flask security
- ✅ **Password Policy**: Minimum length, complexity requirements
- ✅ **First Login Security**: Forced password change for new employees
- ✅ **Email Verification**: Account verification system

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Database**: MySQL with SQLAlchemy ORM / SQLite for development
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **File Upload**: Werkzeug secure filename handling
- **Image Processing**: Pillow (PIL)

## 📊 Database Models

### Core Models:
1. **User** - Authentication and login
2. **Employee** - Complete employee profile
3. **Attendance** - Daily attendance records
4. **TimeOffType** - Leave type definitions
5. **LeaveAllocation** - Employee leave balance
6. **LeaveRequest** - Leave applications
7. **SalaryComponent** - Salary structure
8. **Payroll** - Payroll records

### Relationships:
- User ↔ Employee (One-to-One)
- Employee ↔ Manager (Self-referential Many-to-One)
- Employee → Attendance (One-to-Many)
- Employee → LeaveRequest (One-to-Many)
- Employee → SalaryComponent (One-to-Many)

## 🔄 API Endpoints Overview

### Authentication
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Employee Self-Service
- `GET /employee/profile` - View own profile
- `POST /employee/edit_profile` - Update profile
- `POST /employee/check_in` - Mark attendance check-in
- `POST /employee/check_out` - Mark attendance check-out
- `POST /employee/apply_leave` - Submit leave request

### Admin Management
- `GET /admin/employees` - List all employees
- `POST /admin/employee/add` - Create new employee
- `GET /admin/employee/<id>` - Employee details
- `POST /admin/leave/<id>/approve` - Approve leave
- `GET /admin/payroll` - Payroll management

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check MySQL is running
mysql -u root -p

# Create database if needed
CREATE DATABASE dayflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Login Problems
- Clear browser cookies and cache
- Verify database initialization completed successfully
- Check credentials match those displayed after init

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support & Contact

For questions, issues, or feature requests:
- Check [FEATURE_IMPLEMENTATION.md](FEATURE_IMPLEMENTATION.md) for detailed docs
- Review code comments in `app/models.py`
- Examine route handlers in `app/routes/`

## 🎉 Acknowledgments

Built with modern HR best practices and workflow automation in mind.

---

**Dayflow HRMS** - Complete Human Resource Management Solution  
Version: 2.0 Enhanced Edition  
© 2026 Dayflow. All rights reserved.
