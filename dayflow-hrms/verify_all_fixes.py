#!/usr/bin/env python3
"""
Final Error Resolution Verification Script
Tests that all TemplateSyntaxError and missing template issues are resolved
"""

import os
import sys
from datetime import datetime

def test_all_template_syntax():
    """Test that all templates have valid Jinja2 syntax"""
    print("🧪 Testing Template Syntax...")
    
    try:
        from jinja2 import Environment, FileSystemLoader
        
        # Create Jinja2 environment
        env = Environment(loader=FileSystemLoader('app/templates'))
        
        # List of all templates to test
        templates_to_test = [
            'base.html',
            'auth/login.html',
            'auth/signup.html',
            'auth/forgot_password.html',
            'employee/dashboard.html',
            'employee/profile.html',
            'employee/edit_profile.html',
            'employee/attendance.html',
            'employee/leave_requests.html',
            'employee/apply_leave.html',
            'employee/payroll.html',
            'admin/dashboard.html',
            'admin/employees.html',
            'admin/employee_detail.html',
            'admin/edit_employee.html'
        ]
        
        valid_templates = []
        invalid_templates = []
        
        for template_name in templates_to_test:
            try:
                template = env.get_template(template_name)
                valid_templates.append(template_name)
                print(f"✅ {template_name}")
            except Exception as e:
                invalid_templates.append((template_name, str(e)))
                print(f"❌ {template_name}: {e}")
        
        if invalid_templates:
            print(f"\n❌ {len(invalid_templates)} templates have syntax errors!")
            return False
        else:
            print(f"\n✅ All {len(valid_templates)} templates have valid syntax!")
            return True
            
    except Exception as e:
        print(f"❌ Template syntax test failed: {e}")
        return False

def test_app_startup():
    """Test that the application starts without template errors"""
    print("\n🧪 Testing Application Startup...")
    
    try:
        # Import the main app module
        import app as app_module
        print("✅ Main application module imported successfully")
        
        # Get the Flask app instance
        flask_app = app_module.app
        print("✅ Flask app instance accessed successfully")
        
        # Test creating the Flask app context
        with flask_app.app_context():
            print("✅ Application context created successfully")
            
            # Test that templates can be rendered (basic test)
            from flask import render_template_string
            test_template = "{{ 'Hello World' }}"
            result = render_template_string(test_template)
            if result == "Hello World":
                print("✅ Template rendering engine works")
            else:
                print("❌ Template rendering engine failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Application startup test failed: {e}")
        return False

def test_specific_fixes():
    """Test the specific issues that were fixed"""
    print("\n🧪 Testing Specific Fixes...")
    
    fixes_verified = []
    
    # Test 1: Check that escaped quotes are removed from attendance.html
    try:
        with open('app/templates/employee/attendance.html', 'r') as f:
            content = f.read()
        
        if '\\"' not in content:
            print("✅ No escaped quotes found in attendance.html")
            fixes_verified.append("escaped_quotes")
        else:
            print("❌ Escaped quotes still present in attendance.html")
        
    except Exception as e:
        print(f"❌ Could not verify escaped quotes fix: {e}")
    
    # Test 2: Check that admin templates exist
    admin_templates = [
        'app/templates/admin/employee_detail.html',
        'app/templates/admin/edit_employee.html'
    ]
    
    admin_templates_exist = True
    for template in admin_templates:
        if os.path.exists(template):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} missing")
            admin_templates_exist = False
    
    if admin_templates_exist:
        fixes_verified.append("admin_templates")
    
    # Test 3: Check Flask template folder configuration
    try:
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        if "template_folder='app/templates'" in app_content:
            print("✅ Flask template folder correctly configured")
            fixes_verified.append("template_folder")
        else:
            print("❌ Flask template folder not configured")
    
    except Exception as e:
        print(f"❌ Could not verify template folder fix: {e}")
    
    print(f"\n✅ {len(fixes_verified)}/3 specific fixes verified")
    return len(fixes_verified) == 3

def main():
    """Run all verification tests"""
    print("🔧 FINAL ERROR RESOLUTION VERIFICATION")
    print("="*60)
    print("Verifying that all TemplateSyntaxError and missing template issues are resolved")
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        ("Template Syntax Validation", test_all_template_syntax),
        ("Application Startup", test_app_startup),
        ("Specific Fixes Verification", test_specific_fixes)
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
    
    print(f"\n{'='*60}")
    print(f"🎯 FINAL VERIFICATION RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print(f"\n🎉 ALL TEMPLATE ERRORS RESOLVED! 🎉")
        print("✅ TemplateSyntaxError: Fixed all escaped quotes")
        print("✅ TemplateNotFound: Created missing admin templates")
        print("✅ Template folder: Correctly configured in Flask")
        print("✅ Template syntax: All templates have valid Jinja2 syntax")
        print("\n🚀 Your Dayflow HRMS is now error-free:")
        print("   python app.py")
        print("   Visit: http://127.0.0.1:5000")
    else:
        print(f"\n⚠️  {failed} verification tests failed.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)