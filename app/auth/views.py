import string, random
from flask import url_for, redirect, request, render_template, session, flash, jsonify, views, g
from flask_login import login_user, logout_user
from flask_mail import Mail, Message
from . import auth
from .. import db, mail
from ..models import User
from .forms import RegistrationForm, LoginForm, SMSCaptcha
from . import zlcache


@auth.before_app_request
def before_request():
    user = User.query.filter_by(id=session.get('user_id')).first()
    print(user)
    if user:
        g.user = user


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        password = form.password.data
        user = User.query.filter(User.telephone == telephone, password == password).first()
        if user and user.verify_password(password):
            login_user(user, remember=True)
            # session['user_id'] = user.id
            # session.permanent = True
            # return 'Success!'
            return redirect(url_for('main.index'))
        return 'telephone number or password is incorrect'
        # flash('telephone number or password is incorrect')
    return render_template('login.html')


@auth.route('/logout/')
def logout():
    # session.clear()
    logout_user()
    return redirect(url_for('main.index'))


class RegistrationView(views.MethodView):
    def get(self, message=None):
        return render_template('register.html', message=message)

    def post(self):
        form = RegistrationForm(request.form)
        if form.validate():
            username = form.username.data
            telephone = form.telephone.data
            password = form.password.data
            # email = form.email.data
            # user = User(username=username, telephone=telephone, password=password, email=email)
            user = User(username=username, telephone=telephone, password=password)
            db.session.add(user)
            db.session.commit()
            return jsonify({"code": 200, "message": ""})
            # return redirect(url_for('.login'))
        print('Error: {}'.format(form.errors))
        message = form.errors.popitem()[1][0]
        return jsonify({"code": 401, "message": message})
        # return self.get(message)


auth.add_url_rule('/register/', view_func=RegistrationView.as_view('register'))


@auth.route('/sms_captcha/', methods=['GET', 'POST'])
def index():
    form = SMSCaptcha(request.form)
    if form.validate():
        telephone = form.telephone.data
        code_list = list(string.ascii_letters)
        code_list.extend(list(range(10)))
        # captcha = Captcha.gene_text(number=4)
        captcha = ''.join(str(_) for _ in random.choices(code_list, k=4))
        print('sms is {}'.format(captcha))
        # if alidayu.send_sms(telephone, code=captcha):
        #     zlcache.set(telephone, captcha)
        zlcache.set(telephone, captcha)
        #     return restful.success()
        # return restful.params_error(message='短信验证码发送失败')
        # zlcache.set(telephone, captcha)
        # return restful.success()
        return jsonify({'code': 200})
    # return restful.params_error(message='参数错误')
    return jsonify({'code': 400})


@auth.route('/email/')
def send_email():
    message = Message(subject='this is first mail.', recipients=['541002901@qq.com'], body='this is content.')
    mail.send(message)
    return 'success.'


@auth.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return '请传递邮箱参数'
    source = list(string.ascii_letters)
    source.extend(str(_) for _ in range(0, 10))
    captcha = ''.join(random.sample(source, 6))
    message = Message(subject='Python', recipients=[email], body='验证码：{}'.format(captcha))
    try:
        mail.send(message)
    except Exception as e:
        print(e)
        # return restful.server_error()
    print('generate email captcha: {}'.format(captcha))
    zlcache.set(email, captcha)
    return jsonify({"code": 200, "message": ""})
