from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subdomain = db.Column(db.String(50), unique=True)
    custom_domain = db.Column(db.String(255), unique=True, nullable=True)
    template = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)