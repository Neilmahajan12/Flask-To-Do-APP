from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,DateTimeField

from wtforms.validators import DataRequired, Length, Optional

class TaskForm(FlaskForm):
    content = StringField('Task', validators=[DataRequired(), Length(min=1, max=200)])
    due_date = DateTimeField('Due Date (optional)', format='%Y-%m-%d %H:%M', validators=[Optional()])
    submit = SubmitField('Add Task')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')
