#!/usr/bin/env python3
"""
Dayflow HRMS - System Check and Error Fix Script
This script performs comprehensive checks and fixes common issues
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔧 {title}")
    print(f"{'='*60}")

def check_file_structure():
    """Check if all required files exist"""
    print_header("FILE STRUCTURE CHECK")
    
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
        'app/templates/auth/signup.html',
        'app/templates/employee/dashboard.html',
        'app/templates/admin/dashboard.html',
        'app/static/css/style.css',
        'app/static/js/script.js'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
            print(f"❌ Missing: {file_path}")
        else:
            print(f"✅ Found: {file_path}")
    
    if missing_files:
        print(f"\n⚠️  {len(missing_files)} files are missing!")
        return False
    else:
        print("\n✅ All required files are present!")
        return True

def check_directories():
    """Ensure all required directories exist"""
    print_header("DIRECTORY STRUCTURE CHECK")
    
    required_dirs = [
        'app',
        'app/routes',
        'app/templates',
        'app/templates/auth',
        'app/templates/employee',
        'app/templates/admin',
        'app/static',
        'app/static/css',
        'app/static/js',
        'app/static/images',
        'uploads'
    ]
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def check_python_syntax():
    """Check Python files for syntax errors"""
    print_header("PYTHON SYNTAX CHECK")
    
    python_files = [
        'app.py',
        'app/models.py',
        'app/routes/auth.py',
        'app/routes/main.py',
        'app/routes/employee.py',
        'app/routes/admin.py'
    ]
    
    syntax_errors = []
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                compile(source, file_path, 'exec')
                print(f"✅ {file_path}: No syntax errors")
            except SyntaxError as e:
                syntax_errors.append((file_path, str(e)))
                print(f"❌ {file_path}: {e}")
            except Exception as e:
                print(f"⚠️  {file_path}: {e}")
        else:
            print(f"❌ File not found: {file_path}")
    
    if syntax_errors:
        print(f"\n⚠️  {len(syntax_errors)} files have syntax errors!")
        return False
    else:
        print("\n✅ All Python files have valid syntax!")
        return True

def check_imports():
    """Check if all required imports are working"""
    print_header("IMPORT CHECK")
    
    try:
        # Test critical imports
        import flask
        print("✅ Flask imported successfully")
        
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy imported successfully")
        
        import flask_login
        print("✅ Flask-Login imported successfully")
        
        # Try importing our modules
        sys.path.insert(0, '.')
        
        try:
            from app import app
            print("✅ Main app imported successfully")
        except Exception as e:
            print(f"❌ Error importing app: {e}")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Run: pip install -r requirements.txt")
        return False

def fix_common_issues():
    """Fix common issues automatically"""
    print_header("AUTOMATIC FIXES")
    
    fixes_applied = []
    
    # Fix 1: Create missing __init__.py files
    init_dirs = ['app', 'app/routes', 'app/templates']
    for directory in init_dirs:
        init_file = os.path.join(directory, '__init__.py')
        if not os.path.exists(init_file) and os.path.exists(directory):
            with open(init_file, 'w') as f:
                f.write('# Dayflow HRMS Package\n')
            fixes_applied.append(f"Created {init_file}")
            print(f"✅ Created {init_file}")
    
    # Fix 2: Set proper file permissions (if on Unix-like system)
    if os.name != 'nt':  # Not Windows
        try:
            os.chmod('app.py', 0o755)
            os.chmod('run.py', 0o755)
            os.chmod('setup.py', 0o755)
            fixes_applied.append("Set executable permissions")
            print("✅ Set executable permissions")
        except:
            pass
    
    # Fix 3: Create uploads directory with proper structure
    upload_dirs = ['uploads', 'uploads/profiles', 'uploads/documents']
    for directory in upload_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            fixes_applied.append(f"Created {directory}")
            print(f"✅ Created {directory}")
    
    if fixes_applied:
        print(f"\n✅ Applied {len(fixes_applied)} automatic fixes!")
    else:
        print("\n✅ No automatic fixes needed!")
    
    return True

def check_database_config():
    """Check database configuration"""
    print_header("DATABASE CONFIGURATION CHECK")
    
    try:
        # Check if MySQL/PyMySQL is available
        import pymysql
        print("✅ PyMySQL module available")
        
        # Test database connection string format
        from app import app
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        if db_uri:
            print(f"✅ Database URI configured: {db_uri}")
            if 'mysql' in db_uri:
                print("✅ MySQL database configured")
            else:
                print("⚠️  Non-MySQL database detected")
        else:
            print("❌ No database URI configured")
            return False
            
        return True
        
    except ImportError:
        print("❌ PyMySQL not installed")
        print("📦 Install with: pip install PyMySQL")
        return False
    except Exception as e:
        print(f"❌ Database configuration error: {e}")
        return False

def generate_report():
    """Generate a comprehensive system report"""
    print_header("SYSTEM REPORT")
    
    print(f"🐍 Python Version: {sys.version}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🔧 Platform: {sys.platform}")
    
    # Check disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        print(f"💽 Disk Space: {free // (1024**3)}GB free / {total // (1024**3)}GB total")
    except:
        pass
    
    # Check file count
    total_files = sum(len(files) for _, _, files in os.walk('.'))
    print(f"📄 Total Files: {total_files}")
    
    return True

def main():
    print("🏢 DAYFLOW HRMS - SYSTEM CHECK & ERROR FIX")
    print("=" * 60)
    print("This script will check for common issues and attempt to fix them automatically.")
    print()
    
    checks = [
        ("Directory Structure", check_directories),
        ("File Structure", check_file_structure), 
        ("Python Syntax", check_python_syntax),
        ("Import Dependencies", check_imports),
        ("Database Configuration", check_database_config),
        ("Apply Automatic Fixes", fix_common_issues),
        ("System Report", generate_report)
    ]
    
    passed = 0
    failed = 0
    
    for check_name, check_func in checks:
        try:
            if check_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            failed += 1
    
    # Final summary
    print_header("FINAL SUMMARY")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 All checks passed! Your Dayflow HRMS installation looks good!")
        print("\n🚀 You can now start the application with:")
        print("   python app.py")
        print("   OR")
        print("   python run.py")
    else:
        print(f"\n⚠️  {failed} checks failed. Please review the errors above.")
        print("\n🔧 Common solutions:")
        print("   - Install dependencies: pip install -r requirements.txt")
        print("   - Check MySQL is running")
        print("   - Verify all files are present")
    
    print("\n📚 For help, check README.md or the documentation.")

if __name__ == "__main__":
    main()