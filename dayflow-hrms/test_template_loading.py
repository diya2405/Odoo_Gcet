#!/usr/bin/env python3
"""
Template Loading Test Script
Tests if Flask can properly load admin templates
"""

import os
import sys

def test_template_loading():
    """Test if Flask can load the admin templates"""
    print("Testing Flask template loading...")
    
    try:
        from flask import Flask
        
        # Create Flask app with same configuration as main app
        app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
        
        with app.app_context():
            from flask import render_template_string
            
            # Test basic template loading
            print("✅ Flask app created successfully")
            
            # Test admin template loading
            admin_templates = [
                'admin/attendance.html',
                'admin/leave_requests.html', 
                'admin/payroll.html'
            ]
            
            for template in admin_templates:
                try:
                    # Try to load the template
                    env = app.jinja_env
                    template_obj = env.get_template(template)
                    print(f"✅ {template} loaded successfully")
                except Exception as e:
                    print(f"❌ {template} failed to load: {e}")
                    return False
            
            print("✅ All admin templates loaded successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run template loading test"""
    print("🧪 TESTING FLASK TEMPLATE LOADING")
    print("="*50)
    
    # Ensure we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: Not in the right directory (app.py not found)")
        return False
    
    if not os.path.exists('app/templates'):
        print("❌ Error: app/templates directory not found")
        return False
    
    print("✅ Directory structure looks correct")
    
    # Test template loading
    success = test_template_loading()
    
    if success:
        print("\n🎉 SUCCESS: All templates can be loaded by Flask!")
        print("The TemplateNotFound errors should not occur.")
        print("Try restarting the Flask app: python app.py")
    else:
        print("\n❌ FAILED: Templates cannot be loaded")
        print("There may be an issue with the template content or Flask configuration.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)