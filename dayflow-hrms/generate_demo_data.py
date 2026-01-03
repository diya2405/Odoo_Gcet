"""
Generate comprehensive demo data for DayFlow HRMS
- 15 employees with realistic details
- Attendance data (10 employees for 1 month, 5 employees for 3 months)
- 6 leave requests (2 sick, 1 paid, 3 unpaid)
- Payroll data for all employees
"""
import sys
import os
from datetime import datetime, date, time, timedelta
from decimal import Decimal
import random

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Employee, Attendance, LeaveRequest, Payroll, SalaryComponent

# Sample data
FIRST_NAMES = ['Rahul', 'Priya', 'Amit', 'Sneha', 'Vikram', 'Anjali', 'Rohan', 'Kavita', 
               'Arjun', 'Neha', 'Karan', 'Divya', 'Sanjay', 'Pooja', 'Aditya']
LAST_NAMES = ['Sharma', 'Kumar', 'Singh', 'Patel', 'Gupta', 'Verma', 'Agarwal', 'Joshi', 
              'Reddy', 'Nair', 'Desai', 'Mehta', 'Rao', 'Iyer', 'Chauhan']
DEPARTMENTS = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']
POSITIONS = {
    'Engineering': ['Software Engineer', 'Senior Developer', 'Tech Lead'],
    'Sales': ['Sales Executive', 'Sales Manager', 'Business Development'],
    'Marketing': ['Marketing Executive', 'Content Writer', 'Digital Marketer'],
    'HR': ['HR Executive', 'HR Manager', 'Recruiter'],
    'Finance': ['Accountant', 'Finance Manager', 'Financial Analyst'],
    'Operations': ['Operations Manager', 'Operations Executive', 'Operations Analyst']
}

def generate_employees(count=15):
    """Generate employees with realistic data"""
    print(f"\n📝 Generating {count} employees...")
    
    employees = []
    used_names = set()
    
    for i in range(count):
        # Generate unique name combination
        while True:
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        department = random.choice(DEPARTMENTS)
        position = random.choice(POSITIONS[department])
        
        # Generate hire date (between 6 months to 3 years ago)
        days_ago = random.randint(180, 1095)
        hire_date = date.today() - timedelta(days=days_ago)
        hire_year = hire_date.year
        
        # Generate employee ID
        employee_id = User.generate_employee_id('OI', first_name, last_name, hire_year)
        email = f"{first_name.lower()}.{last_name.lower()}@dayflow.com"
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"  ⏭ Employee {full_name} already exists, skipping...")
            employees.append(existing_user.employee_profile)
            continue
        
        # Create User
        user = User(
            employee_id=employee_id,
            email=email,
            role='employee' if i > 0 else 'admin',  # First one is admin
            is_verified=True,
            is_active=True,
            password_changed=True
        )
        user.set_password('Password@123')
        db.session.add(user)
        db.session.flush()
        
        # Generate salary based on position
        base_salaries = {
            'Software Engineer': 60000,
            'Senior Developer': 90000,
            'Tech Lead': 120000,
            'Sales Executive': 45000,
            'Sales Manager': 80000,
            'Business Development': 55000,
            'Marketing Executive': 50000,
            'Content Writer': 40000,
            'Digital Marketer': 55000,
            'HR Executive': 45000,
            'HR Manager': 70000,
            'Recruiter': 50000,
            'Accountant': 50000,
            'Finance Manager': 85000,
            'Financial Analyst': 65000,
            'Operations Manager': 75000,
            'Operations Executive': 50000,
            'Operations Analyst': 55000
        }
        
        monthly_wage = base_salaries.get(position, 50000)
        
        # Create Employee Profile
        employee = Employee(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            phone=f"+91-{random.randint(7000000000, 9999999999)}",
            personal_email=f"{first_name.lower()}{random.randint(1, 99)}@gmail.com",
            address=f"{random.randint(1, 999)}, {random.choice(['MG Road', 'Brigade Road', 'Whitefield', 'Indiranagar', 'Koramangala'])}, Bangalore",
            date_of_birth=date(random.randint(1985, 2000), random.randint(1, 12), random.randint(1, 28)),
            hire_date=hire_date,
            department=department,
            position=position,
            gender=random.choice(['Male', 'Female']),
            marital_status=random.choice(['Single', 'Married']),
            nationality='Indian',
            pan_no=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))}{random.randint(1000, 9999)}{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=1))}",
            bank_name=random.choice(['HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank', 'Kotak Mahindra']),
            account_number=f"{random.randint(10000000000, 99999999999)}",
            ifsc_code=f"{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))}0{random.randint(100000, 999999)}",
            monthly_wage=monthly_wage,
            salary=monthly_wage,
            working_hours_per_day=8.0,
            working_days_per_week=5,
            emergency_contact_name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            emergency_contact_phone=f"+91-{random.randint(7000000000, 9999999999)}",
            emergency_contact_relationship=random.choice(['Father', 'Mother', 'Spouse', 'Brother', 'Sister'])
        )
        db.session.add(employee)
        employees.append(employee)
        
        print(f"  ✅ Created: {full_name} ({employee_id}) - {position} in {department}")
    
    db.session.commit()
    print(f"✅ Successfully created {len(employees)} employees")
    return employees


def generate_salary_components(employee):
    """Generate salary components for an employee"""
    base_salary = float(employee.monthly_wage) * 0.50
    
    components = [
        {'name': 'Basic Salary', 'type': 'earning', 'comp_type': 'fixed', 'value': base_salary},
        {'name': 'HRA', 'type': 'earning', 'comp_type': 'percentage', 'value': 50, 'base': 'Basic Salary', 'amount': base_salary * 0.50},
        {'name': 'Transport Allowance', 'type': 'earning', 'comp_type': 'fixed', 'value': 1600},
        {'name': 'Special Allowance', 'type': 'earning', 'comp_type': 'fixed', 'value': float(employee.monthly_wage) - base_salary - (base_salary * 0.50) - 1600 - 1800},
        {'name': 'PF Deduction', 'type': 'deduction', 'comp_type': 'percentage', 'value': 12, 'base': 'Basic Salary', 'amount': base_salary * 0.12},
        {'name': 'Professional Tax', 'type': 'deduction', 'comp_type': 'fixed', 'value': 200},
    ]
    
    for comp in components:
        component = SalaryComponent(
            employee_id=employee.id,
            component_name=comp['name'],
            component_type=comp['type'],
            computation_type=comp['comp_type'],
            value=comp['value'],
            base_component=comp.get('base'),
            calculated_amount=comp.get('amount', comp['value']),
            is_active=True
        )
        db.session.add(component)


def generate_attendance_data(employees):
    """Generate attendance data for employees"""
    print("\n📅 Generating attendance data...")
    
    today = date.today()
    
    # 10 employees with 1 month data
    for i, employee in enumerate(employees[:10]):
        start_date = today - timedelta(days=30)
        print(f"  📋 Generating 1 month attendance for {employee.full_name}...")
        
        current_date = start_date
        while current_date <= today:
            # Skip weekends (Saturday=5, Sunday=6)
            if current_date.weekday() < 5:  # Monday=0 to Friday=4
                # 95% attendance probability
                if random.random() < 0.95:
                    check_in_hour = random.randint(8, 10)
                    check_in_minute = random.randint(0, 59)
                    check_out_hour = random.randint(17, 19)
                    check_out_minute = random.randint(0, 59)
                    
                    attendance = Attendance(
                        employee_id=employee.id,
                        date=current_date,
                        check_in_time=time(check_in_hour, check_in_minute),
                        check_out_time=time(check_out_hour, check_out_minute),
                        break_time=1.0,
                        status='present',
                        work_location=random.choice(['Office', 'Remote', 'Office', 'Office']),
                        remarks='Regular working day'
                    )
                    attendance.calculate_hours_worked()
                    db.session.add(attendance)
            
            current_date += timedelta(days=1)
    
    # 5 employees with 3 months data
    for employee in employees[10:15]:
        start_date = today - timedelta(days=90)
        print(f"  📋 Generating 3 months attendance for {employee.full_name}...")
        
        current_date = start_date
        while current_date <= today:
            # Skip weekends
            if current_date.weekday() < 5:
                # 93% attendance probability
                if random.random() < 0.93:
                    check_in_hour = random.randint(8, 10)
                    check_in_minute = random.randint(0, 59)
                    check_out_hour = random.randint(17, 19)
                    check_out_minute = random.randint(0, 59)
                    
                    attendance = Attendance(
                        employee_id=employee.id,
                        date=current_date,
                        check_in_time=time(check_in_hour, check_in_minute),
                        check_out_time=time(check_out_hour, check_out_minute),
                        break_time=1.0,
                        status='present',
                        work_location=random.choice(['Office', 'Remote', 'Office', 'Office']),
                        remarks='Regular working day'
                    )
                    attendance.calculate_hours_worked()
                    db.session.add(attendance)
            
            current_date += timedelta(days=1)
    
    db.session.commit()
    print("✅ Attendance data generated successfully")


def generate_leave_requests(employees):
    """Generate 6 leave requests: 2 sick, 1 paid, 3 unpaid"""
    print("\n🏖 Generating leave requests...")
    
    today = date.today()
    
    # Select 6 random employees
    selected_employees = random.sample(employees, 6)
    
    leave_data = [
        # 2 Sick leaves
        {
            'employee': selected_employees[0],
            'type': 'sick',
            'duration': 3,
            'status': 'approved',
            'reason': 'Suffering from viral fever and body ache. Doctor advised rest.',
            'has_certificate': True
        },
        {
            'employee': selected_employees[1],
            'type': 'sick',
            'duration': 2,
            'status': 'pending',
            'reason': 'Severe headache and unable to work.',
            'has_certificate': False
        },
        # 1 Paid leave
        {
            'employee': selected_employees[2],
            'type': 'paid',
            'duration': 5,
            'status': 'approved',
            'reason': 'Planning family vacation to Goa.',
            'has_certificate': False
        },
        # 3 Unpaid leaves
        {
            'employee': selected_employees[3],
            'type': 'unpaid',
            'duration': 7,
            'status': 'approved',
            'reason': 'Personal family matter - need to travel to hometown urgently.',
            'has_certificate': False
        },
        {
            'employee': selected_employees[4],
            'type': 'unpaid',
            'duration': 4,
            'status': 'rejected',
            'reason': 'Extended weekend trip.',
            'has_certificate': False
        },
        {
            'employee': selected_employees[5],
            'type': 'unpaid',
            'duration': 10,
            'status': 'pending',
            'reason': 'Wedding ceremony in family.',
            'has_certificate': False
        },
    ]
    
    for idx, leave_info in enumerate(leave_data):
        # Generate random dates (some past, some future)
        if idx < 3:  # First 3 are in the past
            start_date = today - timedelta(days=random.randint(5, 20))
        else:  # Last 3 are upcoming
            start_date = today + timedelta(days=random.randint(1, 15))
        
        end_date = start_date + timedelta(days=leave_info['duration'] - 1)
        
        leave_request = LeaveRequest(
            employee_id=leave_info['employee'].id,
            leave_type=leave_info['type'],
            start_date=start_date,
            end_date=end_date,
            reason=leave_info['reason'],
            status=leave_info['status'],
            days_requested=leave_info['duration'],
            certificate_path='uploads/medical_certificates/sample_cert.pdf' if leave_info['has_certificate'] else None,
            admin_comment='Approved as per company policy' if leave_info['status'] == 'approved' else (
                'Rejected due to project deadline' if leave_info['status'] == 'rejected' else None
            )
        )
        db.session.add(leave_request)
        
        print(f"  ✅ Created {leave_info['type'].upper()} leave for {leave_info['employee'].full_name} "
              f"({leave_info['duration']} days, {leave_info['status']})")
    
    db.session.commit()
    print("✅ Leave requests generated successfully")


def generate_payroll_data(employees):
    """Generate payroll data for all employees"""
    print("\n💰 Generating payroll data...")
    
    # Generate for current month and previous month
    months = [
        (date(2026, 1, 1), date(2026, 1, 31), 'January 2026'),
        (date(2025, 12, 1), date(2025, 12, 31), 'December 2025'),
    ]
    
    for pay_period_start, pay_period_end, month_name in months:
        print(f"\n  📊 Creating payroll for {month_name}...")
        
        for employee in employees:
            # Check if payroll already exists
            existing = Payroll.query.filter_by(
                employee_id=employee.id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end
            ).first()
            
            if existing:
                print(f"    ⏭ Payroll exists for {employee.full_name}")
                continue
            
            # Get salary components
            components = SalaryComponent.query.filter_by(
                employee_id=employee.id,
                is_active=True
            ).all()
            
            if not components:
                # Generate components if not exist
                generate_salary_components(employee)
                db.session.commit()
                components = SalaryComponent.query.filter_by(
                    employee_id=employee.id,
                    is_active=True
                ).all()
            
            # Calculate working days and present days
            total_working_days = 22  # Standard working days
            
            # Get attendance count for the month
            days_present = Attendance.query.filter(
                Attendance.employee_id == employee.id,
                Attendance.date >= pay_period_start,
                Attendance.date <= pay_period_end,
                Attendance.status == 'present'
            ).count()
            
            if days_present == 0:
                days_present = total_working_days  # Default to full month if no attendance data
            
            # Get paid and unpaid leave days
            paid_leave_days = LeaveRequest.query.filter(
                LeaveRequest.employee_id == employee.id,
                LeaveRequest.status == 'approved',
                LeaveRequest.leave_type.in_(['paid', 'sick']),
                LeaveRequest.start_date <= pay_period_end,
                LeaveRequest.end_date >= pay_period_start
            ).with_entities(db.func.sum(LeaveRequest.days_requested)).scalar() or 0
            
            unpaid_leave_days = LeaveRequest.query.filter(
                LeaveRequest.employee_id == employee.id,
                LeaveRequest.status == 'approved',
                LeaveRequest.leave_type == 'unpaid',
                LeaveRequest.start_date <= pay_period_end,
                LeaveRequest.end_date >= pay_period_start
            ).with_entities(db.func.sum(LeaveRequest.days_requested)).scalar() or 0
            
            # Calculate salary components
            base_monthly_salary = float(employee.monthly_wage)
            basic_salary = base_monthly_salary * 0.50
            hra = basic_salary * 0.50
            standard_allowance = 1600.00
            fixed_allowance = base_monthly_salary - basic_salary - hra - standard_allowance - 1800
            
            # Calculate deductions
            pf_deduction = basic_salary * 0.12
            professional_tax = 200.00
            
            # Create payroll record
            payroll = Payroll(
                employee_id=employee.id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end,
                base_monthly_salary=Decimal(str(base_monthly_salary)),
                basic_salary=Decimal(str(basic_salary)),
                hra=Decimal(str(hra)),
                standard_allowance=Decimal(str(standard_allowance)),
                fixed_allowance=Decimal(str(fixed_allowance)),
                allowances=Decimal('0.00'),
                performance_bonus=Decimal('0.00'),
                lta=Decimal('0.00'),
                increment_amount=Decimal('0.00'),
                increment_percentage=Decimal('0.00'),
                special_bonus=Decimal('0.00'),
                festival_bonus=Decimal('0.00'),
                other_earnings=Decimal('0.00'),
                pf_deduction=Decimal(str(pf_deduction)),
                professional_tax=Decimal(str(professional_tax)),
                deductions=Decimal('0.00'),
                tax_deductions=Decimal('0.00'),
                unpaid_leave_deduction=Decimal('0.00'),
                overtime_hours=0.0,
                overtime_rate=Decimal('0.00'),
                total_working_days=total_working_days,
                days_present=days_present,
                paid_leave_days=int(paid_leave_days),
                unpaid_leave_days=int(unpaid_leave_days),
                payment_date=pay_period_end + timedelta(days=5),
                payment_status='paid' if pay_period_end < date.today() else 'pending'
            )
            
            # Calculate all values
            payroll.calculate_net_pay()
            
            db.session.add(payroll)
            print(f"    ✅ Created payroll for {employee.full_name}: ₹{payroll.net_pay:,.2f}")
        
        db.session.commit()
    
    print("\n✅ Payroll data generated successfully")


def main():
    """Main function to generate all demo data"""
    app = create_app()
    
    with app.app_context():
        print("="*60)
        print("     DayFlow HRMS - Demo Data Generator")
        print("="*60)
        
        try:
            # Generate employees
            employees = generate_employees(15)
            
            # Generate attendance data
            generate_attendance_data(employees)
            
            # Generate leave requests
            generate_leave_requests(employees)
            
            # Generate payroll data
            generate_payroll_data(employees)
            
            print("\n" + "="*60)
            print("     ✅ ALL DEMO DATA GENERATED SUCCESSFULLY!")
            print("="*60)
            print("\n📊 Summary:")
            print(f"   • Employees: {len(employees)}")
            print(f"   • Attendance records: Generated for all employees")
            print(f"   • Leave requests: 6 (2 sick, 1 paid, 3 unpaid)")
            print(f"   • Payroll records: Created for Jan & Dec")
            print("\n🔐 Login Credentials:")
            print(f"   • Admin Email: {employees[0].user.email}")
            print(f"   • Password: Password@123")
            print(f"   • All employee accounts use the same password")
            print("\n" + "="*60)
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


if __name__ == '__main__':
    main()
