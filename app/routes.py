from flask import render_template, session, abort, redirect, url_for, flash, request
from app import app, db
from app.forms import SearchForm, BookInputs, ChangeUsername
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import google
from flask_dance.contrib.facebook import facebook
from flask_inputs import Inputs
import requests
from flask_login import login_required, login_user, logout_user, current_user, login_manager
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError, OAuth2Error
from app.models import User, OAuth, Read_Books, Read_Notes, TBR_Books, TBR_Notes, Bookclub, Club_Shelf, Forum_Posts, Forums, Members 
import os
import requests
import re
from book_classifier import BookClassifier
import dill as pickle
import numpy as np
from copy import deepcopy
import copy

SEARCH_KEY = os.environ.get('SEARCH_KEY')

@app.before_first_request
def create_tables():
    db.create_all()

###########
## Forms ##
###########

def search_form(form):
    if form.validate_on_submit():
        return redirect('/user/search')


####################
## Landing Routes ##
####################

@app.route('/')
@app.route('/index')
@app.route('/welcome')
def index():
    return render_template('landing/welcome.html')

@app.route('/about')
def about():
    return render_template('landing/about.html')

@app.route('/terms')
@app.route('/tos')
@app.route('/terms-of-service')
def terms():
    return render_template('landing/terms.html')

@app.route('/privacy')
def privacy():
    return render_template('landing/privacy.html')



##################
## AuthN Routes ##
##################

@app.route('/choose-login')
@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile',username=current_user.username))
    return render_template('authn/choose-login.html')

@app.route('/google-login', methods=['GET', 'POST'])
def google_login():
    if current_user.is_authenticated and google.authorized:
        return redirect(url_for('profile',username=current_user.username))
    if (not google.authorized) and (not current_user.is_authenticated):
        return redirect(url_for('google.login'))
    try:
        account_info = google.get('/oauth2/v2/userinfo')
        if account_info.ok:
            account_info_json = account_info.json()
            email = account_info_json["email"]
            f_name = account_info_json["given_name"]
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(email=email, f_name=f_name, algo=None, username=f_name)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            current_user.login_method = "google"
            flash("Signed in with Google")
            return redirect(url_for('profile',username=current_user.username))
    except (InvalidGrantError, TokenExpiredError) as e:
        return redirect(url_for("google.login"))
    return redirect(url_for('profile',username=current_user.username))

@app.route('/facebook-login', methods=['GET', 'POST'])
def facebook_login():
    if current_user.is_authenticated and facebook.authorized:
        return redirect(url_for('profile'))
    if (not facebook.authorized) and (not current_user.is_authenticated):
        return redirect(url_for('facebook.login'))
    try:
        account_info = facebook.get('me?fields=id,first_name,email')
        if account_info.ok:
            with open("errorlog.log", "a+") as cricket:
                cricket.write(str(account_info) + "\n")
        if account_info.ok:
            account_info_json = account_info.json()
            email = account_info_json["email"]
            f_name = account_info_json["first_name"]
            #login_method = "google"
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(email=email, f_name=f_name)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            current_user.login_method = "facebook"
            flash("Signed in with Facebook")
            return redirect(url_for('profile'))
    except (InvalidGrantError, TokenExpiredError) as e:
        return redirect(url_for('facebook.login'))
    return redirect(url_for('profile'))

@app.route('/signup')
def signup():
    return render_template('authn/signup.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    #if current_user.login_method == "google":
    #    token = app.blueprints['google'].token['access_token']
    #    resp = google.post(
    #        "https://accounts.google.com/o/oauth2/revoke",
    #        params={"token": token},
    #        headers={"Content-Type": "application/x-www-form-urlencoded"}
    #    )
    #    assert resp.ok, resp.text
    #elif current_user.login_method == "facebook":
    #    pass
    #with open('greenbook.log', 'a+') as filo:
    #    filo.write(current_user.login_method)
    '''
    try:
        token = app.blueprints['google'].token['access_token']
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    except (TypeError) as e:
         pass
    '''
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))

#################
## User Routes ##
#################

@app.route('/user/<string:username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    form = SearchForm()
    search_form(form)
    user = User.query.filter_by(email=current_user.email).first()

    tbr_books = TBR_Books.query.filter(TBR_Books.user==user.id).all()

    read_books = Read_Books.query.filter(Read_Books.user==user.id).all()
    
    if tbr_books == None:
        tbr_books = False
    if read_books == None:
        read_books = False

    return render_template('user/profile.html', form=form, username=current_user.username, tbr_books=tbr_books, read_books=read_books)

def choose_label(label):
    if int(label) == 1:
        return 'like'
    else:
        return 'not like'


@app.route('/user/<string:username>/<string:title>', methods=['GET', 'POST'])
@app.route('/user/<string:username>/<string:title>/<string:bookid>', methods=['GET', 'POST'])
@app.route('/user/<string:username>/<string:title>/<string:bookid>/<string:method>', methods=['GET', 'POST'])
@login_required
def user_book(username, title, bookid=None, method=None):
    inputValid = BookInputs(request)
    form = SearchForm()
    rateUp = RateBookUp()
    rateDown = RateBookDown()
    addBook = AddBook()
    removeBook = RemoveBook()
    user = User.query.filter_by(email=current_user.email).first()

    if not inputValid.validate():
        return redirect('profile')
 
    url = 'https://www.googleapis.com/books/v1/volumes/'+ bookid +"?key="+ SEARCH_KEY
    resp = requests.get(url)
    resp = resp.json()
    try:
        author = resp['volumeInfo']['authors']
    except (KeyError):
        author = 'Unknown'

    try:
        title = resp['volumeInfo']['title']
        url_title = title.replace(' ','_')
    except (KeyError):
        title = 'Unknown'
        url_title = 'Unknown'

    try:
        description = resp['volumeInfo']['description']
        description = re.sub('<.*?>', '', description)
    except (KeyError):
        description = 'No description available'

    if user.algo == None:
        default_model = BookClassifier
        default_model = pickle.load(open('./app/recommendations/emily_model.pkl', 'rb'))
    else:
        default_model = BookClassifier
        default_model = pickle.loads(user.algo)

    predictions = default_model.predict(bookid)
    percent = str('%.0f' % (predictions[1][0][1]*100))
    label = 'appeal'

    try:
        thumbnail = resp['volumeInfo']['imageLinks']['small']
    except (KeyError):
        try:
            thumbnail = resp['volumeInfo']['imageLinks']['thumbnail']
        except(KeyError):
            thumbnail = url_for('static', filename='./img/cat.png')

    try:
      googlelink= resp['volumeInfo']['previewLink']
    except (KeyError):
      googlelink = 'https://www.google.com'


    if method == 'liked': 
        book = Read_Books.query.filter(Read_Books.user==user.id, Read_Books.volume_id==bookid).first()
        if book == None:
            new_book = Read_Books(user=user.id, volume_id=bookid, title=title, user_rating=1, img_url=thumbnail)
            db.session.add(new_book)
            db.session.commit()
        elif book.user_rating == 0:
            book.user_rating = 1
            db.session.commit()
    elif method == 'disliked':
        book = Read_Books.query.filter(Read_Books.user==user.id, Read_Books.volume_id==bookid).first()
        if book == None:
            new_book = Read_Books(user=user.id, volume_id=bookid, title=title, user_rating=0, img_url=thumbnail)
            db.session.add(new_book)
            db.session.commit()
        elif book.user_rating == 1:
            book.user_rating = 0
            db.session.commit()
    elif method == 'add':
        book = TBR_Books.query.filter(TBR_Books.user==user.id, TBR_Books.volume_id==bookid).first()
        if book == None:
            new_book = TBR_Books(user=user.id, volume_id=bookid, title=title, user_pred=percent, img_url=thumbnail, reading=False)
            db.session.add(new_book)
            db.session.commit()
    elif method == 'remove':
        book = TBR_Books.query.filter(TBR_Books.user==user.id, TBR_Books.volume_id==bookid).first()
        if book != None:
            db.session.delete(book)
            db.session.commit()
    elif method == 'unrate':
        book = Read_Books.query.filter(Read_Books.user==user.id, Read_Books.volume_id==bookid).first()
        if book != None:
            db.session.delete(book)
            db.session.commit()

    book = TBR_Books.query.filter(TBR_Books.user==user.id, TBR_Books.volume_id==bookid).first()
    added = True
    if book == None:
        added = False

    book = Read_Books.query.filter(Read_Books.user==user.id, Read_Books.volume_id==bookid).first()
    if book == None:
        rated = False
    elif book.user_rating == 1:
        rated = 1
    elif book.user_rating == 0:
        rated = 2

    return render_template('user/book.html', form=form,username=current_user.username, bookid=bookid, SEARCH_KEY=SEARCH_KEY, bookTitle=title, author=author, thumbnail=thumbnail, googlelink=googlelink, bookDescription=description, label=label, percent=percent, url_title=url_title, added=added, rated=rated)


@app.route('/<string:username>/my-shelf', methods=['GET', 'POST'])
@login_required
def my_shelf(username):
    form = SearchForm()
    search_form(form)
    return render_template('user/my-shelf.html', form=form,username=current_user.username)

@app.route('/<string:username>/read_shelf', methods=['GET', 'POST'])
@login_required  
def read_shelf(username):
    form = SearchForm()
    return render_template('user/my-shelf.html', form=form)

@app.route('/<string:username>/tbr_shelf', methods=['GET', 'POST'])
@login_required
def tbr_shelf(username):
    form = SearchForm()
    return render_template('user/my-shelf.html', form=form)


@app.route('/user/<string:username>/search', methods=['GET', 'POST'])
@login_required
def search(username):
    form = SearchForm()
    maxResults = '40'
    orderBy = 'relevance'
    printType = 'books'
    projection = 'full'
    url = 'https://www.googleapis.com/books/v1/volumes?q=' + form.search_item.data + '&maxResults=' + maxResults + '&orderBy=' + orderBy + '&printType=' + printType + '&projection=' + projection + '&key=' + SEARCH_KEY
    resp = requests.get(url)
    if resp.ok:
        resp = resp.json()
        new_resp = []
        for book in resp['items']:
            new_book = []
            new_book.append(book['volumeInfo']['title'])
            new_book.append(book['id'])
            urltitle = (book['volumeInfo']['title']).replace(' ','_')
            try:
                image = book['volumeInfo']['imageLinks']['thumbnail']
            except (KeyError):
                image = url_for('static', filename='./img/cat.png')
            new_book.append(urltitle)
            new_book.append(image)
            new_resp.append(new_book)
    else:
        new_resp = None
    #searchTerm = form.value
    if form.validate_on_submit():
        flash('Search requested for {}'.format(form.search_item.data))
        return redirect('/user/search')
    return render_template('user/search.html', form=form,username=current_user.username, SEARCH_KEY=SEARCH_KEY, resp=new_resp)

@app.route('/user/<string:username>/settings', methods=['GET', 'POST'])
@app.route('/user/<string:username>/settings/<string:action>', methods=['GET', 'POST'])
@app.route('/user/<string:username>/settings/<string:action>/<string:classifier>', methods=['GET', 'POST'])
@login_required
def user_settings(username, action=None, classifier=None):
    form = SearchForm()
    search_form(form)
    change_username = ChangeUsername()

    enough = False
    has_classifier = False
    trained = False

    read_books = Read_Books.query.filter(Read_Books.user==current_user.id).all()

    user = User.query.filter(User.id==current_user.id).first()

    num_books = len(read_books)

    defaults = {'fantasy_scifi' : './app/recommendations/fantasy_scify.pkl',
                'mystery'       : './app/recommendations/mystery.pkl',
                'ya_fantasy'    : './app/recommendations/ya_fantasy.pkl',
                'ya_romance'    : './app/recommendations/ya_romance.pkl',
                'biography'     : './app/recommendations/biography.pkl',
                'fiction'       : './app/recommendations/fiction.pkl',
                'history'       : './app/recommendations/history.pkl',
                'classics'      : './app/recommendations/classics.pkl',
                'science'       : './app/recommendations/science.pkl',
                'ya'            : './app/recommendations/ya.pkl',
                'poetry'        : './app/recommendations/poetry.pkl',
                'philosophy'    : './app/recommendations/philosophy.pkl',
                'horror'        : './app/recommendations/horror.pkl',
                'contemporary'  : './app/recommendations/contemporary.pkl',
                'crime'         : './app/recommendations/crime.pkl',
                'art'           : './app/recommendations/art.pkl',
                'christian'     : './app/recommendations/christian.pkl',
                'religion'      : './app/recommendations/religion.pkl',
                'romance'       : './app/recommendations/romance.pkl',
                'psychology'    : './app/recommendations/psychology.pkl',
                'travel'        : './app/recommendations/travel.pkl',
                'sports'        : './app/recommendations/sports.pkl'
               }

    balance = False

    book_balance = False

    if num_books == 0:
        book_balance = 'Liked Books: {} / Disliked Books: {}'.format(0, 0)
    elif num_books > 0:
        num_labels = {1 : 0,
                      0 : 0}
        for book in read_books:
            num_labels[int(book.user_rating)] += 1
        book_balance = 'Liked Books: {} / Disliked Books: {}'.format(num_labels[1], num_labels[0])

    if num_books >= 20:
        enough = True
        if num_labels[0] != 0:
            balance_stat = num_labels[1]/num_labels[0]
        else:
            balance_stat = 2.0
        if (balance_stat <= 1.1) and (balance_stat >= 0.9):
            balance = True
        

    if user.algo != None:
        has_classifier = True

    if (action == 'train'):
        if enough:
            ratings = []
            books = []
            for item in read_books:
                ratings.append(int(item.user_rating))
                books.append(item.volume_id)
            algo = BookClassifier(volumes=books, ratings=ratings)
            algo.fit()
            data = pickle.dumps(algo)
            user.algo = data
            db.session.commit()
            trained = True
    if (action == 'change_username'):
        user.username = change_username.new_username.data
        db.session.commit()
    if (action == 'default_classifier'):
        filename = default[classifier]
        # This should change which default classifier is used in user_books and show which was chosen here

    return render_template('user/settings.html', form=form, username=current_user.username, enough=enough, has_classifier=has_classifier, trained=trained, book_balance=book_balance, balance=balance, num_books=num_books, change_username=change_username)


#####################
## Bookclub Routes ##
#####################

## Bookclub routes should eventually be: /bookclub/<club_name>
@app.route('/bookclub')
@app.route('/club', methods=['GET', 'POST'])
@login_required
def bookclub():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/club.html', form=form)

@app.route('/bookclub/forums', methods=['GET', 'POST'])
@login_required
def forums():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/forums.html', form=form)

## This should eventually be <bookclub_name>/<forum_name>
@app.route('/bookclub/forum', methods=['GET', 'POST'])
@login_required
def forum():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/forum.html', form=form)

@app.route('/bookclub/settings', methods=['GET', 'POST'])
@login_required
def bookclub_settings():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/settings.html', form=form)

@app.route('/bookclub/search', methods=['GET', 'POST'])
@login_required
def bookclub_search():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/search.html', form=form, SEARCH_KEY=SEARCH_KEY)

@app.route('/bookclub/shelf', methods=['GET', 'POST'])
@app.route('/bookclub/bookshelf')
@login_required
def bookclub_shelf():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/shelf.html', form=form)

@app.route('/bookclub/suggestions', methods=['GET', 'POST'])
@login_required
def bookclub_suggestions():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/suggestions.html', form=form)

@app.route('/bookclub/book', methods=['GET', 'POST'])
@login_required
def bookclub_book():
    form = SearchForm()
    search_form(form)
    return render_template('bookclub/book.html', form=form)
