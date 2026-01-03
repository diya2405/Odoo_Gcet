#!/usr/bin/env python3
"""
Dayflow HRMS Setup Script
This script helps set up the Dayflow Human Resource Management System
"""

import os
import sys
import subprocess
import mysql.connector
from mysql.connector import Error

def print_banner():
    print("=" * 60)
    print("🏢 DAYFLOW - HUMAN RESOURCE MANAGEMENT SYSTEM")
    print("Every workday, perfectly aligned.")
    print("=" * 60)
    print()

def check_python_version():
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")
    print()

def check_mysql():
    print("🔍 Checking MySQL connection...")
    try:
        # Try to connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''  # Default XAMPP password
        )
        if connection.is_connected():
            print("✅ MySQL connection successful")
            connection.close()
            return True
    except Error as e:
        print(f"❌ MySQL connection failed: {e}")
        print("   Please ensure MySQL is running (try starting XAMPP)")
        return False
    print()

def create_database():
    print("🗄️  Creating database...")
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS dayflow_hrms")
        print("✅ Database 'dayflow_hrms' created successfully")
        connection.close()
        return True
    except Error as e:
        print(f"❌ Database creation failed: {e}")
        return False

def install_dependencies():
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Try running: pip install -r requirements.txt manually")
        return False

def create_directories():
    print("📁 Creating necessary directories...")
    directories = ['uploads', 'instance']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"ℹ️  Directory already exists: {directory}")

def setup_environment():
    print("⚙️  Setting up environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        env_content = """# Dayflow HRMS Environment Configuration
SECRET_KEY=dayflow-hrms-secret-key-2026-production
DATABASE_URL=mysql://root:@localhost/dayflow_hrms
FLASK_ENV=development
FLASK_DEBUG=True
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with default configuration")
    else:
        print("ℹ️  .env file already exists")

def run_initial_setup():
    print("🚀 Running initial database setup...")
    try:
        # Import and run the Flask app to create tables
        import app
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def print_success_message():
    print()
    print("=" * 60)
    print("🎉 DAYFLOW HRMS SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("1. Start the application:")
    print("   python app.py")
    print()
    print("2. Open your browser and visit:")
    print("   http://localhost:5000")
    print()
    print("3. Create your admin account:")
    print("   - Click 'Sign Up'")
    print("   - Fill in your details")
    print("   - Select 'Admin/HR' as role")
    print()
    print("🔧 Troubleshooting:")
    print("- Ensure MySQL/XAMPP is running")
    print("- Check that port 5000 is available")
    print("- Review README.md for detailed instructions")
    print()
    print("📚 Documentation: README.md")
    print("🐛 Issues: Check console for error messages")
    print()
    print("Happy managing! 🚀")
    print("=" * 60)

def main():
    print_banner()
    
    # Step 1: Check Python version
    check_python_version()
    
    # Step 2: Check MySQL
    if not check_mysql():
        print("\n⚠️  Setup cannot continue without MySQL.")
        print("Please install and start MySQL (XAMPP recommended)")
        sys.exit(1)
    
    # Step 3: Create database
    if not create_database():
        print("\n⚠️  Setup cannot continue without database.")
        sys.exit(1)
    
    # Step 4: Install dependencies
    if not install_dependencies():
        print("\n⚠️  Setup cannot continue without dependencies.")
        sys.exit(1)
    
    # Step 5: Create directories
    create_directories()
    
    # Step 6: Setup environment
    setup_environment()
    
    # Step 7: Initialize database
    if not run_initial_setup():
        print("\n⚠️  Database initialization failed.")
        print("You may need to run 'python app.py' manually")
    
    # Step 8: Success message
    print_success_message()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check the error and try again")
        sys.exit(1)