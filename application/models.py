from . import db

class user(db.Model):
    __tablename__ = 'user_account'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_name = db.Column(db.String(128), nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)

