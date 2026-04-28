/**
 * Auto Remediation - Stuck Thread Manager
 * Frontend JavaScript Application
 */

// API Base URL
const API_BASE_URL = 'http://localhost:8000/api';
let currentJobId = null;
let jobsData = [];

// ===== Initialization =====
$(document).ready(function() {
    console.log('Application initialized');
    
    // Initialize event listeners
    initializeEventListeners();
    
    // Load initial data
    checkSystemHealth();
    loadDashboard();
    
    // Auto-refresh jobs every 5 seconds
    setInterval(refreshJobs, 5000);
});

// ===== Event Listeners =====
function initializeEventListeners() {
    // Tab switching
    $('.tab-button').click(function() {
        const tabName = $(this).attr('data-tab');
        switchTab(tabName);
    });

    // Form submission
    $('#restartForm').submit(function(e) {
        e.preventDefault();
        submitRestartJob();
    });

    // Escalation level slider
    $('#escalationLevel').on('input', function() {
        const level = $(this).val();
        $('#selectedLevel').text(`Level: ${level}`);
    });

    // Health check button
    $('#healthCheckBtn').click(function() {
        checkSystemHealth();
    });
}

// ===== Tab Management =====
function switchTab(tabName) {
    // Hide all tabs
    $('.tab-content').removeClass('active');
    $('.tab-button').removeClass('active');

    // Show selected tab
    $(`#${tabName}`).addClass('active');
    $(`[data-tab="${tabName}"]`).addClass('active');

    // Load data for specific tabs
    if (tabName === 'jobs-list') {
        refreshJobs();
    } else if (tabName === 'analytics') {
        loadAnalytics();
    } else if (tabName === 'dashboard') {
        loadDashboard();
    }
}

// ===== API Functions =====
async function submitRestartJob() {
    const formData = {
        environment: $('#environment').val(),
        server_name: $('#serverName').val() || null,
        reason: $('#reason').val() || null,
        escalation_level: parseInt($('#escalationLevel').val())
    };

    if (!formData.environment) {
        showToast('Please select an environment', 'error');
        return;
    }

    try {
        showSpinner();
        
        const response = await $.ajax({
            url: `${API_BASE_URL}/ansible/jobs/restart`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData)
        });

        console.log('Job created:', response);

        // Display analysis
        if (response.llm_analysis) {
            $('#analysisText').text(response.llm_analysis);
            $('#analysisResult').show();
        }

        // Show success message
        showToast(`Job created successfully: ${response.job_id}`, 'success');

        // Reset form
        $('#restartForm')[0].reset();
        $('#selectedLevel').text('Level: 1');

        // Redirect to jobs list
        setTimeout(() => {
            switchTab('jobs-list');
            refreshJobs();
        }, 2000);

    } catch (error) {
        console.error('Error creating job:', error);
        showToast('Error creating restart job: ' + (error.responseJSON?.detail || error.statusText), 'error');
    }
}

async function checkSystemHealth() {
    try {
        const response = await $.ajax({
            url: `${API_BASE_URL}/health`,
            type: 'GET'
        });

        console.log('Health check:', response);

        // Update health indicator
        $('#healthStatus')
            .addClass('online')
            .removeClass('offline')
            .text('● System Healthy');

        // Update system status table
        displaySystemStatus(response.services);
        
        showToast('System health check completed', 'success');

    } catch (error) {
        console.error('Health check failed:', error);
        $('#healthStatus')
            .addClass('offline')
            .removeClass('online')
            .text('● System Offline');
        
        showToast('Unable to reach API server', 'error');
    }
}

async function refreshJobs() {
    try {
        const environment = $('#environmentFilter').val();
        const url = environment 
            ? `${API_BASE_URL}/ansible/jobs?environment=${environment}`
            : `${API_BASE_URL}/ansible/jobs`;

        const response = await $.ajax({
            url: url,
            type: 'GET'
        });

        console.log('Jobs refreshed:', response);

        jobsData = response;
        displayJobs(response);
        updateJobStats(response);

    } catch (error) {
        console.error('Error refreshing jobs:', error);
        showToast('Error loading jobs', 'error');
    }
}

async function getJobStatus(jobId) {
    try {
        const response = await $.ajax({
            url: `${API_BASE_URL}/ansible/jobs/${jobId}/status`,
            type: 'GET'
        });

        return response;

    } catch (error) {
        console.error('Error getting job status:', error);
        return null;
    }
}

async function loadJobLogs() {
    if (!currentJobId) return;

    try {
        showSpinner();

        const response = await $.ajax({
            url: `${API_BASE_URL}/ansible/jobs/${currentJobId}/logs`,
            type: 'GET'
        });

        $('#logsContent').text(response.logs);
        closeModal();
        $('#logsModal').show();

    } catch (error) {
        console.error('Error loading logs:', error);
        showToast('Error loading job logs', 'error');
    }
}

async function cancelJob() {
    if (!currentJobId) return;

    if (!confirm('Are you sure you want to cancel this job?')) {
        return;
    }

    try {
        const response = await $.ajax({
            url: `${API_BASE_URL}/ansible/jobs/${currentJobId}/cancel`,
            type: 'POST'
        });

        showToast('Job cancelled successfully', 'success');
        closeModal();
        refreshJobs();

    } catch (error) {
        console.error('Error cancelling job:', error);
        showToast('Error cancelling job: ' + (error.responseJSON?.detail || error.statusText), 'error');
    }
}

async function showEnvironments() {
    try {
        const response = await $.ajax({
            url: `${API_BASE_URL}/environments`,
            type: 'GET'
        });

        alert('Supported Environments:\n' + response.supported_environments.join('\n'));

    } catch (error) {
        console.error('Error loading environments:', error);
        showToast('Error loading environments', 'error');
    }
}

// ===== Display Functions =====
function displayJobs(jobs) {
    if (!jobs || jobs.length === 0) {
        $('#jobsList').html('<p class="text-center" style="padding: 40px;">No jobs found</p>');
        return;
    }

    let html = `
        <table>
            <thead>
                <tr>
                    <th>Job ID</th>
                    <th>Environment</th>
                    <th>Server</th>
                    <th>Status</th>
                    <th>Created</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
    `;

    jobs.forEach(job => {
        const createdAt = new Date(job.created_at).toLocaleString();
        const statusClass = `status-${job.status}`;

        html += `
            <tr>
                <td><strong>${job.id}</strong></td>
                <td>${job.environment}</td>
                <td>${job.server}</td>
                <td><span class="status-badge ${statusClass}">${job.status}</span></td>
                <td>${createdAt}</td>
                <td>
                    <div class="job-action">
                        <button class="btn btn-info" onclick="viewJobDetails('${job.id}')">Details</button>
                        <button class="btn btn-secondary" onclick="refreshJobStatus('${job.id}')">Refresh</button>
                    </div>
                </td>
            </tr>
        `;
    });

    html += `
            </tbody>
        </table>
    `;

    $('#jobsList').html(html);
}

function displaySystemStatus(services) {
    if (!services) return;

    let html = `
        <table>
            <thead>
                <tr>
                    <th>Service</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (const [service, status] of Object.entries(services)) {
        const statusClass = status === 'operational' || status === 'ready' ? 'success' : 'error';
        const statusBadge = status === 'operational' || status === 'ready' ? '✓' : '✗';

        html += `
            <tr>
                <td><strong>${service}</strong></td>
                <td><span class="status-badge status-${statusClass}">${statusBadge} ${status}</span></td>
            </tr>
        `;
    }

    html += `
            </tbody>
        </table>
    `;

    $('#systemStatus').html(html);
}

async function viewJobDetails(jobId) {
    currentJobId = jobId;

    try {
        const job = await getJobStatus(jobId);

        if (!job) {
            showToast('Job not found', 'error');
            return;
        }

        const createdAt = new Date(job.created_at).toLocaleString();
        const updatedAt = new Date(job.updated_at).toLocaleString();

        let html = `
            <div>
                <p><strong>Job ID:</strong> ${job.id}</p>
                <p><strong>Template:</strong> ${job.template_name}</p>
                <p><strong>Environment:</strong> ${job.environment}</p>
                <p><strong>Server:</strong> ${job.server}</p>
                <p><strong>Status:</strong> <span class="status-badge status-${job.status}">${job.status}</span></p>
                <p><strong>Created:</strong> ${createdAt}</p>
                <p><strong>Updated:</strong> ${updatedAt}</p>
                <p><strong>Duration:</strong> ${job.duration}s</p>
                ${job.reason ? `<p><strong>Reason:</strong> ${job.reason}</p>` : ''}
                ${job.output ? `<p><strong>Output:</strong> ${job.output}</p>` : ''}
                ${job.error ? `<p><strong>Error:</strong> <span style="color: red;">${job.error}</span></p>` : ''}
            </div>
        `;

        $('#modalBody').html(html);

        // Show/hide cancel button based on status
        if (job.status === 'running' || job.status === 'pending') {
            $('#cancelJobBtn').show();
        } else {
            $('#cancelJobBtn').hide();
        }

        $('#jobModal').show();

    } catch (error) {
        console.error('Error viewing job details:', error);
        showToast('Error loading job details', 'error');
    }
}

async function refreshJobStatus(jobId) {
    try {
        const job = await getJobStatus(jobId);
        if (job) {
            showToast(`Job status: ${job.status}`, 'info');
        }
        refreshJobs();
    } catch (error) {
        console.error('Error refreshing job status:', error);
    }
}

function updateJobStats(jobs) {
    if (!jobs) jobs = [];

    const stats = {
        active: jobs.filter(j => j.status === 'running' || j.status === 'pending').length,
        success: jobs.filter(j => j.status === 'success').length,
        failed: jobs.filter(j => j.status === 'failed' || j.status === 'error').length,
        pending: jobs.filter(j => j.status === 'pending').length
    };

    $('#activeJobsCount').text(stats.active);
    $('#successCount').text(stats.success);
    $('#failedCount').text(stats.failed);
    $('#pendingCount').text(stats.pending);
}

async function loadDashboard() {
    await refreshJobs();
    await checkSystemHealth();
}

async function loadAnalytics() {
    updateJobStats(jobsData);

    // Calculate statistics
    if (jobsData.length > 0) {
        const totalJobs = jobsData.length;
        const successJobs = jobsData.filter(j => j.status === 'success').length;
        const successRate = ((successJobs / totalJobs) * 100).toFixed(1);
        
        const totalDuration = jobsData.reduce((sum, j) => sum + (j.duration || 0), 0);
        const avgDuration = jobsData.length > 0 ? (totalDuration / jobsData.length).toFixed(0) : 0;

        $('#totalJobs').text(totalJobs);
        $('#successRate').text(successRate + '%');
        $('#avgDuration').text(avgDuration + 's');
    }
}

// ===== Modal Functions =====
function closeModal() {
    $('#jobModal').hide();
    currentJobId = null;
}

function closeLogsModal() {
    $('#logsModal').hide();
}

// Close modal when clicking outside
$(window).click(function(event) {
    const modal = $('#jobModal')[0];
    const logsModal = $('#logsModal')[0];

    if (event.target === modal) {
        closeModal();
    }
    if (event.target === logsModal) {
        closeLogsModal();
    }
});

// ===== Notification Functions =====
function showToast(message, type = 'info') {
    const toast = $('#toast');
    toast.text(message).removeClass('success error warning info').addClass(type);
    toast.show();

    setTimeout(() => {
        toast.hide();
    }, 3000);
}

function showSpinner() {
    // Show spinner in appropriate container
    console.log('Loading...');
}

// ===== Utility Functions =====
function formatDate(dateString) {
    return new Date(dateString).toLocaleString();
}

function getStatusColor(status) {
    const colors = {
        'pending': '#f39c12',
        'running': '#3498db',
        'success': '#2ecc71',
        'failed': '#e74c3c',
        'error': '#e74c3c',
        'cancelled': '#95a5a6'
    };

    return colors[status] || '#95a5a6';
}

// Export functions for global access
window.switchTab = switchTab;
window.submitRestartJob = submitRestartJob;
window.checkSystemHealth = checkSystemHealth;
window.refreshJobs = refreshJobs;
window.cancelJob = cancelJob;
window.closeModal = closeModal;
window.closeLogsModal = closeLogsModal;
window.viewJobDetails = viewJobDetails;
window.loadJobLogs = loadJobLogs;
window.refreshJobStatus = refreshJobStatus;
window.showEnvironments = showEnvironments;

console.log('✓ Frontend application loaded successfully');
