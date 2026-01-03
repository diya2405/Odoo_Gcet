# Quick Start Guide - Dayflow HRMS

## 🚀 Getting Started (5 Minutes)

### Step 1: Setup (2 minutes)
```bash
cd dayflow-hrms
pip install -r requirements.txt
python init_enhanced_db.py
```

### Step 2: Run Application (1 minute)
```bash
python run.py
```
Visit: http://localhost:5000

### Step 3: Login (1 minute)
**Admin**: admin@dayflow.com / Admin@123

### Step 4: Add First Employee (1 minute)
1. Click "Employees" → "Add Employee"
2. Fill in: Name, Email, Department, Monthly Wage
3. Copy generated Employee ID & Password
4. Share with employee

---

## 📋 Admin Quick Actions

### Add New Employee
**Route**: Employees → Add Employee

**Required Fields**:
- First Name
- Last Name
- Email
- Monthly Wage (e.g., 50000)

**Optional Fields**:
- Phone, Department, Position
- Date of Birth, Gender
- Bank Details, PAN, UAN

**System Auto-Generates**:
- ✅ Employee ID (e.g., OIJODO20220001)
- ✅ Secure Password (show to employee)
- ✅ Salary Components (Basic, HRA, Bonus, etc.)
- ✅ Leave Allocation (PTO 24 days, Sick 7 days)

### Approve Leave Requests
**Route**: Leave Requests → Pending

**Actions**:
1. Click on request
2. Review details
3. Add comment (optional)
4. Click "Approve" or "Reject"

### View Employee Status
**Dashboard** shows real-time status:
- 🟢 Green = Present
- 🟡 Yellow = Absent
- ✈️ Airplane = On Leave

### Generate Payroll
**Route**: Payroll → Generate

**System Calculates**:
- Days present (from attendance)
- All salary components
- Tax deductions
- Unpaid leave adjustments
- Net pay

---

## 👤 Employee Quick Actions

### First Login
1. Login with provided credentials
2. **Change Password** immediately
3. Update profile information

### Daily Check-in/Check-out
**Dashboard** → Check In / Check Out buttons

### Apply for Leave
**Route**: Time Off → Apply Leave

**Steps**:
1. Select leave type
2. Choose dates
3. Enter reason
4. Upload certificate (if sick leave)
5. Submit

### View Payroll
**Route**: Payroll → My Payroll

Shows:
- Salary breakdown
- Deductions
- Net pay
- Payment history

---

## 💰 Salary Component Example

### For ₹50,000 Monthly Wage:

**Earnings**:
- Basic: ₹25,000 (50%)
- HRA: ₹12,500 (50% of basic)
- Performance Bonus: ₹4,165 (8.33%)
- LTA: ₹4,165 (8.33%)
- Standard Allowance: ₹4,170
- **Gross**: ₹50,000

**Deductions**:
- PF: ₹3,000 (12% of basic)
- Professional Tax: ₹200
- **Net**: ₹46,800

---

## 📅 Leave Types

### 1. Paid Time Off (PTO)
- **Allocation**: 24 days/year
- **Certificate**: Not required
- **Salary**: Paid

### 2. Sick Leave
- **Allocation**: 7 days/year
- **Certificate**: Required
- **Salary**: Paid

### 3. Unpaid Leave
- **Allocation**: Unlimited
- **Certificate**: Not required
- **Salary**: Deducted

---

## 🔧 Common Tasks

### Change Company Code
**File**: `app/routes/admin.py`
```python
company_code = "OI"  # Change this
```

### Modify Salary Components
**File**: `app/models.py` → `create_salary_components_for_employee()`

Change percentages:
- Basic: 50% (line ~420)
- HRA: 50% of basic (line ~427)
- Performance Bonus: 8.33% (line ~433)
- PF: 12% (line ~444)

### Add Custom Leave Type
**File**: `app/models.py` → `initialize_timeoff_types()`

Add new entry:
```python
{
    'name': 'Maternity Leave',
    'code': 'MAT',
    'description': 'Maternity leave',
    'is_paid': True,
    'requires_certificate': True,
    'default_allocation': 90,
    'color': '#ff69b4'
}
```

---

## 🐛 Troubleshooting

### "Cannot connect to database"
```bash
# Check MySQL is running
mysql -u root -p

# Create database
CREATE DATABASE dayflow_db;
```

### "Module not found"
```bash
pip install -r requirements.txt --upgrade
```

### "Admin not found"
```bash
# Re-run initialization
python init_enhanced_db.py
```

### "Cannot login"
- Clear browser cookies
- Check credentials: admin@dayflow.com / Admin@123
- Verify database was initialized

---

## 📊 Database Tables

**Core Tables**:
1. users - Authentication
2. employees - Profile data
3. attendance - Daily records
4. timeoff_types - Leave types
5. leave_allocations - Leave balance
6. leave_requests - Leave applications
7. salary_components - Salary structure
8. payroll - Payment records

---

## 🔐 Security Checklist

- ✅ Change admin password after first login
- ✅ Use strong passwords for all users
- ✅ Enable email verification (future)
- ✅ Regular database backups
- ✅ Keep dependencies updated
- ✅ Don't share credentials in plain text

---

## 📞 Support

**Documentation**:
- FEATURE_IMPLEMENTATION.md - Complete features
- README_ENHANCED.md - Setup guide
- IMPLEMENTATION_SUMMARY.md - Implementation status

**Code**:
- `app/models.py` - Database models
- `app/routes/` - Application routes
- `init_enhanced_db.py` - Database setup

---

## ✅ Feature Checklist

All features from workflow implemented:
- ✅ Auto-generated Employee IDs
- ✅ Auto-generated Passwords
- ✅ Salary Components (Basic, HRA, Bonus, LTA)
- ✅ Tax Deductions (PF, Professional Tax)
- ✅ Check-in/Check-out Attendance
- ✅ Time Off Types (PTO, Sick, Unpaid)
- ✅ Leave Balance Tracking
- ✅ Status Indicators (🟢🟡✈️)
- ✅ Enhanced Employee Profiles
- ✅ Payroll Generation

---

**Quick Start Complete!** 🎉

You're ready to use Dayflow HRMS with all features from the workflow diagram.
