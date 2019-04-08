from app import app, db, login_manager
#from app import google_bp as blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc  import NoResultFound
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Formerly username
    email = db.Column(db.String(256), unique=True) 
    f_name = db.Column(db.String(30))
    username = db.Column(db.String(256))
    profile_photo = db.Column(db.LargeBinary)
    algo = db.Column(db.LargeBinary)

    books = relationship(User_Books, back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.email)

class User_Books(db.Model):
    # Concatenation of volume_id and a users id
    volume_user = db.Column(db.String(256), primary_key=True)
    volume = db.Column(db.String(256))

    user_rating = db.Column(db.Integer)
    user_pred = db.Column(db.Float)

    user = relationship(User, back_populates="books")

class Club_Books(db.Model):
     # Concatenation of volume_id and a club id
     volume_club = db.Column(db.String(256), primary_key=True)
     volume = db.Column(db.String(256))

     club_pred = db.Column(db.Float)

     club = relationship(Book_Club, back_populates="books")

class Book_Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    pres_id = db.Column(db.Integer, db.ForeignKey(User.id))
    host_id = db.Column(db.Integer, db.ForeignKey(User.id))

    name = db.Column(db.String(256))

    forums = relationship(Forums, back_populates="club")
    books = relationship(Club_Books, back_populates="club")

class Forums(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    club = relationship(Book_Club, back_populates="forums")
    posts = relationship(Posts, back_populates="forum")

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    author = db.Column(db.Integer, db.ForeignKey(user.id))
    post = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    forum = relationship(Forums, back_populates="posts")

class OAuth(db.Model, OAuthConsumerMixin):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
