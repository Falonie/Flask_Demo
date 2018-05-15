from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Length, EqualTo, NumberRange, ValidationError, InputRequired


class PostForm(Form):
    title = StringField('title', validators=[InputRequired()])
    content = TextAreaField('content', validators=[InputRequired()])
    submit = SubmitField('submit')


class CommentForm(Form):
    comment_content = StringField('comment_content', validators=[InputRequired()])
    submit = SubmitField('submit')
