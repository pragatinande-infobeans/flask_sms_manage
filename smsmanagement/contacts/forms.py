from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    contact_name = StringField('Enter Name', validators=[DataRequired()])
    contact_nos = StringField('Enter Mobile Number', validators=[DataRequired()])
    contact_email = EmailField('Enter Email', validators=[DataRequired()])
    group = SelectField('Group', coerce=int, validators=[DataRequired()])

    def set_group_choices(self, choices):
        self.group.choices = choices

    submit = SubmitField('Submit')

