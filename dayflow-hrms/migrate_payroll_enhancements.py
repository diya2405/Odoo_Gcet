"""
Database migration script to add new payroll and leave enhancements
This script adds new fields to the Payroll model for detailed salary breakdown
"""

from app import create_app, db
from sqlalchemy import text

app = create_app()

def migrate_database():
    """Add new columns to payroll table for enhanced salary breakdown"""
    
    with app.app_context():
        try:
            print("Starting database migration for payroll enhancements...")
            
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('payroll')]
            
            # Define new columns to add
            new_columns = {
                'base_monthly_salary': 'NUMERIC(10, 2) DEFAULT 0.00',
                'increment_amount': 'NUMERIC(10, 2) DEFAULT 0.00',
                'increment_percentage': 'NUMERIC(5, 2) DEFAULT 0.00',
                'special_bonus': 'NUMERIC(10, 2) DEFAULT 0.00',
                'festival_bonus': 'NUMERIC(10, 2) DEFAULT 0.00',
                'other_earnings': 'NUMERIC(10, 2) DEFAULT 0.00',
                'unpaid_leave_deduction': 'NUMERIC(10, 2) DEFAULT 0.00',
                'paid_leave_days': 'INTEGER DEFAULT 0',
                'total_deductions': 'NUMERIC(10, 2) DEFAULT 0.00',
                'payment_status': "VARCHAR(20) DEFAULT 'pending'",
                'payment_date': 'DATE'
            }
            
            # Add missing columns
            for column_name, column_type in new_columns.items():
                if column_name not in existing_columns:
                    try:
                        sql = f"ALTER TABLE payroll ADD COLUMN {column_name} {column_type}"
                        db.session.execute(text(sql))
                        print(f"✓ Added column: {column_name}")
                    except Exception as e:
                        print(f"✗ Error adding column {column_name}: {str(e)}")
            
            # Ensure certificate_path exists in leave_requests table (already exists in model)
            leave_columns = [col['name'] for col in inspector.get_columns('leave_requests')]
            if 'certificate_path' not in leave_columns:
                try:
                    sql = "ALTER TABLE leave_requests ADD COLUMN certificate_path VARCHAR(200)"
                    db.session.execute(text(sql))
                    print("✓ Added certificate_path column to leave_requests")
                except Exception as e:
                    print(f"✗ Error adding certificate_path: {str(e)}")
            
            db.session.commit()
            print("\n✓ Database migration completed successfully!")
            print("\nNew features enabled:")
            print("  - Medical certificate upload for sick leave")
            print("  - Detailed salary breakdown with increments and bonuses")
            print("  - Automatic unpaid leave salary deductions")
            print("  - Enhanced payroll view with all earning and deduction details")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()
