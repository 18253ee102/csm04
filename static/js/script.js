document.addEventListener('DOMContentLoaded', function () {
    var analyzeForm = document.getElementById('analyzeForm');
    
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevents the default form submission behavior
            var url = document.getElementById('keyword').value;
            console.log('Entered URL:', url); // Log the URL to the console
            localStorage.setItem('analyzedUrl', url); // Store the URL in localStorage
            window.location.href = 'templates/new_page.html'; // Redirect to the new_page.html
        });
    }
});
