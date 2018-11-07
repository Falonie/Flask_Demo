from hashlib import md5
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Length, EqualTo, NumberRange, ValidationError, InputRequired, regexp, Regexp, Email
from ..models import User
from .redis_config import redis_instance
from . import zlcache


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Regexp(r'.{2,20}', message='用户名长度应为2至20位')])
    password = PasswordField('password', validators=[InputRequired(), Regexp(r'[0-9a-zA-Z_\.]{6,20}',
                                                                             message='密码应为6至20位的数字字母及其它字符')])
    repeat_password = PasswordField('repeat_password', validators=[InputRequired(),
                                                                   EqualTo('password', message='两次密码不一致')])
    telephone = StringField('telephone', validators=[InputRequired(), Regexp(r'1[345789]\d{9}', message='手机格式错误')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}')])
    # email = StringField(validators=[Email(message='请输入正确格式邮箱')])
    # captcha = StringField(validators=[Length(6, 6, message='请输入正确长度验证码')])
    # submit = SubmitField('Rigister')

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        # sms_captcha_redis = zlcache.get(telephone)
        sms_captcha_redis = redis_instance.get(telephone).decode('utf-8') or zlcache.get(telephone)
        print('sms_captcha input is {}'.format(sms_captcha))
        print('sms_captcha_redis_cache is {}'.format(sms_captcha_redis))
        if not sms_captcha_redis or sms_captcha_redis.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')

    def validate_telephone(self, field):
        if User.query.filter(User.telephone == field.data).first():
            # u = User.query.filter_by(telephone=field.data).first()
            raise ValidationError('此手机号已被注册')

    def validate_username(self, field):
        if User.query.filter(User.username == field.data).first():
            # u = User.query.filter_by(telephone=field.data).first()
            raise ValidationError('用户名已被注册')

    # def validate_captcha(self, field):
    #     captcha = field.data
    #     print('Input captcha: {}'.format(captcha))
    #     email = self.email.data
    #     print('Input email: {}'.format(email))
    #     captcha_cache = zlcache.get(email)
    #     print('mem captcha_cache: {}'.format(captcha_cache))
    #     if not captcha_cache or captcha.lower() != captcha_cache.lower():
    #         raise ValidationError('邮箱验证码错误')


class RegistrationByEmailForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Regexp(r'.{2,20}', message='用户名长度应为2至20位')])
    password = PasswordField('password', validators=[InputRequired(), Regexp(r'[0-9a-zA-Z_\.]{6,20}',
                                                                             message='密码应为6至20位的数字字母及其它字符')])
    repeat_password = PasswordField('repeat_password',
                                    validators=[InputRequired(), EqualTo('password', message='两次密码不一致')])
    email = StringField(validators=[InputRequired(), Email(message='请输入正确格式邮箱')])

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user:
            raise ValidationError("该邮箱已被注册")

    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user:
            raise ValidationError("该用户名已存在")


class LoginForm(FlaskForm):
    # telephone = StringField('telephone', validators=[InputRequired(message='telephone required'),
    #                                                  Length(11, 11, message='telephone length')])
    account = StringField('account', validators=[InputRequired(message='请输入正确格式邮箱或手机号')])
    password = StringField('password', validators=[InputRequired()])

    def validate_account(self, field):
        user = User.query.filter(User.telephone == field.data).first() or\
               User.query.filter(User.email == field.data).first()
        if not user:
            raise ValidationError("该手机号/邮箱未被注册")


class ChangeTelephoneForm(Form):
    telephone = StringField('telephone', validators=[InputRequired(), Regexp(r'1[345789]\d{9}')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        sms_captcha_redis = redis_instance.get(telephone).decode('utf-8') or zlcache.get(telephone)
        print(f'sms_captcha input is {sms_captcha}')
        print(f'sms_captcha_redis_cache is {sms_captcha_redis}')
        if not sms_captcha_redis or sms_captcha_redis.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')

    def validate_telephone(self, field):
        if User.query.filter(User.telephone == field.data).first():
            raise ValidationError('此手机号已被注册')


class ChangeEmailForm(Form):
    email = StringField(validators=[Email(message='请输入正确格式邮箱')])
    captcha = StringField(validators=[Length(6, 6, message='请输入正确长度验证码')])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_redis = redis_instance.get(email).decode('utf-8') or zlcache.get(email)
        if not captcha_redis or captcha.lower() != captcha_redis.lower():
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
    password = PasswordField('password', validators=[InputRequired(), Regexp(r'[0-9a-zA-Z_\.]{6,20}',
                                                                             message='密码应为6至20位的数字字母及其它字符')])
    repeat_password = PasswordField('repeat_password',
                                    validators=[InputRequired(), EqualTo('password', message='两次密码不一致')])


class PasswordResetForm(Form):
    telephone = StringField('telephone', validators=[InputRequired(), Regexp(r'1[345789]\d{9}', message='请输入正确格式手机号')])
    password = PasswordField('password', validators=[InputRequired(),
                                                     Regexp(r'[0-9a-zA-Z_\.]{6,20}', message='密码应为6至20位的数字字母及其它字符')])
    sms_captcha = StringField(validators=[Regexp(r'\w{4}')])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data
        sms_captcha_redis = redis_instance.get(telephone).decode('utf-8') or zlcache.get(telephone)
        print('sms_captcha input is {}'.format(sms_captcha))
        print('sms_captcha_redis_cache is {}'.format(sms_captcha_redis))
        if not sms_captcha_redis or sms_captcha_redis.lower() != sms_captcha.lower():
            raise ValidationError(message='短信验证码错误')
