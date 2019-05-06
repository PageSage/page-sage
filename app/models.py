from app import app, db, login_manager
#from app import google_bp as blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc  import NoResultFound
from flask_dance.consumer.backend.sqla import OAuthConsumerMixin
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_login import UserMixin
from datetime import date
import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True) 
    f_name = db.Column(db.String(30))
    username = db.Column(db.String(256), nullable=True)
    profile_photo = db.Column(db.LargeBinary, nullable=True)
    algo = db.Column(db.LargeBinary, nullable=True)
    last_train = db.Column(db.Date, nullable=True)

    read_books = db.relationship('Read_Books', backref=db.backref('read_user', lazy=True))
    tbr_books = db.relationship('TBR_Books', backref=db.backref('tbr_user', lazy=True))
    bookclubs = db.relationship('Bookclub', secondary='members')

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Read_Books(db.Model):
    __tablename__ = 'read_books'
    id = db.Column(db.Integer, primary_key=True)
    volume_id = db.Column(db.String(256))
    title = db.Column(db.String(512))
    user_rating = db.Column(db.Integer)
    img_url = db.Column(db.String(512))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))    

    notes = db.relationship('Read_Notes', backref=db.backref('book_note', lazy=True))


class TBR_Books(db.Model):
    __tablename__ = 'tbr_books'
    id = db.Column(db.Integer, primary_key=True)
    volume_id = db.Column(db.String(256))
    title = db.Column(db.String(512))
    user_pred = db.Column(db.String(32))
    img_url = db.Column(db.String(512))
    reading = db.Column(db.Boolean)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))

    notes = db.relationship('TBR_Notes', backref=db.backref('book_note', lazy=True))


class Bookclub(db.Model):
    __tablename__ = 'bookclub'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    president = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    host = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    books = db.relationship('Club_Shelf', backref=db.backref('club_book', lazy=True))
    users = db.relationship('User', secondary='members')


class Members(db.Model):
    __tablename__ = 'members'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookclub_id = db.Column(db.Integer, db.ForeignKey('bookclub.id'))

    user = db.relationship(User, backref=db.backref('members', cascade='all, delete-orphan'))
    product = db.relationship(Bookclub, backref=db.backref('members', cascade='all, delete-orphan'))


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

class Read_Notes(db.Model):
    __tablename__ = 'read_notes'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    content = db.Column(db.Text)
    book = db.Column(db.Integer, db.ForeignKey('read_books.id'))

class TBR_Notes(db.Model):
    __tablename__ = 'tbr_notes'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    content = db.Column(db.Text)
    book = db.Column(db.Integer, db.ForeignKey('tbr_books.id'))

class OAuth(db.Model, OAuthConsumerMixin):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
