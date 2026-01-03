# Database Reset Guide

## When to Reset Database

Reset the database when you encounter errors like:
```
sqlalchemy.exc.OperationalError: no such column: users.password_changed
```

This happens when the database schema is outdated and doesn't match the updated models.

## How to Reset Database

### Step 1: Stop the Application
Make sure Flask is not running. Press `Ctrl+C` in the terminal or:

```powershell
Get-Process python | Stop-Process -Force
```

### Step 2: Delete Old Database
```powershell
cd "c:\Users\VICTUS\Downloads\geminioddo\dayflow-hrms"
Remove-Item -Path "instance\dayflow_hrms.db" -Force
```

### Step 3: Initialize New Database
```powershell
python init_enhanced_db.py
```

This will:
- ✅ Create all tables with new schema
- ✅ Initialize time off types (PTO, Sick, Unpaid)
- ✅ Create admin user
- ✅ Create sample employee
- ✅ Setup salary components
- ✅ Allocate leaves

### Step 4: Note the Credentials
After initialization, you'll see:

**Admin Account**:
- Employee ID: OIADUS20260001 (or similar)
- Email: admin@dayflow.com
- Password: Admin@123

**Sample Employee**:
- Employee ID: OIJODO20260001 (or similar)  
- Email: john.doe@dayflow.com
- Password: (auto-generated, displayed in terminal)

### Step 5: Run the Application
```powershell
python run.py
```

Visit: http://localhost:5000

## Quick Reset (One Command)

```powershell
cd "c:\Users\VICTUS\Downloads\geminioddo\dayflow-hrms"; Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force; Start-Sleep -Seconds 2; Remove-Item -Path "instance\dayflow_hrms.db" -Force -ErrorAction SilentlyContinue; python init_enhanced_db.py; python run.py
```

## Troubleshooting

### "File is being used by another process"
**Solution**: Stop all Python processes first
```powershell
Get-Process python | Stop-Process -Force
Start-Sleep -Seconds 3
Remove-Item -Path "instance\dayflow_hrms.db" -Force
```

### "Module not found" errors
**Solution**: Reinstall dependencies
```powershell
pip install -r requirements.txt --upgrade
```

### Tables not created properly
**Solution**: Make sure database file is completely deleted before running init script
```powershell
Get-ChildItem -Recurse -Include "*.db" | Remove-Item -Force
python init_enhanced_db.py
```

## What Gets Created

### Database Tables:
1. `users` - Authentication (with password_changed field)
2. `employees` - Enhanced profiles (with 20+ fields)
3. `attendance` - Daily records (with break_time)
4. `timeoff_types` - Leave types (PTO, Sick, Unpaid)
5. `leave_allocations` - Employee leave balance
6. `leave_requests` - Leave applications
7. `salary_components` - Salary structure
8. `payroll` - Payroll records

### Default Data:
- 3 Time Off Types
- 1 Admin user
- 1 Sample employee
- Salary components for all employees
- Leave allocations for current year

## Verify Successful Initialization

After running `init_enhanced_db.py`, you should see:
```
✓ Tables created successfully!
✓ Time off types initialized!
✓ Admin user created!
✓ Sample employee created!
==================================================
Database initialization completed successfully!
==================================================
```

## Login and Test

1. Visit: http://localhost:5000
2. Login with: admin@dayflow.com / Admin@123
3. Navigate to Employees → Add Employee
4. System should auto-generate Employee ID and Password
5. Check that all new fields are available

---

**Note**: Resetting the database will delete all existing data. In production, use database migrations instead.
