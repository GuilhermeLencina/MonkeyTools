# Bibliotecas padrão
import os

# Bibliotecas de terceiros
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Módulos locais
from models import User
from database import database
from config import Config

# Inicialização da aplicação Flask
app = Flask(__name__)
app.config.from_object(Config)
loginManager = LoginManager(app)
loginManager.login_view = 'index'

# Inicialização do banco de dados com a aplicação
database.init_app(app)

# Carregador de usuário (apartir do ID obtem as informações)
@loginManager.user_loader
def user_loader(id):
    user = database.session.query(User).filter_by(id=id).first()
    return user
    
# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signIn', methods=['POST'])
def sign_in():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Todos os campos precisam ser preenchidos!", "warning")
        return redirect(url_for('index'))

    user = database.session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Email ou senha incorretos!", "error")
        return redirect(url_for('index'))

    login_user(user)
    return redirect(url_for('home'))

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
        flash("Email já cadastrado!", "error")
        return redirect(url_for('index'))

    if len(password) < 6:
        flash("A senha deve ter pelo menos 6 caracteres!", "warning")
        return redirect(url_for('index'))

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)

    database.session.add(new_user)
    database.session.commit()

    flash("Conta criada com sucesso!", "success")
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Execução
if __name__ == '__main__':  
    with app.app_context():
        database.create_all()

    app.run(debug=True)