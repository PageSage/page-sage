from flask import render_template, session, abort, redirect, url_for, flash
from app import app, db
from app.forms import SearchForm
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.google import google
from flask_dance.contrib.facebook import facebook
import requests
from flask_login import login_required, login_user, logout_user, current_user
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError, OAuth2Error
from app.models import User, OAuth
import os

SEARCH_KEY = os.environ.get('SEARCH_KEY')

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
        return redirect(url_for('profile'))
    return render_template('authn/choose-login.html') 

@app.route('/google-login', methods=['GET', 'POST'])
def google_login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if not google.authorized:
        return redirect(url_for('google.login'))
    try:
        account_info = google.get('/oauth2/v2/userinfo')
        if account_info.ok:
            account_info_json = account_info.json()
            email = account_info_json["email"]
            f_name = account_info_json["given_name"]
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(email=email, f_name=f_name)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            flash("Signed in with Google")
            return redirect(url_for('profile'))
    except (InvalidGrantError, TokenExpiredError) as e:
        return redirect(url_for("google.login"))
    return redirect(url_for('profile'))

@app.route('/facebook-login', methods=['GET', 'POST'])
def facebook_login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if not facebook.authorized:
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
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(email=email, f_name=f_name)
                db.session.add(user)
                db.session.commit()
            login_user(user)
            flash("Signed in with Facebook")
            return redirect(url_for('profile'))
    except (InvalidGrantError, TokenExpiredError) as e:
        return redirect(url_for('facebook.login'))
    return redirect(url_for('profile'))

@app.route('/signup')
def signup():
    return render_template('authn/signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))

#################
## User Routes ##
#################

## All user routes should eventually be modified to have dynamic links
## such that the urls are /<username>/profile, etc.
@app.route('/user')
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = SearchForm()
    search_form(form)
    return render_template('user/profile.html', form=form)

## Book should appear as /user/<book>
## Should book be moved to a more general page?
@app.route('/user/book', methods=['GET', 'POST'])
@login_required
def user_book():
    form = SearchForm()
    search_form(form)
    return render_template('user/book.html', form=form)

@app.route('/my-shelf', methods=['GET', 'POST'])
@login_required
def my_shelf():
    form = SearchForm()
    search_form(form)
    return render_template('user/my-shelf.html', form=form)

@app.route('/user/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        flash('Search requested for {}'.format(form.search_item.data))
        return redirect('/user/search')
    return render_template('user/search.html', form=form, SEARCH_KEY=SEARCH_KEY)

@app.route('/user/settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    form = SearchForm()
    search_form(form)
    return render_template('user/settings.html', form=form)


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
