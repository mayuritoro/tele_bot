
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tele_bot.db'
db = SQLAlchemy(app)

class user_info(db.Model):
    mobile_no = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)

#db.create_all()