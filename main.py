# main.py

# Bibliotecas padrão
import os
import re
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

# Bibliotecas de terceiros
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Módulos locais
from models import User
from database import database
from config import Config
from email_utils import send_reset_email  # Envio de email real

# Inicialização do app
load_dotenv()
app = Flask(__name__)
app.config.from_object(Config)

# Setup do banco e login
database.init_app(app)
loginManager = LoginManager(app)
loginManager.login_view = 'index'

# Token Serializer para redefinição de senha
serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])

# Carregador de usuário para o Flask-Login
@loginManager.user_loader
def user_loader(user_id):
    return database.session.query(User).filter_by(id=user_id).first()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página home (pós login)
@app.route('/home')
@login_required
def home():
    return render_template('home.html', user=current_user)

# Página de configurações do usuário (opcional)
@app.route('/user-settings')
@login_required
def user_settings():
    return render_template('user-settings.html', user=current_user)

# Login
@app.route('/signIn', methods=['POST'])
def sign_in():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Todos os campos precisam ser preenchidos!", "warning")
        return redirect(url_for('index'))

    user = database.session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        flash("Email ou senha incorretos!", "danger")
        return redirect(url_for('index'))

    login_user(user)
    return redirect(url_for('home'))

# Registro
@app.route('/signUp', methods=['POST'])
def sign_up():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    if not name or not email or not password:
        flash("Todos os campos são obrigatórios!", "warning")
        return redirect(url_for('index'))

    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        flash("Formato de email inválido!", "warning")
        return redirect(url_for('index'))

    if User.query.filter_by(email=email).first():
        flash("Email já cadastrado!", "danger")
        return redirect(url_for('index'))

    if len(password) < 6:
        flash("A senha deve ter pelo menos 6 caracteres!", "warning")
        return redirect(url_for('index'))

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password_hash=hashed_password)

    database.session.add(new_user)
    database.session.commit()

    flash("Conta criada com sucesso! Faça login.", "success")
    return redirect(url_for('index'))

# Trocar senha após login
@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    if not check_password_hash(current_user.password_hash, current_password):
        flash("Senha atual incorreta!", "danger")
        return redirect(url_for('user_settings'))

    if new_password != confirm_password:
        flash("Nova senha e confirmação não conferem.", "warning")
        return redirect(url_for('user_settings'))

    if len(new_password) < 6:
        flash("A nova senha deve ter pelo menos 6 caracteres!", "warning")
        return redirect(url_for('user_settings'))

    current_user.password_hash = generate_password_hash(new_password)
    database.session.commit()
    flash("Senha atualizada com sucesso!", "success")
    return redirect(url_for('user_settings'))

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Esqueci minha senha - Solicitar reset
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = database.session.query(User).filter_by(email=email).first()

        if user:
            token = serializer.dumps(email, salt="recover-password")
            reset_link = url_for('reset_password', token=token, _external=True)
            send_reset_email(user.email, reset_link)
            flash('Instruções de recuperação de senha foram enviadas para seu email!', 'success')
        else:
            flash('Email não encontrado.', 'danger')

        return redirect(url_for('index'))

    return render_template('index.html')  # fallback para GET

# Redefinir senha via link
@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="recover-password", max_age=3600)
    except (SignatureExpired, BadSignature):
        flash('O link expirou ou é inválido.', 'danger')
        return redirect(url_for('index'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not password or not confirm_password:
            flash('Preencha todos os campos!', 'warning')
            return redirect(request.url)

        if password != confirm_password:
            flash('As senhas não conferem!', 'warning')
            return redirect(request.url)

        if len(password) < 6:
            flash('A senha deve ter no mínimo 6 caracteres!', 'warning')
            return redirect(request.url)

        user = database.session.query(User).filter_by(email=email).first()
        if user:
            user.password_hash = generate_password_hash(password)
            database.session.commit()
            flash('Senha atualizada com sucesso! Faça login.', 'success')
        else:
            flash('Usuário não encontrado.', 'danger')

        return redirect(url_for('index'))

    return render_template('reset_password.html', token=token)

# Execução
if __name__ == '__main__':
    with app.app_context():
        database.create_all()

    app.run(debug=True, host="127.0.0.1", port=5050)
