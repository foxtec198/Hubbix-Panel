from models.base_model import BaseModel, db

class Partnership(BaseModel):
    __tablename__ = "partnership"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)