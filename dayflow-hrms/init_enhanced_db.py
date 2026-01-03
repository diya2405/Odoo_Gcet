"""
Enhanced Database Initialization Script
Creates all tables and initializes default data including time off types
"""

from app import create_app, db
from app.models import (User, Employee, Attendance, LeaveRequest, Payroll,
                        SalaryComponent, TimeOffType, LeaveAllocation,
                        initialize_timeoff_types, create_salary_components_for_employee,
                        allocate_leave_for_employee)
from datetime import date, datetime
from decimal import Decimal

def init_enhanced_database():
    app = create_app()
    
    with app.app_context():
        print("Creating all database tables...")
        db.create_all()
        print("✓ Tables created successfully!")
        
        print("\nInitializing default time off types...")
        initialize_timeoff_types()
        print("✓ Time off types initialized!")
        
        # Check if admin already exists
        admin_user = User.query.filter_by(role='admin').first()
        
        if not admin_user:
            print("\nCreating default admin user...")
            
            # Create admin user with auto-generated ID
            admin_employee_id = User.generate_employee_id('OI', 'Admin', 'User', date.today().year)
            admin_password = 'Admin@123'  # Default password
            
            admin_user = User(
                employee_id=admin_employee_id,
                email='admin@dayflow.com',
                role='admin',
                is_verified=True,
                password_changed=False
            )
            admin_user.set_password(admin_password)
            
            db.session.add(admin_user)
            db.session.flush()
            
            # Create admin employee profile
            admin_employee = Employee(
                user_id=admin_user.id,
                first_name='Admin',
                last_name='User',
                phone='1234567890',
                personal_email='admin.personal@example.com',
                department='Administration',
                position='System Administrator',
                monthly_wage=Decimal('100000.00'),
                salary=Decimal('100000.00'),
                gender='Other',
                nationality='Indian',
                hire_date=date.today()
            )
            
            db.session.add(admin_employee)
            db.session.flush()
            
            # Create salary components for admin
            create_salary_components_for_employee(admin_employee.id, Decimal('100000.00'))
            
            # Allocate leaves for admin
            allocate_leave_for_employee(admin_employee.id)
            
            db.session.commit()
            
            print(f"✓ Admin user created!")
            print(f"  Employee ID: {admin_employee_id}")
            print(f"  Email: admin@dayflow.com")
            print(f"  Password: {admin_password}")
        else:
            print("\n✓ Admin user already exists")
        
        # Create a sample employee if none exist
        employee_count = Employee.query.filter(Employee.user.has(role='employee')).count()
        
        if employee_count == 0:
            print("\nCreating sample employee...")
            
            # Create sample employee with auto-generated ID
            emp_employee_id = User.generate_employee_id('OI', 'John', 'Doe', date.today().year)
            emp_password = User.generate_random_password()
            
            emp_user = User(
                employee_id=emp_employee_id,
                email='john.doe@dayflow.com',
                role='employee',
                is_verified=True,
                password_changed=False
            )
            emp_user.set_password(emp_password)
            
            db.session.add(emp_user)
            db.session.flush()
            
            # Create employee profile
            employee = Employee(
                user_id=emp_user.id,
                first_name='John',
                last_name='Doe',
                phone='9876543210',
                personal_email='john.personal@example.com',
                department='Engineering',
                position='Software Developer',
                monthly_wage=Decimal('50000.00'),
                salary=Decimal('50000.00'),
                gender='Male',
                marital_status='Single',
                nationality='Indian',
                hire_date=date.today(),
                bank_name='HDFC Bank',
                account_number='12345678901234',
                ifsc_code='HDFC0001234',
                pan_no='ABCDE1234F',
                uan_no='123456789012'
            )
            
            db.session.add(employee)
            db.session.flush()
            
            # Create salary components
            create_salary_components_for_employee(employee.id, Decimal('50000.00'))
            
            # Allocate leaves
            allocate_leave_for_employee(employee.id)
            
            db.session.commit()
            
            print(f"✓ Sample employee created!")
            print(f"  Employee ID: {emp_employee_id}")
            print(f"  Email: john.doe@dayflow.com")
            print(f"  Password: {emp_password}")
        else:
            print(f"\n✓ {employee_count} employee(s) already exist")
        
        print("\n" + "="*50)
        print("Database initialization completed successfully!")
        print("="*50)
        print("\nYou can now run the application with: python run.py")

if __name__ == '__main__':
    init_enhanced_database()
