from database import database
from flask_login import UserMixin

# Definindo o modelo de dados para login
class User(UserMixin, database.Model):
    __tablename__ = 'users'

    id = database.Column(database.Integer, primary_key = True)
    name = database.Column(database.String(30), nullable = False)
    email = database.Column(database.String(30), nullable = False, unique=True)
    password = database.Column(database.String(), nullable = False)
