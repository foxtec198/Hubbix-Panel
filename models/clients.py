from models.base_model import BaseModel, db
from datetime import datetime as dt

class Client(BaseModel):
    __tablename__ = "clients"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    subdomain = db.Column(db.String(50), unique=True)
    custom_domain = db.Column(db.String(255), unique=True, nullable=True)
    template = db.Column(db.String(100))
    active = db.Column(db.Boolean, default=True)
    partnership_id = db.Column(db.Integer, default=0)
    gtag = db.Column(db.String)
    pixel = db.Column(db.String)
    tel = db.Column(db.String)
    logo = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=dt.utcnow)

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def _search_by_partnership(cls, partnership_id):
        clients = cls.query.filter(cls.partnership_id == partnership_id).all()
        return [c.to_dict() for c in clients]

    @classmethod 
    def _get_all_clients(cls):
        clients = cls.query.all()
        return [c.to_dict() for c in clients]