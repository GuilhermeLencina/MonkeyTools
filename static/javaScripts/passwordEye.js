// Sign In
const togglePassword = document.querySelector('#togglePassword');
const password = document.querySelector('#password');

if (togglePassword && password) {
    togglePassword.addEventListener('click', function () {
        const type = password.type === 'password' ? 'text' : 'password';
        password.type = type;
        this.classList.toggle('bxs-lock-alt');
        this.classList.toggle('bxs-lock-open-alt');
    });
}

// Sign Up
const toggleRegisterPassword = document.querySelector('#toggleRegisterPassword');
const registerPassword = document.querySelector('#registerPassword');

if (toggleRegisterPassword && registerPassword) {
    toggleRegisterPassword.addEventListener('click', function () {
        const type = registerPassword.type === 'password' ? 'text' : 'password';
        registerPassword.type = type;
        this.classList.toggle('bxs-lock-alt');
        this.classList.toggle('bxs-lock-open-alt');
    });
}