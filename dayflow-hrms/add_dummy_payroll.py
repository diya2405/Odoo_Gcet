"""
Add dummy payroll data for testing
"""
import sys
import os
from datetime import datetime, date
from decimal import Decimal

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Payroll, Employee, SalaryComponent

def add_dummy_payroll():
    """Add sample payroll records"""
    app = create_app()
    
    with app.app_context():
        # Get all employees
        employees = Employee.query.all()
        
        if not employees:
            print("❌ No employees found. Please add employees first.")
            return
        
        print(f"Found {len(employees)} employees")
        
        # Create payroll for each employee
        for employee in employees:
            # Check if payroll already exists for January 2026
            pay_period_start = date(2026, 1, 1)
            pay_period_end = date(2026, 1, 31)
            
            existing_payroll = Payroll.query.filter_by(
                employee_id=employee.id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end
            ).first()
            
            if existing_payroll:
                print(f"⏭  Payroll already exists for {employee.full_name}")
                continue
            
            # Use employee's configured salary or default
            base_salary = float(employee.monthly_wage or employee.salary or 50000)
            
            # Calculate components
            basic_salary = base_salary * 0.50
            hra = basic_salary * 0.50
            standard_allowance = 4167
            performance_bonus = base_salary * 0.0833
            lta = base_salary * 0.08333
            fixed_allowance = base_salary - (basic_salary + hra + standard_allowance + performance_bonus + lta)
            
            # Calculate deductions
            pf = basic_salary * 0.12
            professional_tax = 200
            
            total_earnings = base_salary
            total_deductions = pf + professional_tax
            net_salary = total_earnings - total_deductions
            
            # Create payroll record
            payroll = Payroll(
                employee_id=employee.id,
                pay_period_start=pay_period_start,
                pay_period_end=pay_period_end,
                base_monthly_salary=Decimal(str(base_salary)),
                basic_salary=Decimal(str(basic_salary)),
                hra=Decimal(str(hra)),
                standard_allowance=Decimal(str(standard_allowance)),
                performance_bonus=Decimal(str(performance_bonus)),
                lta=Decimal(str(lta)),
                fixed_allowance=Decimal(str(max(0, fixed_allowance))),
                allowances=Decimal('0'),
                increment_amount=Decimal('0'),
                increment_percentage=Decimal('0'),
                special_bonus=Decimal('0'),
                festival_bonus=Decimal('0'),
                other_earnings=Decimal('0'),
                pf_deduction=Decimal(str(pf)),
                professional_tax=Decimal(str(professional_tax)),
                deductions=Decimal('0'),
                tax_deductions=Decimal('0'),
                unpaid_leave_deduction=Decimal('0'),
                days_present=26,
                total_working_days=26,
                unpaid_leave_days=0,
                paid_leave_days=26,
                overtime_hours=0.0,
                overtime_rate=Decimal('0'),
                gross_pay=Decimal(str(total_earnings)),
                total_deductions=Decimal(str(total_deductions)),
                net_pay=Decimal(str(net_salary)),
                payment_status='Paid',
                payment_date=date(2026, 1, 31),
                created_at=datetime.utcnow()
            )
            
            db.session.add(payroll)
            print(f"✓ Created payroll for {employee.full_name} - ₹{net_salary:,.2f}")
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✅ Dummy payroll data added successfully!")
            print("\nPayroll Summary:")
            
            # Show summary
            pay_start = date(2026, 1, 1)
            pay_end = date(2026, 1, 31)
            all_payroll = Payroll.query.filter_by(
                pay_period_start=pay_start,
                pay_period_end=pay_end
            ).all()
            for p in all_payroll:
                print(f"  - {p.employee.full_name}: ₹{float(p.net_pay):,.2f} (Status: {p.payment_status})")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    add_dummy_payroll()
