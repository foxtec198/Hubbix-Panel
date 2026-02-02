from models.base_model import BaseModel, db

class Client(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subdomain = db.Column(db.String(50), unique=True)
    custom_domain = db.Column(db.String(255), unique=True, nullable=True)
    template = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    partnership_id = db.Column(db.Integer, default=1)