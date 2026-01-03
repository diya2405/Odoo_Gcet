from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import random
import string

# Import db from __init__.py to avoid multiple instances
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # 'employee' or 'admin'
    is_verified = db.Column(db.Boolean, default=False)
    password_changed = db.Column(db.Boolean, default=False)  # Track if user changed auto-generated password
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with Employee
    employee_profile = db.relationship('Employee', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    @staticmethod
    def generate_employee_id(company_code, first_name, last_name, hire_year):
        """
        Generate employee ID in format: [CompanyCode][FirstName][LastName][Year][SerialNumber]
        Example: OIJODO20220001
        """
        # Get initials: first two letters of first and last name
        first_initial = first_name[:2].upper() if len(first_name) >= 2 else first_name.upper().ljust(2, 'X')
        last_initial = last_name[:2].upper() if len(last_name) >= 2 else last_name.upper().ljust(2, 'X')
        
        # Count existing employees for that year
        existing_count = User.query.filter(
            User.employee_id.like(f"{company_code}{first_initial}{last_initial}{hire_year}%")
        ).count()
        
        serial = str(existing_count + 1).zfill(4)
        return f"{company_code}{first_initial}{last_initial}{hire_year}{serial}"
    
    @staticmethod
    def generate_random_password(length=10):
        """Generate a random password for new employees"""
        characters = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(characters) for _ in range(length))
    
    def __repr__(self):
        return f'<User {self.employee_id}>'

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    personal_email = db.Column(db.String(120))
    address = db.Column(db.Text)
    date_of_birth = db.Column(db.Date)
    hire_date = db.Column(db.Date, default=date.today)
    department = db.Column(db.String(100))
    position = db.Column(db.String(100))
    
    # Personal Information
    gender = db.Column(db.String(10))  # Male, Female, Other
    marital_status = db.Column(db.String(20))  # Single, Married, Divorced, Widowed
    nationality = db.Column(db.String(50), default='Indian')
    
    # Government IDs
    pan_no = db.Column(db.String(20))
    uan_no = db.Column(db.String(20))
    
    # Bank Details
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(50))
    ifsc_code = db.Column(db.String(20))
    
    # Professional Details
    skills = db.Column(db.Text)  # JSON or comma-separated
    certifications = db.Column(db.Text)  # JSON or comma-separated
    interests = db.Column(db.Text)
    resume = db.Column(db.String(200))  # File path
    
    # Manager relationship
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')
    
    # Salary and Work Info
    monthly_wage = db.Column(db.Numeric(10, 2))  # Total monthly wage
    salary = db.Column(db.Numeric(10, 2))  # Kept for backward compatibility
    working_hours_per_day = db.Column(db.Float, default=8.0)
    working_days_per_week = db.Column(db.Integer, default=5)
    
    profile_picture = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='employee', lazy=True)
    leave_requests = db.relationship('LeaveRequest', backref='employee', lazy=True)
    payroll_records = db.relationship('Payroll', backref='employee', lazy=True)
    salary_components = db.relationship('SalaryComponent', backref='employee', lazy=True)
    leave_allocations = db.relationship('LeaveAllocation', backref='employee', lazy=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def current_status(self):
        """Get current status: present, absent, on_leave"""
        today = date.today()
        
        # Check if on approved leave
        leave_today = LeaveRequest.query.filter(
            LeaveRequest.employee_id == self.id,
            LeaveRequest.status == 'approved',
            LeaveRequest.start_date <= today,
            LeaveRequest.end_date >= today
        ).first()
        
        if leave_today:
            return 'on_leave'
        
        # Check attendance
        attendance_today = Attendance.query.filter_by(
            employee_id=self.id,
            date=today
        ).first()
        
        if attendance_today and attendance_today.status == 'present':
            return 'present'
        
        return 'absent'
    
    def __repr__(self):
        return f'<Employee {self.full_name}>'

class Attendance(db.Model):
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    check_in_time = db.Column(db.Time)
    check_out_time = db.Column(db.Time)
    break_time = db.Column(db.Float, default=0.0)  # Break time in hours
    status = db.Column(db.String(20), nullable=False, default='absent')  # 'present', 'absent', 'half_day', 'leave'
    hours_worked = db.Column(db.Float, default=0.0)
    work_location = db.Column(db.String(100))  # Office, Remote, Field
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_hours_worked(self):
        if self.check_in_time and self.check_out_time:
            check_in = datetime.combine(date.today(), self.check_in_time)
            check_out = datetime.combine(date.today(), self.check_out_time)
            duration = check_out - check_in
            total_hours = duration.total_seconds() / 3600  # Convert to hours
            self.hours_worked = total_hours - self.break_time  # Subtract break time
        return self.hours_worked
    
    def __repr__(self):
        return f'<Attendance {self.employee.full_name} - {self.date}>'

class TimeOffType(db.Model):
    """Model for different types of time off/leave"""
    __tablename__ = 'timeoff_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # Paid Time Off, Sick Leave, Unpaid Leave
    code = db.Column(db.String(10), nullable=False, unique=True)  # PTO, SICK, UNPAID
    description = db.Column(db.Text)
    is_paid = db.Column(db.Boolean, default=True)
    requires_certificate = db.Column(db.Boolean, default=False)  # For sick leave
    default_allocation = db.Column(db.Integer, default=0)  # Days per year
    color = db.Column(db.String(20), default='#007bff')  # For UI display
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    leave_requests = db.relationship('LeaveRequest', backref='timeoff_type', lazy=True)
    allocations = db.relationship('LeaveAllocation', backref='timeoff_type', lazy=True)
    
    def __repr__(self):
        return f'<TimeOffType {self.name}>'

class LeaveAllocation(db.Model):
    """Track leave balance for each employee"""
    __tablename__ = 'leave_allocations'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    timeoff_type_id = db.Column(db.Integer, db.ForeignKey('timeoff_types.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    allocated_days = db.Column(db.Integer, nullable=False)
    used_days = db.Column(db.Integer, default=0)
    pending_days = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def available_days(self):
        return self.allocated_days - self.used_days - self.pending_days
    
    def __repr__(self):
        return f'<LeaveAllocation {self.employee.full_name} - {self.year}>'

class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    timeoff_type_id = db.Column(db.Integer, db.ForeignKey('timeoff_types.id'))
    leave_type = db.Column(db.String(20), nullable=False)  # 'paid', 'sick', 'unpaid' - kept for backward compatibility
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    certificate_path = db.Column(db.String(200))  # For sick leave certificate
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'approved', 'rejected'
    admin_comment = db.Column(db.Text)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    days_requested = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with admin who approved/rejected
    approver = db.relationship('User', foreign_keys=[approved_by], backref='approved_leaves')
    
    def calculate_days(self):
        if self.start_date and self.end_date:
            self.days_requested = (self.end_date - self.start_date).days + 1
        return self.days_requested
    
    def __repr__(self):
        return f'<LeaveRequest {self.employee.full_name} - {self.leave_type}>'

class SalaryComponent(db.Model):
    """Model for salary components like Basic, HRA, PF, etc."""
    __tablename__ = 'salary_components'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    component_name = db.Column(db.String(100), nullable=False)  # Basic Salary, HRA, PF, etc.
    component_type = db.Column(db.String(20), nullable=False)  # 'earning' or 'deduction'
    computation_type = db.Column(db.String(20), nullable=False)  # 'fixed' or 'percentage'
    value = db.Column(db.Numeric(10, 2), nullable=False)  # Amount or percentage value
    base_component = db.Column(db.String(100))  # For percentage calculations (e.g., 'Basic Salary')
    calculated_amount = db.Column(db.Numeric(10, 2))  # Final calculated amount
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_amount(self, monthly_wage, basic_salary=None):
        """Calculate the component amount based on type and value"""
        if self.computation_type == 'fixed':
            self.calculated_amount = self.value
        elif self.computation_type == 'percentage':
            if self.base_component == 'wage':
                self.calculated_amount = (float(monthly_wage) * float(self.value)) / 100
            elif self.base_component == 'basic' and basic_salary:
                self.calculated_amount = (float(basic_salary) * float(self.value)) / 100
            else:
                self.calculated_amount = 0
        return self.calculated_amount
    
    def __repr__(self):
        return f'<SalaryComponent {self.component_name} - {self.employee.full_name}>'

class Payroll(db.Model):
    __tablename__ = 'payroll'
    
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    pay_period_start = db.Column(db.Date, nullable=False)
    pay_period_end = db.Column(db.Date, nullable=False)
    
    # Salary components breakdown
    basic_salary = db.Column(db.Numeric(10, 2), nullable=False)
    hra = db.Column(db.Numeric(10, 2), default=0.00)
    standard_allowance = db.Column(db.Numeric(10, 2), default=0.00)
    performance_bonus = db.Column(db.Numeric(10, 2), default=0.00)
    lta = db.Column(db.Numeric(10, 2), default=0.00)  # Leave Travel Allowance
    fixed_allowance = db.Column(db.Numeric(10, 2), default=0.00)
    allowances = db.Column(db.Numeric(10, 2), default=0.00)  # Total other allowances
    
    # Deductions
    pf_deduction = db.Column(db.Numeric(10, 2), default=0.00)  # Provident Fund (12% of basic)
    professional_tax = db.Column(db.Numeric(10, 2), default=200.00)  # Fixed ₹200
    deductions = db.Column(db.Numeric(10, 2), default=0.00)  # Total other deductions
    tax_deductions = db.Column(db.Numeric(10, 2), default=0.00)
    
    # Attendance based
    days_present = db.Column(db.Integer, default=0)
    total_working_days = db.Column(db.Integer, default=0)
    unpaid_leave_days = db.Column(db.Integer, default=0)
    
    overtime_hours = db.Column(db.Float, default=0.0)
    overtime_rate = db.Column(db.Numeric(8, 2), default=0.00)
    
    gross_pay = db.Column(db.Numeric(10, 2))
    net_pay = db.Column(db.Numeric(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def calculate_gross_pay(self):
        """Calculate gross pay from all earning components"""
        overtime_pay = float(self.overtime_hours) * float(self.overtime_rate)
        self.gross_pay = (
            float(self.basic_salary) + 
            float(self.hra) + 
            float(self.standard_allowance) + 
            float(self.performance_bonus) + 
            float(self.lta) + 
            float(self.fixed_allowance) + 
            float(self.allowances) + 
            overtime_pay
        )
        return self.gross_pay
    
    def calculate_net_pay(self):
        """Calculate net pay after all deductions"""
        self.calculate_gross_pay()
        total_deductions = (
            float(self.pf_deduction) + 
            float(self.professional_tax) + 
            float(self.deductions) + 
            float(self.tax_deductions)
        )
        
        # Adjust for unpaid leaves
        if self.total_working_days > 0 and self.unpaid_leave_days > 0:
            per_day_salary = float(self.gross_pay) / self.total_working_days
            unpaid_leave_deduction = per_day_salary * self.unpaid_leave_days
            total_deductions += unpaid_leave_deduction
        
        self.net_pay = float(self.gross_pay) - total_deductions
        return self.net_pay
    
    def __repr__(self):
        return f'<Payroll {self.employee.full_name} - {self.pay_period_start}>'


# Utility functions
def initialize_timeoff_types():
    """Initialize default time off types if they don't exist"""
    timeoff_types = [
        {
            'name': 'Paid Time Off',
            'code': 'PTO',
            'description': 'Regular paid time off for vacation and personal matters',
            'is_paid': True,
            'requires_certificate': False,
            'default_allocation': 24,
            'color': '#28a745'
        },
        {
            'name': 'Sick Leave',
            'code': 'SICK',
            'description': 'Paid sick leave with medical certificate required',
            'is_paid': True,
            'requires_certificate': True,
            'default_allocation': 7,
            'color': '#ffc107'
        },
        {
            'name': 'Unpaid Leave',
            'code': 'UNPAID',
            'description': 'Unpaid leave without salary deduction from balance',
            'is_paid': False,
            'requires_certificate': False,
            'default_allocation': 0,
            'color': '#6c757d'
        }
    ]
    
    for timeoff_data in timeoff_types:
        existing = TimeOffType.query.filter_by(code=timeoff_data['code']).first()
        if not existing:
            timeoff = TimeOffType(**timeoff_data)
            db.session.add(timeoff)
    
    db.session.commit()


def create_salary_components_for_employee(employee_id, monthly_wage):
    """
    Create default salary components for an employee based on monthly wage
    Components:
    - Basic Salary: 50% of wage
    - HRA: 50% of basic salary
    - Standard Allowance: Fixed amount (determined after other components)
    - Performance Bonus: 8.33% of wage
    - LTA: 8.33% of wage
    - Fixed Allowance: Remaining amount to make up the wage
    - PF Deduction: 12% of basic salary
    - Professional Tax: Fixed ₹200
    """
    components = [
        {
            'component_name': 'Basic Salary',
            'component_type': 'earning',
            'computation_type': 'percentage',
            'value': 50.00,
            'base_component': 'wage'
        },
        {
            'component_name': 'House Rent Allowance',
            'component_type': 'earning',
            'computation_type': 'percentage',
            'value': 50.00,
            'base_component': 'basic'
        },
        {
            'component_name': 'Performance Bonus',
            'component_type': 'earning',
            'computation_type': 'percentage',
            'value': 8.33,
            'base_component': 'wage'
        },
        {
            'component_name': 'Leave Travel Allowance',
            'component_type': 'earning',
            'computation_type': 'percentage',
            'value': 8.33,
            'base_component': 'wage'
        },
        {
            'component_name': 'Provident Fund',
            'component_type': 'deduction',
            'computation_type': 'percentage',
            'value': 12.00,
            'base_component': 'basic'
        },
        {
            'component_name': 'Professional Tax',
            'component_type': 'deduction',
            'computation_type': 'fixed',
            'value': 200.00,
            'base_component': None
        }
    ]
    
    # Calculate basic salary first
    basic_salary = (float(monthly_wage) * 50) / 100
    
    total_components = 0
    for comp_data in components:
        comp = SalaryComponent(employee_id=employee_id, **comp_data)
        comp.calculate_amount(monthly_wage, basic_salary)
        if comp.component_type == 'earning':
            total_components += float(comp.calculated_amount)
        db.session.add(comp)
    
    # Add standard/fixed allowance to make up the remaining wage
    remaining = float(monthly_wage) - total_components
    if remaining > 0:
        fixed_comp = SalaryComponent(
            employee_id=employee_id,
            component_name='Standard Allowance',
            component_type='earning',
            computation_type='fixed',
            value=remaining,
            base_component=None
        )
        fixed_comp.calculated_amount = remaining
        db.session.add(fixed_comp)
    
    db.session.commit()


def allocate_leave_for_employee(employee_id, year=None):
    """Allocate default leaves for an employee for a given year"""
    if year is None:
        year = date.today().year
    
    timeoff_types = TimeOffType.query.all()
    for timeoff_type in timeoff_types:
        existing = LeaveAllocation.query.filter_by(
            employee_id=employee_id,
            timeoff_type_id=timeoff_type.id,
            year=year
        ).first()
        
        if not existing and timeoff_type.default_allocation > 0:
            allocation = LeaveAllocation(
                employee_id=employee_id,
                timeoff_type_id=timeoff_type.id,
                year=year,
                allocated_days=timeoff_type.default_allocation
            )
            db.session.add(allocation)
    
    db.session.commit()