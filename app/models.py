from app import app, db, login_manager
#from app import google_bp as blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc  import NoResultFound
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # Formerly username
    email = db.Column(db.String(256), unique=True) 
    f_name = db.Column(db.String(30))
    username = db.Column(db.String(256))
    profile_photo = db.Column(db.LargeBinary)
    algo = db.Column(db.LargeBinary, nullable=True)

    user_books = db.relationship('User_Books', backref=db.backref('book_user'))
    clubs = db.relationship('Bookclub', secondary='club_members', lazy='subquery', backref=db.backref('club_users'))

    def __repr__(self):
        return '<User {}>'.format(self.email)
                    
class User_Books(db.Model):
    __tablename__ = 'user_books'
    # Concatenation of volume_id and a users id
    volume_user = db.Column(db.String(256), primary_key=True)
    volume = db.Column(db.String(256))

    user_rating = db.Column(db.Integer)
    user_pred = db.Column(db.Float)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    notes = db.relationship('Notes', backref=db.backref('book_notes'))

class Bookclub(db.Model):
    __tablename__ = 'bookclub'
    id = db.Column(db.Integer, primary_key=True)

    pres_id = db.Column(db.Integer, db.ForeignKey(User.id))
    host_id = db.Column(db.Integer, db.ForeignKey(User.id))

    name = db.Column(db.String(256))

    forums = db.relationship('Forums', backref=db.backref('club_forum'), lazy=True)
    books = db.relationship('Club_Books', backref=db.backref('club_id'), lazy=True)
    users = db.relationship('User', secondary='club_members', lazy='subquery', backref=db.backref('user_clubs'))

class Club_Members(db.Model):
    __tablename__ = 'club_members'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True, nullable=True)
    bookclub_id = db.Column(db.Integer, db.ForeignKey(Bookclub.id), primary_key=True, nullable=True)

class Club_Books(db.Model):
    __tablename__ = 'club_books'
     # Concatenation of volume_id and a club id
    volume_club = db.Column(db.String(256), primary_key=True)
    volume = db.Column(db.String(256))

    club_pred = db.Column(db.Float)
    club = db.Column(db.Integer, db.ForeignKey('bookclub.id'), nullable=False)

# Club_Members = db.Table('club_members', \
#         db.Column('user_id', db.Integer, db.ForeignKey(User.id), primary_key=True), \
#         db.Column('bookclub_id', db.Integer, db.ForeignKey(Bookclub.id), primary_key=True))

class Forums(db.Model):
    __tablename__ = 'forums'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    club = db.Column(db.Integer, db.ForeignKey('bookclub.id'), nullable=False)

    posts = db.relationship('Posts', backref=db.backref('post_forum'))

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)

    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    post = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    forum = db.Column(db.Integer, db.ForeignKey('forums.id'), nullable=False)

class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)

    post = db.Column(db.Text)
    book = db.Column(db.String(256), db.ForeignKey('user_books.volume_user'), nullable=False)

class OAuth(db.Model, OAuthConsumerMixin):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
