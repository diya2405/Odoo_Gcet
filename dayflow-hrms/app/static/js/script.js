// Dayflow HRMS JavaScript Functions

// Global variables
let currentPage = 1;
let loading = false;

// Document ready function
$(document).ready(function() {
    initializeApp();
    setupEventListeners();
    setupFormValidation();
});

// Initialize application
function initializeApp() {
    // Add fade-in animation to cards
    $('.card').addClass('fade-in');
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize current time display
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    
    // Check for flash messages and auto-dismiss them
    setTimeout(function() {
        $('.alert').fadeOut();
    }, 5000);
}

// Setup event listeners
function setupEventListeners() {
    // Confirm delete actions
    $('.btn-danger[data-confirm]').on('click', function(e) {
        if (!confirm($(this).data('confirm'))) {
            e.preventDefault();
        }
    });
    
    // Loading states for buttons
    $('form').on('submit', function() {
        var $submitBtn = $(this).find('button[type="submit"]');
        $submitBtn.prop('disabled', true);
        $submitBtn.html('<span class="loading-spinner me-2"></span>Processing...');
    });
    
    // Auto-resize textareas
    $('textarea').on('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Profile picture preview
    $('#profile_picture').on('change', function(e) {
        if (e.target.files && e.target.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#profilePreview').attr('src', e.target.result).show();
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });
}

// Form validation
function setupFormValidation() {
    // Password strength indicator
    $('#password').on('input', function() {
        var password = $(this).val();
        var strength = getPasswordStrength(password);
        updatePasswordStrength(strength);
    });
    
    // Confirm password validation
    $('#confirm_password').on('input', function() {
        var password = $('#password').val();
        var confirmPassword = $(this).val();
        
        if (password !== confirmPassword) {
            $(this).addClass('is-invalid');
            $(this).next('.invalid-feedback').text('Passwords do not match');
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
        }
    });
    
    // Email validation
    $('input[type="email"]').on('blur', function() {
        var email = $(this).val();
        if (email && !isValidEmail(email)) {
            $(this).addClass('is-invalid');
            $(this).next('.invalid-feedback').text('Please enter a valid email address');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
    
    // Date validation
    $('input[type="date"]').on('change', function() {
        var selectedDate = new Date($(this).val());
        var today = new Date();
        
        if ($(this).hasClass('future-date') && selectedDate < today) {
            $(this).addClass('is-invalid');
            $(this).next('.invalid-feedback').text('Please select a future date');
        } else if ($(this).hasClass('past-date') && selectedDate > today) {
            $(this).addClass('is-invalid');
            $(this).next('.invalid-feedback').text('Please select a past date');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
}

// Utility functions
function updateCurrentTime() {
    var now = new Date();
    var timeString = now.toLocaleTimeString();
    var dateString = now.toLocaleDateString();
    
    $('#currentTime').text(timeString);
    $('#currentDate').text(dateString);
}

function getPasswordStrength(password) {
    var score = 0;
    
    // Length check
    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    
    // Character type checks
    if (/[a-z]/.test(password)) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    
    return score;
}

function updatePasswordStrength(strength) {
    var $indicator = $('#passwordStrength');
    var text = '';
    var className = '';
    
    switch (strength) {
        case 0:
        case 1:
            text = 'Very Weak';
            className = 'text-danger';
            break;
        case 2:
        case 3:
            text = 'Weak';
            className = 'text-warning';
            break;
        case 4:
        case 5:
            text = 'Good';
            className = 'text-info';
            break;
        case 6:
            text = 'Strong';
            className = 'text-success';
            break;
    }
    
    $indicator.text(text).attr('class', className);
}

function isValidEmail(email) {
    var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatTime(timeString) {
    var time = new Date('2000-01-01 ' + timeString);
    return time.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// AJAX helper functions
function showLoading() {
    $('#loadingModal').modal('show');
}

function hideLoading() {
    $('#loadingModal').modal('hide');
}

function showAlert(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var alertHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('#alertContainer').prepend(alertHTML);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').first().fadeOut();
    }, 5000);
}

// Attendance functions
function checkIn() {
    if (loading) return;
    loading = true;
    
    $.ajax({
        url: '/employee/check_in',
        type: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        success: function(data) {
            if (data.success) {
                showAlert('Checked in successfully at ' + data.time, 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert(data.message, 'error');
            }
        },
        error: function() {
            showAlert('Error during check-in. Please try again.', 'error');
        },
        complete: function() {
            loading = false;
        }
    });
}

function checkOut() {
    if (loading) return;
    loading = true;
    
    $.ajax({
        url: '/employee/check_out',
        type: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        success: function(data) {
            if (data.success) {
                showAlert(`Checked out successfully at ${data.time}. Hours worked: ${data.hours_worked}`, 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert(data.message, 'error');
            }
        },
        error: function() {
            showAlert('Error during check-out. Please try again.', 'error');
        },
        complete: function() {
            loading = false;
        }
    });
}

// Admin functions
function updateAttendance(employeeId, date, status, remarks) {
    if (loading) return;
    loading = true;
    
    $.ajax({
        url: '/admin/update_attendance',
        type: 'POST',
        data: {
            employee_id: employeeId,
            date: date,
            status: status,
            remarks: remarks
        },
        success: function(data) {
            if (data.success) {
                showAlert('Attendance updated successfully', 'success');
            } else {
                showAlert(data.message, 'error');
            }
        },
        error: function() {
            showAlert('Error updating attendance. Please try again.', 'error');
        },
        complete: function() {
            loading = false;
        }
    });
}

function approveLeave(requestId, comment = '') {
    if (loading) return;
    loading = true;
    
    $.ajax({
        url: `/admin/leave_request/${requestId}/approve`,
        type: 'POST',
        data: {
            admin_comment: comment
        },
        success: function(data) {
            if (data.success) {
                showAlert('Leave request approved successfully', 'success');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert(data.message, 'error');
            }
        },
        error: function() {
            showAlert('Error approving leave request. Please try again.', 'error');
        },
        complete: function() {
            loading = false;
        }
    });
}

function rejectLeave(requestId, comment) {
    if (loading) return;
    loading = true;
    
    $.ajax({
        url: `/admin/leave_request/${requestId}/reject`,
        type: 'POST',
        data: {
            admin_comment: comment
        },
        success: function(data) {
            if (data.success) {
                showAlert('Leave request rejected', 'info');
                setTimeout(() => location.reload(), 1500);
            } else {
                showAlert(data.message, 'error');
            }
        },
        error: function() {
            showAlert('Error rejecting leave request. Please try again.', 'error');
        },
        complete: function() {
            loading = false;
        }
    });
}

// Data table initialization
function initializeDataTable(tableId, options = {}) {
    var defaultOptions = {
        pageLength: 10,
        lengthMenu: [10, 25, 50, 100],
        order: [[0, 'desc']],
        responsive: true,
        language: {
            search: "Search:",
            lengthMenu: "Show _MENU_ entries per page",
            info: "Showing _START_ to _END_ of _TOTAL_ entries",
            infoEmpty: "Showing 0 to 0 of 0 entries",
            infoFiltered: "(filtered from _MAX_ total entries)",
            paginate: {
                first: "First",
                last: "Last",
                next: "Next",
                previous: "Previous"
            }
        }
    };
    
    var finalOptions = Object.assign(defaultOptions, options);
    
    if ($.fn.DataTable) {
        $(tableId).DataTable(finalOptions);
    }
}

// Export functions
function exportToCSV(tableId, filename) {
    var csv = [];
    var rows = document.querySelectorAll(tableId + " tr");
    
    for (var i = 0; i < rows.length; i++) {
        var row = [], cols = rows[i].querySelectorAll("td, th");
        
        for (var j = 0; j < cols.length; j++) {
            row.push(cols[j].innerText);
        }
        
        csv.push(row.join(","));
    }
    
    downloadCSV(csv.join("\n"), filename);
}

function downloadCSV(csv, filename) {
    var csvFile;
    var downloadLink;
    
    csvFile = new Blob([csv], {type: "text/csv"});
    downloadLink = document.createElement("a");
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// Print function
function printPage() {
    window.print();
}

// Theme toggle (if implemented)
function toggleTheme() {
    var body = document.body;
    body.classList.toggle('dark-theme');
    
    var isDark = body.classList.contains('dark-theme');
    localStorage.setItem('darkTheme', isDark);
}

// Initialize theme from localStorage
function initializeTheme() {
    var isDark = localStorage.getItem('darkTheme') === 'true';
    if (isDark) {
        document.body.classList.add('dark-theme');
    }
}