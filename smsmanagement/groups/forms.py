from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField
from wtforms.validators import DataRequired


class GroupForm(FlaskForm):
    group_name = StringField('Group Name', validators=[DataRequired()])
    group_description = StringField('Group Description', validators=[DataRequired()])
    # created_date = DateTimeField('Created Date', validators=[DataRequired()])
    submit = SubmitField('SUbmit')
