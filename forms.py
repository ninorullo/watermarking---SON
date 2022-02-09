from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from wtforms.validators import DataRequired, Length, NumberRange
from werkzeug.utils import secure_filename


class ImageForm(FlaskForm):
    image = FileField(validators=[FileRequired()])
    signature = StringField('Signature', validators=[
                            DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Embed')

class ExtractForm(FlaskForm):
    image = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    # signature_len = h5fields.IntegerField('Signature length', widget=h5widgets.NumberInput(min=2, max=20))
    submit = SubmitField('Extract')
