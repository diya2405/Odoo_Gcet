# Quick Admin Guide - Leave & Payroll Management

## 🔍 Viewing Medical Certificates

### From Leave Requests Table
1. Go to **Admin Dashboard** → **Leave Requests**
2. Look for the **"Medical Cert"** column
3. If a certificate is uploaded, you'll see a green **"View"** button with a PDF icon
4. Click the button to download and view the certificate

### From Leave Request Details
1. Click **"View"** button on any leave request row
2. A modal opens with full leave details
3. If it's a sick leave with certificate, you'll see **"View Medical Certificate"** button at the bottom
4. Click to download in a new tab

### Tips:
- ✅ Only sick leave requests will have medical certificates
- ✅ Certificates open in a new tab for easy viewing
- ✅ All certificates are securely stored and accessible only to admins

---

## 💰 Creating Payroll with Unpaid Leave Deductions

### Step 1: Navigate to Payroll
1. Go to **Admin Dashboard** → **Payroll Management**
2. Click **"Generate Payroll"** button

### Step 2: Select Employee & Period
1. Choose **Employee** from dropdown
2. Set **Pay Period Start Date**
3. Set **Pay Period End Date**
4. Enter **Total Working Days** (e.g., 22 for monthly)
5. Enter **Days Present**

### Step 3: System Auto-Calculates
The system automatically:
- ✅ Fetches employee's base salary
- ✅ Calculates basic salary (50% of wage)
- ✅ Calculates HRA (50% of basic)
- ✅ **Counts unpaid leave days** in the selected period
- ✅ **Calculates unpaid leave deduction**
- ✅ Calculates PF (12% of basic)
- ✅ Adds professional tax (₹200)

### Step 4: Add Increments/Bonuses (Optional)
- **Increment Amount**: Enter fixed increment amount (e.g., ₹5000)
- **Increment %**: Enter percentage increase
- **Special Bonus**: One-time bonuses
- **Festival Bonus**: Diwali, New Year bonuses
- **Other Earnings**: Any additional earnings

### Step 5: Review & Save
- Check **Gross Pay** (total earnings)
- Check **Unpaid Leave Deduction** (auto-calculated)
- Check **Total Deductions**
- Verify **Net Pay** (take-home salary)
- Click **"Create Payroll"**

---

## 📊 Understanding Salary Breakdown

### Earnings Section
```
Base Monthly Salary:     ₹50,000
Basic Salary (50%):      ₹25,000
HRA (50% of basic):      ₹12,500
Standard Allowance:      ₹5,000
Performance Bonus:       ₹3,000
Increment:               ₹2,000
Special Bonus:           ₹5,000
-----------------------------------
GROSS PAY:               ₹1,02,500
```

### Deductions Section
```
PF (12% of basic):       ₹3,000
Professional Tax:        ₹200
TDS:                     ₹2,000
Unpaid Leave (2 days):   ₹4,545  ← Auto-calculated!
-----------------------------------
TOTAL DEDUCTIONS:        ₹9,745
```

### Final Calculation
```
Gross Pay:               ₹1,02,500
(-) Total Deductions:    ₹9,745
===================================
NET PAY:                 ₹92,755
```

---

## 🎯 Unpaid Leave Deduction Formula

```
Per Day Salary = Base Monthly Salary ÷ Total Working Days
Unpaid Leave Deduction = Per Day Salary × Unpaid Leave Days
```

### Example:
- Base Salary: ₹50,000
- Working Days: 22
- Unpaid Leave: 2 days

**Calculation:**
- Per Day = ₹50,000 ÷ 22 = ₹2,272.73
- Deduction = ₹2,272.73 × 2 = **₹4,545.46**

---

## ✅ Best Practices

### For Leave Approval
1. **Always check medical certificates** for sick leave
2. Verify certificate is from registered practitioner
3. Check if dates match leave request
4. Look for hospital/clinic stamp
5. Approve only if certificate is valid

### For Payroll Creation
1. **Process at end of month** for accurate leave count
2. **Verify attendance** before creating payroll
3. **Double-check unpaid leaves** - system shows count
4. **Add increments** separately if applicable
5. **Review calculations** before finalizing

### For Record Keeping
1. Download important medical certificates
2. Keep payroll records for audit
3. Track increment history
4. Monitor leave patterns
5. Generate reports regularly

---

## 🚨 Common Issues & Solutions

### Issue: Can't see medical certificate
**Solution**: Only sick leave requests have certificates. Check leave type badge.

### Issue: Unpaid leave deduction seems wrong
**Solution**: 
- Verify total working days is correct (usually 22-26)
- Check if leave was actually approved as "unpaid" type
- System only counts approved unpaid leaves in the pay period

### Issue: Net salary is negative
**Solution**: 
- Check if employee had excessive unpaid leaves
- Review all deduction amounts
- Verify base salary is set correctly

### Issue: Can't download certificate
**Solution**:
- Ensure file was uploaded successfully
- Check server permissions on uploads folder
- Verify certificate file exists

---

## 📞 Support

For technical issues or questions:
- Check documentation: `LEAVE_AND_PAYROLL_ENHANCEMENTS.md`
- Review error logs in application
- Contact system administrator

---

**Quick Tips:**
- 🎯 Always approve leaves before generating payroll
- 💡 Medical certificates are mandatory for sick leave
- ⚡ Unpaid leave deductions are automatic - just select pay period
- 🔒 All medical documents are secure and admin-only
- 📊 Review salary breakdown before finalizing payroll

---

**Last Updated**: January 3, 2026
