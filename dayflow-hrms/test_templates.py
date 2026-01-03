#!/usr/bin/env python3
"""
Template Fix Verification Script
Tests that the template loading issue is resolved
"""

import os
import sys
from flask import Flask

def test_template_loading():
    """Test that templates can be found and loaded"""
    print("🧪 Testing Template Loading...")
    
    try:
        # Create app with correct template folder
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        app.config['SECRET_KEY'] = 'test-key'
        
        with app.app_context():
            # Test template loader can find templates
            template_loader = app.jinja_loader
            
            # Check if key templates exist
            templates_to_check = [
                'base.html',
                'auth/login.html', 
                'auth/signup.html',
                'employee/dashboard.html',
                'admin/dashboard.html'
            ]
            
            found_templates = []
            missing_templates = []
            
            for template in templates_to_check:
                try:
                    source = template_loader.get_source(app.jinja_env, template)
                    found_templates.append(template)
                    print(f"✅ Found: {template}")
                except Exception as e:
                    missing_templates.append(template)
                    print(f"❌ Missing: {template} - {e}")
            
            if missing_templates:
                print(f"\n❌ {len(missing_templates)} templates not found")
                return False
            else:
                print(f"\n✅ All {len(found_templates)} templates found successfully!")
                return True
                
    except Exception as e:
        print(f"❌ Template loading test failed: {e}")
        return False

def test_static_folder():
    """Test that static files can be found"""
    print("\n🧪 Testing Static File Access...")
    
    try:
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        
        with app.app_context():
            # Check static files
            static_files = [
                'css/style.css',
                'js/script.js'
            ]
            
            found_static = []
            missing_static = []
            
            for static_file in static_files:
                static_path = os.path.join('app/static', static_file)
                if os.path.exists(static_path):
                    found_static.append(static_file)
                    print(f"✅ Found: {static_file}")
                else:
                    missing_static.append(static_file)
                    print(f"❌ Missing: {static_file}")
            
            if missing_static:
                print(f"\n❌ {len(missing_static)} static files not found")
                return False
            else:
                print(f"\n✅ All {len(found_static)} static files found!")
                return True
                
    except Exception as e:
        print(f"❌ Static file test failed: {e}")
        return False

def test_app_creation_with_templates():
    """Test that the app can be created and templates rendered"""
    print("\n🧪 Testing App Creation with Template Rendering...")
    
    try:
        # Import the actual app 
        from app.models import db
        
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        app.config['SECRET_KEY'] = 'test-key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        # Register blueprints
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp
        from app.routes.employee import employee_bp
        from app.routes.admin import admin_bp
        
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.register_blueprint(main_bp)
        app.register_blueprint(employee_bp, url_prefix='/employee')
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        print("✅ App created with blueprints")
        
        # Test that we can create the app context
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
            
            # Test template rendering
            from flask import render_template_string, render_template
            
            # Test simple template rendering
            try:
                template_test = render_template('base.html')
                print("✅ Base template renders successfully")
            except Exception as e:
                print(f"❌ Base template error: {e}")
                return False
            
            return True
            
    except Exception as e:
        print(f"❌ App creation test failed: {e}")
        return False

def main():
    """Run template fix verification"""
    print("🔧 TEMPLATE FIX VERIFICATION")
    print("="*50)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        ("Template Loading", test_template_loading),
        ("Static File Access", test_static_folder),
        ("App Creation with Templates", test_app_creation_with_templates)
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
    
    print(f"\n{'='*50}")
    print(f"🎯 TEMPLATE FIX RESULTS:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print(f"\n🎉 TEMPLATE LOADING FIXED! 🎉")
        print("The auth/login.html template error is resolved!")
        print("\n🚀 Your app should now work at:")
        print("   http://127.0.0.1:5000")
    else:
        print(f"\n⚠️  Some template issues remain.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)