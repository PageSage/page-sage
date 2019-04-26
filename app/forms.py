from flask_wtf import FlaskForm
from flask_inputs import Inputs
from wtforms import StringField, SelectField, SubmitField
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
