document.addEventListener('DOMContentLoaded', function() {
    const password = document.getElementById('password');
    const password2 = document.getElementById('password2');

    if (password2) {
        password2.addEventListener('input', function() {
            if (password.value !== password2.value) {
                password2.setCustomValidity('Passwords do not match');
            } else {
                password2.setCustomValidity('');
            }
        });
    }
});


function cancelLogout() {
    window.location.href = baseUrl;
}
