"""
Migration script to ensure Employee and SalaryComponent tables are ready for salary management
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Employee, SalaryComponent
from sqlalchemy import text, inspect

def check_and_add_columns():
    """Check and add missing columns to employees table"""
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check employees table
        if 'employees' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('employees')]
            print(f"✓ Employees table exists with {len(columns)} columns")
            
            # Check for monthly_wage column
            if 'monthly_wage' not in columns:
                print("  Adding monthly_wage column...")
                try:
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE employees ADD COLUMN monthly_wage NUMERIC(10, 2)"))
                        conn.commit()
                    print("  ✓ monthly_wage column added")
                except Exception as e:
                    print(f"  ⚠ Error adding monthly_wage: {e}")
            else:
                print("  ✓ monthly_wage column exists")
            
            # Check for working_days_per_week column
            if 'working_days_per_week' not in columns:
                print("  Adding working_days_per_week column...")
                try:
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE employees ADD COLUMN working_days_per_week INTEGER DEFAULT 5"))
                        conn.commit()
                    print("  ✓ working_days_per_week column added")
                except Exception as e:
                    print(f"  ⚠ Error adding working_days_per_week: {e}")
            else:
                print("  ✓ working_days_per_week column exists")
            
            # Check for working_hours_per_day column
            if 'working_hours_per_day' not in columns:
                print("  Adding working_hours_per_day column...")
                try:
                    with db.engine.connect() as conn:
                        conn.execute(text("ALTER TABLE employees ADD COLUMN working_hours_per_day FLOAT DEFAULT 8.0"))
                        conn.commit()
                    print("  ✓ working_hours_per_day column added")
                except Exception as e:
                    print(f"  ⚠ Error adding working_hours_per_day: {e}")
            else:
                print("  ✓ working_hours_per_day column exists")
        
        # Check salary_components table
        if 'salary_components' not in inspector.get_table_names():
            print("\n⚠ salary_components table does not exist. Creating it...")
            try:
                db.create_all()
                print("✓ salary_components table created")
            except Exception as e:
                print(f"✗ Error creating salary_components table: {e}")
        else:
            columns = [col['name'] for col in inspector.get_columns('salary_components')]
            print(f"\n✓ salary_components table exists with {len(columns)} columns")
        
        print("\n✓ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Edit an employee from the admin panel")
        print("2. Set the monthly wage and configure salary components")
        print("3. View the employee detail page to see the salary breakdown")

if __name__ == '__main__':
    try:
        check_and_add_columns()
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
