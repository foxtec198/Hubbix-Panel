from models.base_model import BaseModel, db

class Member(BaseModel):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    join_date = db.Column(db.Date, nullable=False)
    active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime, nullable=True)
    partnership_id = db.Column(db.Integer)

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
