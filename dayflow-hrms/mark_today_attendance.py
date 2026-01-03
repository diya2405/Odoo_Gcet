"""
Mark employees as present for today
"""
import sys
import os
from datetime import datetime, date, time
import random

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Employee, Attendance

def mark_today_attendance():
    """Mark employees as present for today"""
    app = create_app()
    
    with app.app_context():
        today = date.today()
        
        # Get all active employees
        all_employees = Employee.query.all()
        total_employees = len(all_employees)
        
        print(f"📊 Total employees in database: {total_employees}")
        
        if total_employees == 0:
            print("❌ No employees found in database!")
            return
        
        # Calculate how many to mark present (48 out of 53, proportionally)
        target_percentage = 48 / 53  # About 90.5%
        present_count = int(total_employees * target_percentage)
        
        print(f"🎯 Target: Mark {present_count} employees as present today ({today})")
        
        # Check if attendance already exists for today
        existing_attendance = Attendance.query.filter_by(date=today).all()
        if existing_attendance:
            print(f"\n⚠️  Found {len(existing_attendance)} existing attendance records for today")
            print("🗑️  Deleting existing records and creating fresh data...")
            for att in existing_attendance:
                db.session.delete(att)
            db.session.commit()
            print("✅ Deleted existing attendance records")
        
        # Randomly select employees to mark as present
        present_employees = random.sample(all_employees, present_count)
        
        print(f"\n✅ Marking {len(present_employees)} employees as present...")
        
        for employee in present_employees:
            # Generate realistic check-in time (8:00 AM to 10:30 AM)
            check_in_hour = random.randint(8, 10)
            check_in_minute = random.randint(0, 59) if check_in_hour < 10 else random.randint(0, 30)
            
            # Generate realistic check-out time (5:00 PM to 7:30 PM)
            check_out_hour = random.randint(17, 19)
            check_out_minute = random.randint(0, 59) if check_out_hour < 19 else random.randint(0, 30)
            
            # Calculate hours worked
            check_in = datetime.combine(today, time(check_in_hour, check_in_minute))
            check_out = datetime.combine(today, time(check_out_hour, check_out_minute))
            duration = check_out - check_in
            hours_worked = duration.total_seconds() / 3600 - 1.0  # Subtract 1 hour break
            
            attendance = Attendance(
                employee_id=employee.id,
                date=today,
                check_in_time=time(check_in_hour, check_in_minute),
                check_out_time=time(check_out_hour, check_out_minute),
                break_time=1.0,
                status='present',
                hours_worked=hours_worked,
                work_location=random.choice(['Office', 'Office', 'Office', 'Remote']),  # 75% office, 25% remote
                remarks='Regular working day'
            )
            db.session.add(attendance)
            print(f"  ✅ {employee.full_name} - Check-in: {check_in_hour:02d}:{check_in_minute:02d}, Check-out: {check_out_hour:02d}:{check_out_minute:02d}")
        
        db.session.commit()
        
        # Mark remaining employees as absent
        absent_employees = [emp for emp in all_employees if emp not in present_employees]
        
        print(f"\n📋 Summary for {today}:")
        print(f"   ✅ Present: {len(present_employees)} employees")
        print(f"   ❌ Absent: {len(absent_employees)} employees")
        print(f"   📊 Attendance Rate: {(len(present_employees)/total_employees)*100:.1f}%")
        
        if absent_employees:
            print(f"\n❌ Absent employees:")
            for emp in absent_employees:
                print(f"   • {emp.full_name} ({emp.department})")
        
        print("\n✅ Today's attendance marked successfully!")


if __name__ == '__main__':
    mark_today_attendance()
