from wtforms import Form, StringField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Length, NumberRange, ValidationError, InputRequired
from flask_pagedown.fields import PageDownField
from ..models import User


class PostForm(Form):
    title = StringField('title', validators=[InputRequired()])
    # content = TextAreaField('content', validators=[InputRequired()])
    content = PageDownField('content', validators=[InputRequired()])
    submit = SubmitField('submit')


class CommentForm(Form):
    comment_content = StringField('comment_content', validators=[InputRequired()])
    question_id = StringField('question_id', validators=[InputRequired()])
    submit = SubmitField('submit')


class EditProfileForm(Form):
    name = StringField('name', validators=[InputRequired(), Length(1, 64)])

    def validate_name(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user:
            raise ValidationError('该用户名已存在')


class EditArticleForm(Form):
    title = StringField('title', validators=[InputRequired()])
    # content = TextAreaField('content', validators=[InputRequired()])
    content = PageDownField('content', validators=[InputRequired()])


class DeleteArticleForm(Form):
    article_id = IntegerField('article_id', validators=[InputRequired()])
