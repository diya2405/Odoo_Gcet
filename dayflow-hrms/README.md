# DayFlow HRMS - Human Resource Management System

A comprehensive Flask-based HRMS solution for managing employees, attendance, leave requests, payroll, and more.

## 🚀 Features

### Core Modules
- **User Management**
  - Role-based access control (Admin/Employee)
  - User activation/deactivation
  - Auto-generated employee IDs
  - Secure authentication with password strength validation

- **Employee Management**
  - Complete employee profiles
  - Department and position tracking
  - Personal information management
  - Profile pictures and documents

- **Attendance System**
  - Daily attendance tracking
  - Visual attendance calendar
  - Status: Present, Absent, Leave, Half-Day
  - Attendance reports

- **Leave Management**
  - Multiple leave types (Sick, Casual, Annual, Unpaid)
  - Medical certificate upload for sick leave (PDF/DOC/DOCX)
  - Leave request approval workflow
  - Leave balance tracking
  - Admin can download medical certificates

- **Salary & Payroll**
  - Comprehensive salary component system
  - Auto-calculation based on monthly wage:
    - Basic Salary: 50% of wage
    - HRA: 50% of basic
    - Standard Allowance: ₹4,167 (configurable)
    - Performance Bonus: 8.33% of wage
    - LTA: 8.333% of wage
    - Fixed Allowance: Auto-calculated remainder
  - Deductions:
    - Provident Fund: 12% of basic (configurable)
    - Professional Tax: ₹200 (configurable)
  - Detailed payroll records with salary breakdown
  - Automatic unpaid leave deduction calculation
  - Net salary computation

### Admin Features
- Employee CRUD operations
- Attendance management
- Leave request approval/rejection
- Payroll generation with detailed breakdown
- User account activation/deactivation
- User deletion with cascade cleanup
- Medical certificate verification
- Department-wise employee filtering

### Employee Features
- Personal dashboard
- View own attendance records
- Apply for leave with medical certificate upload
- View leave history and status
- View payslip with detailed breakdown
- Profile management

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd dayflow-hrms
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python init_enhanced_db.py
```

This will:
- Create the database with all required tables
- Set up default leave types
- Create an admin account

**Default Admin Credentials:**
- Employee ID: `ADMIN001`
- Email: `admin@dayflow.com`
- Password: `Admin@123`

### 5. Run the Application
```bash
python run.py
```

The application will be available at: `http://localhost:5000`

## 📁 Project Structure

```
dayflow-hrms/
├── app/
│   ├── __init__.py           # Application factory
│   ├── models.py             # Database models
│   ├── routes/               # Route blueprints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── admin.py         # Admin routes
│   │   ├── employee.py      # Employee routes
│   │   └── main.py          # Main routes
│   ├── static/               # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── templates/            # Jinja2 templates
│       ├── base.html
│       ├── auth/            # Auth templates
│       ├── admin/           # Admin templates
│       └── employee/        # Employee templates
├── instance/
│   └── dayflow_hrms.db      # SQLite database
├── uploads/                  # Uploaded files
│   ├── profiles/            # Profile pictures
│   ├── documents/           # Employee documents
│   ├── certificates/        # Certificates
│   └── medical_certificates/ # Medical certificates for leave
├── docs/                     # Documentation
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
├── setup.py                 # Setup script
└── README.md               # This file
```

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get started quickly
- **[Admin Guide](ADMIN_QUICK_GUIDE.md)** - Admin panel usage
- **[Database Guide](DATABASE_RESET_GUIDE.md)** - Database management
- **[Salary Configuration](SALARY_CONFIGURATION_GUIDE.md)** - Salary system setup
- **[Salary System Details](SALARY_SYSTEM_IMPLEMENTATION.md)** - Technical implementation
- **[Profile System](PROFILE_SYSTEM_GUIDE.md)** - Employee profiles

## 🔐 Security Features

- Password strength validation (minimum 8 characters, uppercase, lowercase, numbers)
- Password hashing using Werkzeug security
- Session-based authentication with Flask-Login
- Role-based access control
- CSRF protection
- SQL injection prevention through SQLAlchemy ORM
- File upload validation (type and size)
- Secure file naming

## 🗄️ Database Schema

### Main Tables
- **users** - User accounts and authentication
- **employees** - Employee profiles and information
- **attendance** - Daily attendance records
- **leave_requests** - Leave applications with medical certificates
- **payroll** - Salary payments and breakdowns
- **salary_components** - Individual salary components
- **timeoff_types** - Leave type definitions
- **leave_allocations** - Employee leave balances

## 🚀 Usage

### For Administrators

1. **Login** with admin credentials
2. **Dashboard** shows overview of employees, attendance, leaves
3. **Manage Employees**:
   - Add new employees
   - Edit employee details
   - Configure salary components
   - Deactivate/delete users
4. **Attendance Management**:
   - Mark daily attendance
   - View attendance reports
5. **Leave Management**:
   - Approve/reject leave requests
   - View and download medical certificates
6. **Payroll**:
   - Generate monthly payroll
   - View detailed salary breakdown
   - Track unpaid leave deductions

### For Employees

1. **Sign Up** - Register with email, name, and password (Employee ID auto-generated)
2. **Login** with email and password
3. **Dashboard** - View your attendance, leaves, and profile
4. **Apply Leave**:
   - Select leave type
   - Choose dates
   - Upload medical certificate for sick leave
5. **View Attendance** - Check your attendance history
6. **View Payslip** - See detailed salary breakdown

## 🔄 Database Migrations

If you need to update the database schema:

```bash
# Add salary components support
python migrate_salary_components.py

# Add user active status
python migrate_user_active_status.py

# Add payroll enhancements
python migrate_payroll_enhancements.py
```

## 📧 Configuration

### Email Settings (Optional)
To enable email notifications, configure SMTP settings in `app/__init__.py`:

```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'
```

### File Upload Settings
Configure in `app/__init__.py`:

```python
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
```

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database completely
python init_enhanced_db.py --reset
```

### Port Already in Use
```bash
# Run on different port
flask run --port 5001
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

## 🛠️ Development

### Running Tests
```bash
python test_system.py
```

### Debug Mode
Set in `run.py`:
```python
app.run(debug=True)
```

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributors

- Development Team

## 📞 Support

For issues and questions:
- Check documentation files
- Review error logs in the console
- Contact system administrator

## 🔄 Version History

### Version 2.0.0 (Current)
- ✅ Comprehensive salary component system
- ✅ Medical certificate upload for sick leave
- ✅ User activation/deactivation
- ✅ User deletion with cascade cleanup
- ✅ Auto-generated employee IDs
- ✅ Detailed payroll breakdown
- ✅ Unpaid leave deduction automation

### Version 1.0.0
- Basic HRMS functionality
- Employee, Attendance, Leave management
- Simple payroll system

## 🎯 Future Enhancements

- [ ] Email notifications
- [ ] Performance reviews
- [ ] Training management
- [ ] Asset management
- [ ] Expense tracking
- [ ] Reports and analytics
- [ ] Mobile application
- [ ] Multi-language support

---

**Made with ❤️ by the DayFlow Team**
