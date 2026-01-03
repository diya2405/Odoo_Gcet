# Dayflow HRMS - Complete Feature Implementation

## Overview
This document outlines all the features implemented in the Dayflow Human Resource Management System based on the workflow diagram.

## Features Implemented

### 1. Auto-Generated Employee ID System ✅
**Format**: `[CompanyCode][FirstName][LastName][Year][SerialNumber]`
**Example**: `OIJODO20220001`

- Company Code: OI (Oddo India)
- First two letters of first and last name
- Year of joining
- Serial number (4 digits) based on joining order for that year

**Implementation**: 
- `User.generate_employee_id()` method in models.py
- Automatically generated when admin creates new employee

### 2. Auto-Generated Password System ✅
**Features**:
- System generates random secure password (10 characters)
- Contains mix of uppercase, lowercase, numbers, and special characters
- Admin receives password to share with employee
- `password_changed` flag tracks if employee changed initial password
- Employee must change password on first login

**Implementation**:
- `User.generate_random_password()` method in models.py
- Admin route `/employee/add` handles employee creation

### 3. Comprehensive Salary Components System ✅
**Components Automatically Calculated**:

#### Earnings:
1. **Basic Salary**: 50% of monthly wage
   - Example: If wage = ₹50,000, Basic = ₹25,000

2. **House Rent Allowance (HRA)**: 50% of basic salary
   - Example: If Basic = ₹25,000, HRA = ₹12,500

3. **Performance Bonus**: 8.33% of monthly wage
   - Variable amount defined by company

4. **Leave Travel Allowance (LTA)**: 8.33% of monthly wage
   - Covers employee travel expenses

5. **Standard/Fixed Allowance**: Remaining amount
   - Calculated to make total equal to monthly wage

#### Deductions:
1. **Provident Fund (PF)**: 12% of basic salary
   - Mandatory contribution

2. **Professional Tax**: Fixed ₹200
   - Statutory deduction

**Features**:
- All components auto-calculate based on monthly wage
- Supports both percentage-based and fixed amount calculations
- Can be customized per employee
- Validates total doesn't exceed defined wage

**Database Tables**:
- `SalaryComponent` model stores each component
- Linked to employee profile
- Computation type: 'percentage' or 'fixed'
- Component type: 'earning' or 'deduction'

### 4. Time Off/Leave Management System ✅
**Time Off Types**:
1. **Paid Time Off (PTO)**: 24 days/year
2. **Sick Leave**: 7 days/year (requires medical certificate)
3. **Unpaid Leave**: No fixed allocation

**Features**:
- Allocation tracking per employee per year
- Leave balance calculation (allocated - used - pending)
- Certificate upload for sick leave
- Approval workflow (pending → approved/rejected)
- Admin can approve/reject with comments
- Employees can view their leave balance

**Database Tables**:
- `TimeOffType` model for leave types
- `LeaveAllocation` model for employee leave balance
- `LeaveRequest` model for leave applications

### 5. Enhanced Attendance System ✅
**Features**:
- **Check In/Check Out**: Employees can mark attendance
- **Break Time Tracking**: Records break duration
- **Work Hours Calculation**: Auto-calculates hours worked (excluding breaks)
- **Status Indicators**:
  - 🟢 Green dot: Present in office
  - 🟡 Yellow dot: Absent (no time off applied)
  - ✈️ Airplane icon: On approved leave

**Work Hours Calculation**:
```
Hours Worked = (Check Out Time - Check In Time) - Break Time
```

**Attendance Status**:
- `present`: Employee checked in
- `absent`: Not present, no leave
- `half_day`: Partial attendance
- `leave`: On approved leave

### 6. Enhanced Employee Profile ✅
**Personal Information**:
- First Name, Last Name
- Date of Birth
- Gender (Male, Female, Other)
- Marital Status (Single, Married, Divorced, Widowed)
- Nationality (default: Indian)
- Phone, Personal Email
- Residing Address

**Professional Information**:
- Department
- Job Position
- Manager (hierarchical relationship)
- Skills (comma-separated or JSON)
- Certifications
- Resume upload
- Date of Joining

**Government IDs**:
- PAN Number
- UAN Number (Universal Account Number)

**Bank Details**:
- Bank Name
- Account Number
- IFSC Code

**Work Schedule**:
- Monthly Wage
- Working Hours per Day (default: 8)
- Working Days per Week (default: 5)

**Additional**:
- Profile Picture
- "What I love about my job" (interests field)
- "My interests and hobbies"

### 7. Enhanced Payroll System ✅
**Features**:
- **Automatic Calculation** based on:
  - Attendance days present
  - Salary components (earnings & deductions)
  - Unpaid leave deductions
  - Overtime hours and rate

**Payroll Components**:
- Basic Salary
- HRA
- Standard Allowance
- Performance Bonus
- LTA
- Fixed Allowance
- Provident Fund Deduction
- Professional Tax
- Other Deductions

**Calculation Logic**:
```
Gross Pay = Sum of all earnings + overtime pay
Total Deductions = PF + Professional Tax + Other Deductions
Unpaid Leave Deduction = (Gross Pay / Total Working Days) × Unpaid Leave Days
Net Pay = Gross Pay - Total Deductions - Unpaid Leave Deduction
```

**Features**:
- Attendance-based payroll calculation
- Automatic unpaid leave adjustment
- Days present tracking
- Payslip generation

### 8. Admin Features ✅
**Employee Management**:
- View all employees with status indicators
- Add new employees (auto-generates ID & password)
- Edit employee details
- View employee complete profile
- Access salary information (restricted to admin)

**Attendance Management**:
- View all employee attendance
- Day-wise attendance view
- Mark attendance for employees
- Attendance statistics

**Leave Management**:
- View all leave requests
- Approve/Reject leave requests
- Add admin comments
- View leave allocation status

**Payroll Management**:
- Generate payroll for employees
- View payroll history
- Process bulk payroll
- Mark payroll as paid

**Dashboard**:
- Total employees count
- Present/Absent/On Leave statistics
- Pending leave requests count
- Department-wise summary
- Recent activity feed

### 9. Employee Features ✅
**Dashboard**:
- Today's attendance status
- Check In/Check Out buttons
- Recent attendance (last 7 days)
- Pending leave requests count
- Approved leaves this month
- Total hours worked this month
- Latest payroll information

**My Profile**:
- View complete profile
- Edit personal details
- Update profile picture
- View salary components
- View bank details
- View skills and certifications

**Attendance**:
- View attendance records
- Check In/Check Out functionality
- Monthly attendance statistics
- Hours worked tracking

**Time Off**:
- View leave balance
- Apply for leave
- Upload certificate (for sick leave)
- Track leave request status
- View leave history

**Payroll**:
- View payroll history
- Download payslips
- View salary breakdown

### 10. Security Features ✅
**User Authentication**:
- Secure password hashing
- Password complexity requirements
- Email verification
- Role-based access control (Admin/Employee)

**Access Control**:
- Admin-only routes protected
- Employee can only view their own data
- Salary information restricted to admin

**Password Policy**:
- Minimum 8 characters
- Must contain uppercase letter
- Must contain lowercase letter
- Must contain number
- Force password change on first login

### 11. Status Indicator System ✅
**Real-time Status Display**:
- Dynamically calculated based on current date
- Visual indicators on dashboard cards
- Color-coded for easy identification

**Status Logic**:
```python
if employee.has_approved_leave_today():
    status = 'on_leave' (✈️ Airplane icon)
elif employee.attendance_today.status == 'present':
    status = 'present' (🟢 Green dot)
else:
    status = 'absent' (🟡 Yellow dot)
```

### 12. Database Schema ✅
**Tables Created**:
1. `users` - User authentication
2. `employees` - Employee profiles
3. `attendance` - Attendance records
4. `timeoff_types` - Leave type definitions
5. `leave_allocations` - Employee leave balance
6. `leave_requests` - Leave applications
7. `salary_components` - Salary structure
8. `payroll` - Payroll records

**Relationships**:
- User ↔ Employee (One-to-One)
- Employee ↔ Manager (Self-referential)
- Employee ↔ Attendance (One-to-Many)
- Employee ↔ LeaveRequest (One-to-Many)
- Employee ↔ SalaryComponent (One-to-Many)
- Employee ↔ LeaveAllocation (One-to-Many)
- TimeOffType ↔ LeaveRequest (One-to-Many)

## Setup Instructions

### 1. Install Dependencies
```bash
cd dayflow-hrms
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_enhanced_db.py
```

This will:
- Create all database tables
- Initialize time off types (PTO, Sick, Unpaid)
- Create default admin user
- Create sample employee
- Setup salary components
- Allocate leaves

### 3. Default Credentials
**Admin**:
- Email: admin@dayflow.com
- Password: Admin@123
- Employee ID: Auto-generated (e.g., OIADUS2026001)

**Sample Employee**:
- Email: john.doe@dayflow.com
- Password: Auto-generated (displayed after init)
- Employee ID: Auto-generated (e.g., OIJODO2026001)

### 4. Run Application
```bash
python run.py
```

Visit: http://localhost:5000

## Configuration

### Company Settings
Edit in `admin.py`:
```python
company_code = "OI"  # Change to your company code
```

### Salary Component Defaults
Edit in `models.py` → `create_salary_components_for_employee()`:
- Basic Salary percentage
- HRA percentage
- Performance Bonus percentage
- LTA percentage
- PF percentage
- Professional Tax amount

### Time Off Allocations
Edit in `models.py` → `initialize_timeoff_types()`:
- Default PTO days
- Default sick leave days
- Add custom leave types

## Usage Workflow

### Admin Workflow:
1. Login with admin credentials
2. Add new employees (system generates ID & password)
3. Share credentials with employee
4. Monitor employee attendance
5. Review and approve leave requests
6. Generate monthly payroll
7. View department statistics

### Employee Workflow:
1. Login with credentials
2. Change password on first login
3. Check In at start of day
4. Check Out at end of day
5. Apply for leave when needed
6. View attendance records
7. Check payroll and salary breakdown
8. Update profile information

## Features Summary

✅ Auto-generated Employee IDs
✅ Auto-generated Passwords
✅ Comprehensive Salary Components
✅ Tax Deductions (PF, Professional Tax)
✅ Time Off Types (PTO, Sick, Unpaid)
✅ Leave Allocation & Balance Tracking
✅ Attendance Check-In/Check-Out
✅ Break Time Tracking
✅ Status Indicators (Green/Yellow/Airplane)
✅ Enhanced Employee Profile
✅ Bank Details & Government IDs
✅ Skills & Certifications
✅ Manager Hierarchy
✅ Payroll Auto-calculation
✅ Attendance-based Salary Adjustment
✅ Leave Certificate Upload
✅ Approval Workflow
✅ Role-based Access Control
✅ Dashboard Analytics
✅ Department-wise Statistics

## Next Steps (Future Enhancements)

1. **Email Notifications**: Send credentials to new employees
2. **Password Reset**: Email-based password reset
3. **Biometric Integration**: Hardware attendance devices
4. **Mobile App**: Check-in via mobile
5. **Reports**: PDF export of payslips, attendance
6. **Analytics**: Advanced charts and insights
7. **Shift Management**: Multiple shift support
8. **Overtime Approval**: Workflow for overtime requests
9. **Document Management**: Central repository
10. **Performance Reviews**: Annual review system

## Support

For issues or questions, refer to:
- `README.md` - Basic setup guide
- `models.py` - Database schema
- `routes/` - API endpoints
- This document - Feature details

---
**Dayflow HRMS** - Complete Human Resource Management Solution
Version: 2.0 Enhanced
Last Updated: January 2026
