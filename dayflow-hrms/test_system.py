#!/usr/bin/env python3
"""
Dayflow HRMS - Quick Test Script
Tests core functionality without starting the full web server
"""

import os
import sys
import tempfile
from datetime import date

def test_imports():
    """Test that all modules can be imported successfully"""
    print("🧪 Testing Python Imports...")
    
    try:
        # Test Flask and extensions
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_login import LoginManager
        print("✅ Flask and extensions imported successfully")
        
        # Test our application modules
        sys.path.insert(0, '.')
        from app.models import User, Employee, Attendance, LeaveRequest, Payroll
        print("✅ Application models imported successfully")
        
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp
        from app.routes.employee import employee_bp
        from app.routes.admin import admin_bp
        print("✅ Application routes imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database_models():
    """Test database model creation"""
    print("\n🧪 Testing Database Models...")
    
    try:
        from flask import Flask
        from app.models import db, User, Employee
        
        # Create a test app with in-memory SQLite
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            # Create tables
            db.create_all()
            print("✅ Database tables created successfully")
            
            # Test creating a user
            test_user = User(
                employee_id='TEST001',
                email='test@dayflow.com',
                role='employee'
            )
            test_user.set_password('TestPassword123!')
            
            db.session.add(test_user)
            db.session.commit()
            print("✅ User model creation and password hashing works")
            
            # Test password verification
            if test_user.check_password('TestPassword123!'):
                print("✅ Password verification works")
            else:
                print("❌ Password verification failed")
                return False
            
            # Test creating employee profile
            test_employee = Employee(
                user_id=test_user.id,
                first_name='Test',
                last_name='User',
                department='IT',
                position='Developer',
                hire_date=date.today()
            )
            
            db.session.add(test_employee)
            db.session.commit()
            print("✅ Employee model creation works")
            
            return True
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

def test_application_creation():
    """Test that the main application can be created"""
    print("\n🧪 Testing Application Creation...")
    
    try:
        # Import after ensuring path is set
        sys.path.insert(0, '.')
        
        # Test app creation without running
        from flask import Flask
        from flask_sqlalchemy import SQLAlchemy
        from flask_login import LoginManager
        from app.models import db
        
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize extensions
        db.init_app(app)
        login_manager = LoginManager()
        login_manager.init_app(app)
        
        # Register blueprints
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp
        from app.routes.employee import employee_bp
        from app.routes.admin import admin_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(main_bp)
        app.register_blueprint(employee_bp, url_prefix='/employee')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        print("✅ Flask application created successfully")
        print("✅ All blueprints registered successfully")
        
        # Test that we can create tables
        with app.app_context():
            db.create_all()
            print("✅ Database initialization successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Application creation error: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing File Structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'app/models.py',
        'app/routes/auth.py',
        'app/routes/main.py',
        'app/routes/employee.py',
        'app/routes/admin.py',
        'app/templates/base.html',
        'app/templates/auth/login.html',
        'app/static/css/style.css',
        'app/static/js/script.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ Missing: {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ {len(missing_files)} required files are missing!")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files exist!")
        return True

def main():
    """Run all tests"""
    print("🏢 DAYFLOW HRMS - QUICK FUNCTIONALITY TEST")
    print("="*60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_imports),
        ("Database Models", test_database_models),
        ("Application Creation", test_application_creation)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSED")
            else:
                failed += 1
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "="*60)
    print(f"🎯 FINAL RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print(f"\n🎉 ALL TESTS PASSED! 🎉")
        print("Your Dayflow HRMS is ready to run!")
        print("\n🚀 To start the application:")
        print("   python app.py")
        print("   Then visit: http://127.0.0.1:5000")
    else:
        print(f"\n⚠️  Some tests failed. Please review the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = main()
    sys.exit(0 if success else 1)