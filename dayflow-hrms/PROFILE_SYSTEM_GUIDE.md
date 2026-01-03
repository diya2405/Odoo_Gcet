# Enhanced Profile System - Implementation Guide

## 🎉 New Features Implemented

### 1. **Three-Tab Profile Interface**
The employee profile has been reorganized into three comprehensive tabs:

#### Tab 1: Personal Information
- Basic information (name, email, phone, DOB)
- Gender and marital status
- Address and nationality
- Emergency contact details
- Bank account information
- Government IDs (PAN, UAN)
- Skills and interests

#### Tab 2: Company Data
- Employee ID and role
- Department and position
- Hire date and work schedule
- Salary information (monthly and annual CTC)
- Working hours and days
- Reporting structure (manager)

#### Tab 3: Documents & Certificates
- Resume upload/download/delete
- Certificate management system with:
  - Certificate name and file
  - Issuing organization
  - Issue and expiry dates
  - Description
  - File size display
  - Upload/download/delete capabilities
  - Visual expiry indicators

### 2. **Resume Management**
- Upload resume in PDF, DOC, or DOCX format
- Maximum file size: 10MB
- Download and delete functionality
- Replace existing resume anytime
- Accessible from profile and edit profile pages

### 3. **Certificate Management**
- Upload multiple certificates
- Supported formats: PDF, DOC, DOCX
- Track certificate details:
  - Certificate name
  - Issuing organization
  - Issue date and expiry date
  - Description
- Visual indicators for expired certificates
- Individual download and delete options
- Compressed file size display

### 4. **Enhanced Signup Process**
Additional fields during registration:
- Phone number
- Personal email
- Date of birth
- Gender
- Address

These fields can also be left empty and filled later from the profile edit page.

### 5. **Profile Picture Improvements**
- Proper file upload handling
- Image preview before upload
- Support for PNG, JPG, JPEG, GIF
- Maximum file size: 10MB
- Stored in organized directory structure
- Circular display with border styling

## 📁 File Structure

```
dayflow-hrms/
├── app/
│   ├── models.py                          # Updated with Certificate model
│   ├── routes/
│   │   ├── employee.py                    # Enhanced with file upload routes
│   │   └── auth.py                        # Updated signup with personal info
│   └── templates/
│       ├── employee/
│       │   ├── profile.html               # New three-tab interface
│       │   └── edit_profile.html          # Comprehensive edit form
│       └── auth/
│           └── signup.html                # Enhanced signup form
└── uploads/                               # File storage
    ├── profiles/                          # Profile pictures
    ├── documents/                         # Resumes
    └── certificates/                      # Certificates
```

## 🚀 Installation & Setup

### Step 1: Update the Database

Run the database update script:

```bash
cd dayflow-hrms
python update_database.py
```

This will:
- Add the `certificates` table
- Create necessary upload directories
- Update the database schema

### Step 2: Verify Directory Structure

Ensure these directories exist:
```
uploads/
├── profiles/
├── documents/
└── certificates/
```

### Step 3: Test the Application

1. Start the application:
```bash
python run.py
```

2. Navigate to http://localhost:5000

## 💡 Usage Guide

### For Employees

#### Updating Profile
1. Click "My Profile" from the dashboard
2. Click "Edit Profile" button
3. Fill in personal information
4. Upload profile picture (optional)
5. Upload resume (optional)
6. Click "Save Changes"

#### Managing Certificates
1. Go to "My Profile"
2. Click the "Documents & Certificates" tab
3. Click "Upload Certificate" button
4. Fill in certificate details:
   - Certificate name (required)
   - Upload file (required)
   - Issuing organization (optional)
   - Issue/expiry dates (optional)
   - Description (optional)
5. Click "Upload"

#### Deleting Files
- **Resume**: Click the red "Delete" button next to your resume
- **Certificates**: Click "Delete" on any certificate card
- **Profile Picture**: Upload a new picture to replace the old one

### For New Users

#### During Signup
1. Fill in required fields:
   - Employee ID
   - Email
   - First & Last Name
   - Department
   - Position
   - Password

2. Optionally fill in:
   - Phone number
   - Personal email
   - Date of birth
   - Gender
   - Address

3. Complete signup and login

4. Upload certificates anytime from profile page

## 🔒 Security Features

- File type validation (only allowed extensions)
- File size limits (10MB max)
- Secure filename handling
- Organized file storage by type
- Proper file deletion on replace/remove
- User-specific file access control

## 📊 Database Schema Updates

### New Certificate Model
```python
- id: Primary key
- employee_id: Foreign key to Employee
- certificate_name: String (required)
- certificate_file: String (file path)
- issue_date: Date (optional)
- expiry_date: Date (optional)
- issuing_organization: String (optional)
- description: Text (optional)
- file_size: Integer (bytes)
- uploaded_at: DateTime
```

### Updated Employee Model
```python
Added fields:
- emergency_contact_name
- emergency_contact_phone
- emergency_contact_relationship
- profile_picture (enhanced)
- resume (enhanced)
```

## 🎨 UI/UX Improvements

- **Sticky Sidebar**: Profile picture and basic info stay visible while scrolling
- **Tab Navigation**: Easy switching between information categories
- **Visual Indicators**: Badge colors for certificate status (valid/expired)
- **Responsive Design**: Works on desktop and mobile devices
- **File Size Display**: Human-readable file sizes (KB, MB)
- **Loading States**: Spinner during file uploads
- **Confirmation Dialogs**: Prevent accidental deletions

## 🔧 API Endpoints

### Employee Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/employee/profile` | View profile with three tabs |
| GET/POST | `/employee/edit_profile` | Edit profile and upload files |
| POST | `/employee/upload_certificate` | Upload new certificate |
| POST | `/employee/delete_certificate/<id>` | Delete specific certificate |
| POST | `/employee/delete_resume` | Delete resume |
| GET | `/employee/download/<type>/<filename>` | Download files |

## ⚙️ Configuration

### File Upload Settings
Located in `app/routes/employee.py`:

```python
ALLOWED_EXTENSIONS_IMAGE = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_EXTENSIONS_DOCUMENT = {'pdf', 'doc', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
```

## 🐛 Troubleshooting

### Issue: Upload directories not found
**Solution**: Run `python update_database.py` to create directories

### Issue: Files not uploading
**Solution**: Check file size (max 10MB) and format (PDF, DOC, DOCX for documents)

### Issue: Profile picture not displaying
**Solution**: 
1. Verify file is in `uploads/profiles/` directory
2. Check file path in database
3. Ensure file extensions are lowercase

### Issue: Certificate model not found
**Solution**: Run `python update_database.py` to update schema

## 📝 Notes

1. **File Storage**: All files are stored locally in the `uploads/` directory. Consider cloud storage for production.

2. **Database Backup**: Always backup your database before running updates.

3. **Permissions**: Ensure the application has write permissions to the `uploads/` directory.

4. **File Cleanup**: Old files are automatically deleted when replaced or removed.

5. **Validation**: Both frontend and backend validation ensure data integrity.

## 🔄 Future Enhancements

Possible additions:
- Cloud storage integration (AWS S3, Azure Blob)
- Image compression for profile pictures
- Bulk certificate upload
- Certificate expiry notifications
- Document versioning
- Audit trail for file changes

## 📞 Support

For issues or questions about the enhanced profile system, refer to:
- Database models in `app/models.py`
- Route handlers in `app/routes/employee.py`
- Templates in `app/templates/employee/`

---

**Version**: 2.0
**Last Updated**: January 2026
**Status**: ✅ Production Ready
