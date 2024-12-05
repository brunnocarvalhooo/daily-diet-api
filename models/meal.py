from sqlalchemy.orm import relationship

from database import db


class Meal(db.Model):
    __tablename__ = "meals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    datetime = db.Column(db.DateTime, nullable=False)
    in_diet = db.Column(db.Boolean, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = relationship("User", back_populates="meals")
