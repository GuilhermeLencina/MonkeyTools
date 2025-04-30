// Seletores principais
const container = document.querySelector('.container');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

// Caixas de formulário
const loginBox = document.querySelector('.form-box.login');
const registerBox = document.querySelector('.form-box.register');
const forgotBox = document.querySelector('.form-box.forgot');

// Funções para alternar telas
function showLogin() {
  if (loginBox && registerBox && forgotBox) {
    loginBox.style.display = 'block';
    registerBox.style.display = 'none';
    forgotBox.style.display = 'none';
  }
}

function showRegister() {
  if (loginBox && registerBox && forgotBox) {
    loginBox.style.display = 'none';
    registerBox.style.display = 'block';
    forgotBox.style.display = 'none';
  }
}

function showForgot() {
  if (loginBox && registerBox && forgotBox) {
    loginBox.style.display = 'none';
    registerBox.style.display = 'none';
    forgotBox.style.display = 'block';
  }
}

// Evento para abrir o modal (botão "Login")
if (btnPopup) {
  btnPopup.addEventListener('click', () => {
    container.classList.add('active-popup');
    showLogin();
  });
}

// Evento para fechar o modal (ícone "X")
if (iconClose) {
  iconClose.addEventListener('click', () => {
    container.classList.remove('active-popup');
  });
}

// Evento de troca para Sign Up
document.querySelectorAll('.register-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    showRegister();
  });
});

// Eventos de retorno para Sign In
document.querySelectorAll('.login-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    showLogin();
  });
});

// Evento de troca para Forgot Password
document.querySelectorAll('.forgot-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    showForgot();
  });
});

// Exibir login automaticamente ao abrir a página
window.addEventListener('DOMContentLoaded', () => {
  container.classList.add('active-popup');
  showLogin();
});
