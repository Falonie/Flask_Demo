import string, random
from flask import url_for, redirect, request, render_template, session, jsonify, views, g
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from . import auth
from .. import db, mail
from ..models import User
from .forms import RegistrationForm, LoginForm, ResetEmailForm, SMSCaptcha, ChangePasswordForm, \
    PasswordResetRequestForm, PasswordResetEmailForm, PasswordResetForm
from ..email import send_mail_thread, send_mail_thread2
from . import zlcache


@auth.before_app_request
def before_request():
    # if current_user.is_authenticated:
    #     current_user.ping()
    # return redirect(url_for('main.index'))
    user = User.query.filter_by(id=session.get('user_id')).first()
    if user:
        g.user = user
        # user.ping()

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
            # return redirect(url_for('main.index'))
            return jsonify({"code": 200, "message": ""})
        return jsonify({"code": 401, "message": "手机号或密码错误"})
    return render_template('login.html')


@auth.route('/logout/')
def logout():
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
    send_mail_thread(to='541002901@qq.com', subject='python', body='captcha code')
    return 'success.'


@auth.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return '请传递邮箱参数'
    source = list(string.ascii_letters)
    source.extend(str(_) for _ in range(0, 10))
    captcha = ''.join(random.sample(source, 6))
    # message = Message(subject='Python', recipients=[email], body='验证码：{}'.format(captcha))
    # mail.send(message)
    # send_mail_thread(to=email, subject='captcha code', body='验证码：{}'.format(captcha))
    token = current_user.generate_reset_token()
    send_mail_thread2(to=email, subject='captcha code', template='email/change_email', user=current_user, token=token,
                      captcha_code=captcha)
    print('generate email captcha: {}'.format(captcha))
    zlcache.set(email, captcha)
    return jsonify({"code": 200, "message": ""})


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self, message=None):
        return render_template('reset_email.html', message=message)

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            print('captcha is: {}'.format(form.captcha.data))
            email = form.email.data
            # g.user.email = email
            current_user.email = email
            db.session.commit()
            return jsonify({"code": 200, "message": "邮箱修改成功"})
        print(form.errors)
        message = form.errors.popitem()[1][0]
        return jsonify({"code": 401, "message": message})
        # return self.get(message)


auth.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


class ChangePassword(views.MethodView):
    decorators = [login_required]

    def get(self, message=None):
        # print(current_user.username)
        # print(g.user.password_hash)
        print('change password')
        print('verify password {}'.format(current_user.verify_password('13059827504')))
        return render_template('change_password.html', message=message)

    def post(self):
        form = ChangePasswordForm(request.form)
        if form.validate():
            old_password = form.old_password.data
            new_password = form.password.data
            print('form validate.')
            if current_user.verify_password(old_password):
                current_user.password = new_password
                db.session.commit()
                print('verified.')
                # return redirect(url_for('main.index'))
                return jsonify({"code": 200, "message": "密码修改成功"})
            return jsonify({"code": 401, "message": '密码错误'})
        return jsonify({"code": 401, "message": form.errors.popitem()[1][0]})


auth.add_url_rule('/changepassword/', view_func=ChangePassword.as_view('changepassword'))


class PasswordReset(views.MethodView):
    def get(self):
        return render_template('reset_password.html')

    def post(self):
        form = PasswordResetForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            # sms_captcha = form.sms_captcha.data
            # sms_captcha_mem = zlcache.get(telephone)
            user = User.query.filter(User.telephone == telephone).first()
            # if user and sms_captcha.lower() == sms_captcha_mem.lower():
            if user:
                user.password = password
                db.session.commit()
                return jsonify({"code": 200, "message": "密码修改成功"})
            return jsonify({"code": 401, "message": "该手机号未被注册"})
        return jsonify({"code": 401, "message": form.errors.popitem()[1][0]})


auth.add_url_rule('/password_reset/', view_func=PasswordReset.as_view('password_reset'))


@auth.route('/password_reset_email/', methods=['GET', 'POST'])
def password_reset_email_request():
    form = PasswordResetRequestForm(request.form)
    if form.validate():
        user = User.query.filter(User.email == form.email.data).first()
        if user:
            print('username is {}'.format(user.username))
            # source = list(string.ascii_letters)
            # source.extend(str(_) for _ in range(0, 10))
            # captcha = ''.join(random.sample(source, 6))
            token = user.generate_reset_token()
            send_mail_thread2(user.email, 'reset password', 'email/reset_password', token=token, user=user)
            return redirect(url_for('.login'))
    return render_template('reset_password_email_request.html')


@auth.route('/password_reset_email/<token>/', methods=['GET', 'POST'])
def password_reset_email(token):
    form = PasswordResetEmailForm(request.form)
    if form.validate():
        user = User.query.filter(User.email == form.email.data).first()
        if user.reset_password(token, form.password.data):
            print('set password: {}'.format(form.password.data))
            return redirect(url_for('.login'))
            # return jsonify({"code":200,"message":""})
    return render_template('reset_password_email.html')
