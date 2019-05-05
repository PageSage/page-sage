from flask_wtf import FlaskForm
from flask_inputs import Inputs
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired
from markupsafe import Markup

class SearchForm(FlaskForm):
    search_item = StringField('', validators=[DataRequired()])
    search = SubmitField('Search')

class BookInputs(Inputs):
    rule={
    'bookid': [DataRequired()],
    'title': [DataRequired()]
    }

class AddBook(FlaskForm):
    volume_id = StringField('', validators=[DataRequired()])
    user_pred = StringField('', validators=[DataRequired()])
    add_book = SubmitField('Add Book')

class RemoveBook(FlaskForm):
    volume_id = StringField('', validators=[DataRequired()])
    user_pred = StringField('', validators=[DataRequired()])
    add_book = SubmitField('Remove Book')

class RateBookUp(FlaskForm):
    volume_id = StringField('', validators=[DataRequired()])
    user_rating = IntegerField('', validators=[DataRequired()])
    img_url = StringField('', validators=[DataRequired()])
    rate_up = SubmitField('Liked')

class RateBookDown(FlaskForm):
    volume_id = StringField('', validators=[DataRequired()])
    user_rating = IntegerField('', validators=[DataRequired()])
    img_url = StringField('', validators=[DataRequired()])
    rate_down = SubmitField('Disliked')
