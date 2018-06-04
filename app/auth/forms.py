from hashlib import md5
from flask_login import current_user
from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Length, EqualTo, NumberRange, ValidationError, InputRequired, regexp, Regexp, Email
from ..models import User
from . import zlcache


class RegistrationForm(Form):
    username = StringField('Username', validators=[InputRequired(), Regexp(r'.{2,20}')])
    password = PasswordField('password', validators=[InputRequired(), Regexp(r'[0-9a-zA-Z_\.]{6,20}')])
    repeat_password = PasswordField('repeat_password', validators=[InputRequired(), EqualTo('password')])
    telephone = StringField('telephone', validators=[InputRequired(), Regexp(r'1[345789]\d{9}')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}')])
    # email = StringField(validators=[Email(message='请输入正确格式邮箱')])
    # captcha = StringField(validators=[Length(6, 6, message='请输入正确长度验证码')])
    # submit = SubmitField('Rigister')

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        sms_captcha_mem = zlcache.get(telephone)
        print('sms_captcha is {}'.format(sms_captcha))
        print('sms_captcha_mem is {}'.format(sms_captcha_mem))
        print(sms_captcha.lower() == sms_captcha_mem.lower())
        if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')

    def validate_telephone(self, field):
        if User.query.filter(User.telephone == field.data).first():
            # u = User.query.filter_by(telephone=field.data).first()
            raise ValidationError('telephone has been registered.')

    def validate_username(self, field):
        if User.query.filter(User.username == field.data).first():
            # u = User.query.filter_by(telephone=field.data).first()
            raise ValidationError('username has been registered.')

    # def validate_captcha(self, field):
    #     captcha = field.data
    #     print('Input captcha: {}'.format(captcha))
    #     email = self.email.data
    #     print('Input email: {}'.format(email))
    #     captcha_cache = zlcache.get(email)
    #     print('mem captcha_cache: {}'.format(captcha_cache))
    #     if not captcha_cache or captcha.lower() != captcha_cache.lower():
    #         raise ValidationError('邮箱验证码错误')


class LoginForm(Form):
    telephone = StringField('telephone', validators=[InputRequired(message='telephone required'),
                                                     Length(11, 11, message='telephone length')])
    password = StringField('password', validators=[InputRequired()])


class ResetEmailForm(Form):
    email = StringField(validators=[Email(message='请输入正确格式邮箱')])
    captcha = StringField(validators=[Length(6, 6, message='请输入正确长度验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误')

    def validate_email(self, field):
        email = field.data
        # if g.user.email == email:
        if current_user.email == email:
            raise ValidationError('不能修改为相同邮箱')
        user = User.query.filter(User.email == email).first()
        if user:
            raise ValidationError('该邮箱已被注册')


class SMSCaptcha(Form):
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])
    salt = 'werqewr2jmvspo2938lwsop'

    def validate(self):
        result = super(SMSCaptcha, self).validate()
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        sign2 = md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()
        print('sign {}'.format(sign))
        print('sign2 {}'.format(sign2))
        if sign == sign2:
            return True
        return False


class ChangePasswordForm(Form):
    old_password = PasswordField(validators=[Length(6, 20, message='请输入正确格式密码'), InputRequired()])
    password = PasswordField(validators=[Length(6, 20, message='请输入正确格式密码'), InputRequired()])
    password2 = PasswordField(validators=[Length(6, 20, message='请输入正确格式密码'),
                                          EqualTo('password', message='两次密码不一致')])


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[Email(message='请输入正确格式邮箱')])
    submit = SubmitField('提交')


class PasswordResetEmailForm(Form):
    email = StringField('Email', validators=[Email(message='请输入正确格式邮箱')])
    password = PasswordField('password', validators=[InputRequired(), Regexp(r'[0-9a-zA-Z_\.]{6,20}')])
    repeat_password = PasswordField('repeat_password', validators=[InputRequired(), EqualTo('password')])


class PasswordResetForm(Form):
    telephone = StringField('telephone', validators=[InputRequired(), Regexp(r'1[345789]\d{9}')])
    password = PasswordField('password', validators=[InputRequired(), Regexp(r'[0-9a-zA-Z_\.]{6,20}')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        sms_captcha_mem = zlcache.get(telephone)
        print('sms_captcha is {}'.format(sms_captcha))
        print('sms_captcha_mem is {}'.format(sms_captcha_mem))
        print(sms_captcha.lower() == sms_captcha_mem.lower())
        if not sms_captcha_mem or sms_captcha_mem.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')
