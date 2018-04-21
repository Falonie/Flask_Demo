from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Required, Length, EqualTo, NumberRange, ValidationError
from ..models import User


class RegistrationForm(Form):
    username = StringField('Username', validators=[Required(), Length(3, 64)])
    password = PasswordField('password',
                             validators=[Required(), EqualTo('repeat_password', message='Passwords must match')])
    repeat_password = PasswordField('repeat_password', validators=[Required()])
    telephone = StringField('telephone', validators=[Required(), Length(11, 11)])
    submit = SubmitField('Rigister')

    def validate_telephone(self, field):
        if User.query.filter(User.telephone == field.data).first():
            # u = User.query.filter_by(telephone=field.data).first()
            raise ValidationError('telephone has been registered.')

    def validate_username(self, field):
        if User.query.filter(User.username == field.data).first():
            # u = User.query.filter_by(telephone=field.data).first()
            raise ValidationError('username has been registered.')
