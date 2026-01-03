"""
Get credentials for employees with different leave types
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Employee, LeaveRequest

def get_leave_credentials():
    """Get credentials for employees on different leave types"""
    app = create_app()
    
    with app.app_context():
        print("="*70)
        print("     EMPLOYEE CREDENTIALS BY LEAVE TYPE")
        print("="*70)
        
        # Get sick leave employees
        sick_leaves = LeaveRequest.query.filter_by(leave_type='sick').all()
        print("\n🤒 SICK LEAVE EMPLOYEES:")
        print("-"*70)
        for leave in sick_leaves:
            employee = leave.employee
            user = employee.user
            print(f"\n👤 {employee.full_name}")
            print(f"   📧 Email: {user.email}")
            print(f"   🔑 Password: Password@123")
            print(f"   📋 Leave Status: {leave.status.upper()}")
            print(f"   📅 Duration: {leave.start_date} to {leave.end_date} ({leave.days_requested} days)")
            print(f"   💼 Department: {employee.department}")
            print(f"   📍 Position: {employee.position}")
        
        # Get paid leave employees
        paid_leaves = LeaveRequest.query.filter_by(leave_type='paid').all()
        print("\n\n🏖️ PAID LEAVE EMPLOYEES:")
        print("-"*70)
        for leave in paid_leaves:
            employee = leave.employee
            user = employee.user
            print(f"\n👤 {employee.full_name}")
            print(f"   📧 Email: {user.email}")
            print(f"   🔑 Password: Password@123")
            print(f"   📋 Leave Status: {leave.status.upper()}")
            print(f"   📅 Duration: {leave.start_date} to {leave.end_date} ({leave.days_requested} days)")
            print(f"   💼 Department: {employee.department}")
            print(f"   📍 Position: {employee.position}")
        
        # Get unpaid leave employees
        unpaid_leaves = LeaveRequest.query.filter_by(leave_type='unpaid').all()
        print("\n\n💰 UNPAID LEAVE EMPLOYEES:")
        print("-"*70)
        for leave in unpaid_leaves:
            employee = leave.employee
            user = employee.user
            print(f"\n👤 {employee.full_name}")
            print(f"   📧 Email: {user.email}")
            print(f"   🔑 Password: Password@123")
            print(f"   📋 Leave Status: {leave.status.upper()}")
            print(f"   📅 Duration: {leave.start_date} to {leave.end_date} ({leave.days_requested} days)")
            print(f"   💼 Department: {employee.department}")
            print(f"   📍 Position: {employee.position}")
        
        print("\n" + "="*70)
        print("     QUICK REFERENCE SUMMARY")
        print("="*70)
        
        if sick_leaves:
            print("\n🤒 SICK LEAVE:")
            for leave in sick_leaves:
                print(f"   {leave.employee.user.email} | {leave.status}")
        
        if paid_leaves:
            print("\n🏖️ PAID LEAVE:")
            for leave in paid_leaves:
                print(f"   {leave.employee.user.email} | {leave.status}")
        
        if unpaid_leaves:
            print("\n💰 UNPAID LEAVE:")
            for leave in unpaid_leaves:
                print(f"   {leave.employee.user.email} | {leave.status}")
        
        print("\n🔑 Default Password for ALL employees: Password@123")
        print("="*70)


if __name__ == '__main__':
    get_leave_credentials()
