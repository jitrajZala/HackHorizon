// Main JavaScript file for the College Hackathon Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Countdown timer for active hackathons
    const countdownElements = document.querySelectorAll('.hackathon-countdown');
    countdownElements.forEach(function(element) {
        const endDate = new Date(element.getAttribute('data-end-date')).getTime();
        
        const countdownInterval = setInterval(function() {
            const now = new Date().getTime();
            const distance = endDate - now;
            
            if (distance < 0) {
                clearInterval(countdownInterval);
                element.innerHTML = "Hackathon has ended";
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            element.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }, 1000);
    });

    // Form validation for submission form
    const submissionForm = document.getElementById('submission-form');
    if (submissionForm) {
        submissionForm.addEventListener('submit', function(event) {
            const githubLink = document.getElementById('id_github_link').value;
            if (!githubLink.includes('github.com')) {
                event.preventDefault();
                alert('Please enter a valid GitHub repository URL');
            }
        });
    }

    // Team member invitation form
    const inviteForm = document.getElementById('invite-form');
    if (inviteForm) {
        inviteForm.addEventListener('submit', function(event) {
            const emailInput = document.getElementById('id_email').value;
            if (!emailInput.includes('@')) {
                event.preventDefault();
                alert('Please enter a valid email address');
            }
        });
    }
});