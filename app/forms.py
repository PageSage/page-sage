from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from markupsafe import Markup

class SearchForm(FlaskForm):
    search_item = StringField('', validators=[DataRequired()])
    search = SubmitField('Search')
