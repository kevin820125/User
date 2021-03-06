from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__  = 'users'
    username = db.Column(db.Text , 
                 primary_key = True,
                 unique=True,
                 nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email= db.Column(db.Text, nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)

    @classmethod
    def register(cls , username ,password,first_name, last_name, email):
        hashed = bcrypt.generate_password_hash(password).decode('utf8')
        return cls(username = username , password = hashed,
         first_name=first_name,last_name=last_name,email=email)


    @classmethod
    def authentication(cls , username , password):
        u = User.query.filter_by(username = username).first()
        if u and bcrypt.check_password_hash(u.password , password):
            return u
        else:
            return False

class FeedBack(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'),
        nullable=False,)
    user = db.relationship('User' , backref = 'feedback')
