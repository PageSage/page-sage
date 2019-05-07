from flask_wtf import FlaskForm
from flask_inputs import Inputs
from wtforms import StringField, SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired, Length
from markupsafe import Markup

class SearchForm(FlaskForm):
    search_item = StringField('', validators=[DataRequired()])
    search = SubmitField('Search')

class BookInputs(Inputs):
    rule = {
        'bookid': [DataRequired()],
        'title': [DataRequired()]
    }

class ChangeUsername(FlaskForm):
    new_username = StringField('New username here', validators=[InputRequired(message='Username cannot be blank'), Length(min=2, max=24, message='Username must be between 2 and 24 characters')])
    change = SubmitField('Change Username')

class SearchBookclubs(FlaskForm):
    bookclub = StringField('Search for a Bookclub Here', validators=[InputRequired()])
    search = SubmitField('Search Bookclubs')

class JoinBookclub(FlaskForm):
    bookclub = StringField('Bookclub Key Code', validators=[InputRequired()])
    join = SubmitField('Join Bookclub')
