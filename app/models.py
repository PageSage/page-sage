from app import app, db, login_manager
#from app import google_bp as blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc  import NoResultFound
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import UserMixin
import datetime

# club_members = db.Table('club_members', \
#         db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True), \
#         db.Column('club_id', db.Integer, db.ForeignKey('bookclub.id'), primary_key=True))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # Formerly username
    email = db.Column(db.String(256), unique=True) 
    f_name = db.Column(db.String(30))
    username = db.Column(db.String(256), nullable=True)
    profile_photo = db.Column(db.LargeBinary, nullable=True)
    algo = db.Column(db.LargeBinary, nullable=True)

    books = db.relationship('User_Shelf', backref=db.backref('reader', lazy=True))
    # clubs = db.relationship('Bookclub', secondary=club_members, lazy='subquery', backref=db.backref('members', lazy=True))

    def __repr__(self):
        return '<User {}>'.format(self.email)

class User_Shelf(db.Model):
    __tablename__ = 'user_shelf'
    id = db.Column(db.String(256), primary_key=True)
    volume_id = db.Column(db.String(256))
    user_rating = db.Column(db.Integer, nullable=True)
    user_pred = db.Column(db.Float)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    notes = db.relationship('Notes', backref=db.backref('book_note', lazy=True))

class Bookclub(db.Model):
    __tablename__ = 'bookclub'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    president = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    host = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    books = db.relationship('Club_Shelf', backref=db.backref('club_book', lazy=True))

class Club_Shelf(db.Model):
    __tablename__ = 'club_shelf'
    id = db.Column(db.String(256), primary_key=True)
    volume_id = db.Column(db.String(256))
    club_pred = db.Column(db.Float)

    club = db.Column(db.Integer, db.ForeignKey('bookclub.id'))

class Forums(db.Model):
    __tablename__ = 'forums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))

    posts = db.relationship('Forum_Posts', backref=db.backref('forum_post', lazy=True))

class Forum_Posts(db.Model):
    __tablename__ = 'forum_posts'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    content = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    forum = db.Column(db.Integer, db.ForeignKey('forums.id'))

class Notes(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    content = db.Column(db.Text)
    book = db.Column(db.String(256), db.ForeignKey('user_shelf.id'))

class OAuth(db.Model, OAuthConsumerMixin):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
