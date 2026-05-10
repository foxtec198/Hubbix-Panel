from models.base_model import BaseModel, db
from datetime import datetime as dt

class Events(BaseModel):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    partnership_id = db.Column(db.Integer, nullable=False)
    ip = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=dt.utcnow)
    user_agent = db.Column(db.String, nullable=False, default="Não Informado")
    type = db.Column(db.String, nullable=False)

    @classmethod
    def _get_all_views(cls):
        views = cls.query.filter(
            cls.type == "VIEW"
        ).all()
        return [v.to_dict() for v in views]

    @classmethod
    def _get_count_all_views(cls):
        views = cls.query.filter(
            cls.type == "VIEW"
        ).all()
        return len(views)

    @classmethod
    def _get_count_views_by_client(cls, client_id):
        views = cls.query.filter(
            cls.type == "VIEW", 
            cls.client_id == client_id
        ).all()
        return len(views)

    @classmethod
    def _get_count_views_by_partnership(cls, partnership_id):
        views = cls.query.filter(
            cls.type == "VIEW", 
            cls.partnership_id == partnership_id
        ).all()
        return len(views)

    @classmethod
    def _get_all_clicks(cls):
        clicks = cls.query.filter(
            cls.type == "CLICK"
        ).all()
        return [c.to_dict() for c in clicks]

    @classmethod
    def _get_count_all_clicks(cls):
        clicks = cls.query.filter(
            cls.type == "CLICK"
        ).all()
        return len(clicks)

    @classmethod
    def _get_count_clicks_by_client(cls, client_id):
        clicks = cls.query.filter(
            cls.type == "CLICK", 
            cls.client_id == client_id
        ).all()
        return len(clicks)

    @classmethod
    def _get_count_clicks_by_partnership(cls, partnership_id):
        clicks = cls.query.filter(
            cls.type == "CLICK", 
            cls.partnership_id == partnership_id
        ).all()
        return len(clicks)
