"""
Migration script to add is_active column to users table
"""
import sys
import os

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text, inspect

def add_is_active_column():
    """Add is_active column to users table"""
    app = create_app()
    
    with app.app_context():
        inspector = inspect(db.engine)
        
        # Check users table
        if 'users' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('users')]
            print(f"✓ Users table exists with {len(columns)} columns")
            
            # Check for is_active column
            if 'is_active' not in columns:
                print("  Adding is_active column...")
                try:
                    with db.engine.connect() as conn:
                        # Add column with default value TRUE
                        conn.execute(text("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1 NOT NULL"))
                        conn.commit()
                    print("  ✓ is_active column added successfully")
                    print("  ✓ All existing users set to active by default")
                except Exception as e:
                    print(f"  ⚠ Error adding is_active column: {e}")
                    return False
            else:
                print("  ✓ is_active column already exists")
        else:
            print("✗ Users table does not exist!")
            return False
        
        print("\n✓ Migration completed successfully!")
        print("\nFeatures added:")
        print("1. Admin can now deactivate user accounts")
        print("2. Admin can delete user accounts")
        print("3. Deactivated users cannot log in")
        print("4. Status badges show account state (Active/Deactivated)")
        return True

if __name__ == '__main__':
    try:
        success = add_is_active_column()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
