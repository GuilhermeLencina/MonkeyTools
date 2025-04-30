# models.py

from database import database
from flask_login import UserMixin

class User(UserMixin, database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), nullable=False)
    email = database.Column(database.String(255), unique=True, nullable=False)
    password_hash = database.Column(database.Text, nullable=False)  # Corrigido!
    created_at = database.Column(database.DateTime, server_default=database.func.now())
    updated_at = database.Column(database.DateTime, onupdate=database.func.now())
    is_active = database.Column(database.Boolean, default=True)
    last_login = database.Column(database.DateTime)
    reset_password_token = database.Column(database.Text)
    reset_password_expires = database.Column(database.DateTime)
