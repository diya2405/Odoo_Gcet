#!/usr/bin/env python3
"""
Database initialization script for Dayflow HRMS
Creates the database and sample data for testing
"""

import sys
import os
from datetime import date, datetime, timedelta
from decimal import Decimal

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def init_database():
    """Initialize database with sample data"""
    try:
        from app import app, db
        from app.models import User, Employee, Attendance, LeaveRequest, Payroll
        
        with app.app_context():
            print("🗄️  Creating database tables...")
            db.create_all()
            
            # Check if admin user already exists
            if User.query.filter_by(role='admin').first():
                print("ℹ️  Admin user already exists. Skipping sample data creation.")
                return True
            
            print("👤 Creating sample admin user...")
            # Create admin user
            admin_user = User(
                employee_id='ADMIN001',
                email='admin@dayflow.com',
                role='admin',
                is_verified=True
            )
            admin_user.set_password('Admin123!')
            
            db.session.add(admin_user)
            db.session.flush()
            
            # Create admin employee profile
            admin_employee = Employee(
                user_id=admin_user.id,
                first_name='System',
                last_name='Administrator',
                phone='+1-555-0100',
                address='123 Admin Street, City, State 12345',
                date_of_birth=date(1980, 1, 1),
                hire_date=date.today(),
                department='Administration',
                position='System Administrator',
                salary=Decimal('75000.00')
            )
            
            db.session.add(admin_employee)
            
            print("👥 Creating sample employee users...")
            # Create sample employee users
            employees_data = [
                {
                    'employee_id': 'EMP001',
                    'email': 'john.doe@dayflow.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'department': 'Engineering',
                    'position': 'Software Engineer',
                    'salary': Decimal('65000.00')
                },
                {
                    'employee_id': 'EMP002', 
                    'email': 'jane.smith@dayflow.com',
                    'first_name': 'Jane',
                    'last_name': 'Smith',
                    'department': 'Marketing',
                    'position': 'Marketing Manager',
                    'salary': Decimal('58000.00')
                },
                {
                    'employee_id': 'EMP003',
                    'email': 'bob.wilson@dayflow.com', 
                    'first_name': 'Bob',
                    'last_name': 'Wilson',
                    'department': 'Sales',
                    'position': 'Sales Representative',
                    'salary': Decimal('45000.00')
                }
            ]
            
            for emp_data in employees_data:
                # Create user
                user = User(
                    employee_id=emp_data['employee_id'],
                    email=emp_data['email'],
                    role='employee',
                    is_verified=True
                )
                user.set_password('Employee123!')
                
                db.session.add(user)
                db.session.flush()
                
                # Create employee profile
                employee = Employee(
                    user_id=user.id,
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    phone=f'+1-555-0{user.id:03d}',
                    address=f'12{user.id} Employee St, City, State 1234{user.id}',
                    date_of_birth=date(1985 + user.id, user.id % 12 + 1, 15),
                    hire_date=date.today() - timedelta(days=30 * user.id),
                    department=emp_data['department'],
                    position=emp_data['position'],
                    salary=emp_data['salary']
                )
                
                db.session.add(employee)
            
            db.session.commit()
            print("✅ Sample data created successfully!")
            
            # Print login information
            print("\n" + "="*50)
            print("🔐 LOGIN INFORMATION")
            print("="*50)
            print("Admin Login:")
            print("  Email: admin@dayflow.com")
            print("  Password: Admin123!")
            print()
            print("Employee Login (John Doe):")
            print("  Email: john.doe@dayflow.com")
            print("  Password: Employee123!")
            print()
            print("Employee Login (Jane Smith):")
            print("  Email: jane.smith@dayflow.com") 
            print("  Password: Employee123!")
            print("="*50)
            
            return True
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def main():
    print("🏢 DAYFLOW HRMS - DATABASE INITIALIZATION")
    print("="*50)
    
    success = init_database()
    
    if success:
        print("\n✅ Database initialization completed successfully!")
        print("\nYou can now run the application with: python app.py")
        print("Then visit: http://localhost:5000")
    else:
        print("\n❌ Database initialization failed!")
        print("Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()