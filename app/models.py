from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.png')
  password = db.Column(db.String(60), nullable=False)
  newhires = db.relationship('NewHire', backref='user', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class NewHire(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  position = db.Column(db.String(100), nullable=False)
  pay_rate = db.Column(db.Float, nullable=False)
  hire_date = db.Column(db.Date, nullable=False)
  start_date = db.Column(db.Date, nullable=False)
  wisely_no = db.Column(db.Integer, nullable=False)
  date_entered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

  def __repr__(self):
    return f"NewHire('{self.first_name}', '{self.last_name}', '{self.position}',\
                        '{self.pay_rate}', '{self.hire_date}', '{self.start_date}'\
                        '{self.wisely_no}', '{self.date_entered}')"
