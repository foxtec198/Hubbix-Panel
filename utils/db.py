"""
Instancia o db da sessão, evita a criação de verios dbs
fazendo com que gere erro de sessões
"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
