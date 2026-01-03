#!/usr/bin/env python3
"""
Simple run script for Dayflow HRMS
This script starts the Flask development server with proper configuration
"""

import os
import sys
from datetime import datetime

def print_banner():
    print("=" * 60)
    print("🏢 DAYFLOW - HUMAN RESOURCE MANAGEMENT SYSTEM")
    print("Every workday, perfectly aligned.")
    print("=" * 60)
    print(f"🕒 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

def check_requirements():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        print("✅ All required dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Please install requirements: pip install -r requirements.txt")
        return False

def main():
    print_banner()
    
    # Check dependencies
    if not check_requirements():
        sys.exit(1)
    
    # Import and run the app
    try:
        from app import app
        
        print("🚀 Starting Dayflow HRMS server...")
        print("📍 Application will be available at: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Run the Flask development server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=True
        )
        
    except ImportError as e:
        print(f"❌ Error importing application: {e}")
        print("🔧 Please ensure all files are in place and dependencies are installed")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("👋 Thank you for using Dayflow HRMS!")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()