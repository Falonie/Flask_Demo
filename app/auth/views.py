import string, random
from flask import url_for, redirect, request, render_template, session, jsonify, views, g, current_app,flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from . import auth
from .. import db, mail
from ..models import User, Permission, Question
from .forms import RegistrationForm, RegistrationByEmailForm, LoginForm, ChangeEmailForm, SMSCaptcha, \
    ChangeTelephoneForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetEmailForm, PasswordResetForm
from ..email import send_mail_thread, send_mail_thread2
from .redis_config import redis_instance
from . import zlcache
from tasks import send_mail, send_mail2


@auth.before_app_request
def before_request():
    user = User.query.filter_by(id=session.get('user_id')).first()
    if user:
        g.user = user
    if current_user.is_authenticated:
        print('request.endpoint: ', request.endpoint)
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))
    # print('*' * 20, 'permissions', current_user.can(Permission.WRITE_ARTICLES), '*' * 20)
    # u = User.query.filter(User.id == 3).all()
    u = User.query.get_or_404(3)
    print(u)
    print(f"User Count: {User.query.count()}")
    # print(f'g.current_user: {g.current_user}')
    # page = request.args.get('page', type=int, default=1)
    # print(Question.query.filter(Question.user_id==u.id).order_by(Question.create_time.desc()).all())
    # p = u.questions.order_by(Question.create_time.desc())
    # p = Question.query.filter(Question.user_id == u.id).order_by(Question.create_time.desc()).all()
    # page = request.args.get('page', type=int, default=1)
    # p = Question.query.filter(Question.user_id == u.id).order_by(Question.create_time.desc()).paginate(page=page,per_page=2,error_out=False)
    # print(p.items)
    # p = Question.query.order_by(Question.create_time.desc()).paginate(page=page, per_page=5, error_out=False)
    # p = Question.query.order_by(Question.create_time.desc()).all()
    # print(p.items)


@auth.route('/unconfirmed/')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


class RegistrationView(views.MethodView):
    def get(self, message=None):
        return_to = request.referrer
        return render_template('register.html', return_to=return_to, message=message)

    def post(self):
        form = RegistrationForm()
        if form.validate():
            username = form.username.data
            telephone = form.telephone.data
            password = form.password.data
            # email = form.email.data
            # user = User(username=username, telephone=telephone, password=password, email=email)
            user = User(username=username, telephone=telephone, password=password, confirmed=True)
            db.session.add(user)
            db.session.commit()
            return jsonify({"code": 200, "message": "注册成功"})
            # return redirect(url_for('.login'))
        print(f'Error: {form.errors}')
        message = form.errors.popitem()[1][0]
        return jsonify({"code": 401, "message": message})
        # return self.get(message)


auth.add_url_rule('/register/', view_func=RegistrationView.as_view('register'))


class LoginView(views.MethodView):
    def get(self):
        return_to = request.referrer
        print('*' * 30, f'login return_to {return_to}', '*' * 30)
        return render_template('login.html', return_to=return_to)

    def post(self):
        form = LoginForm()
        if form.validate():
            # telephone = form.telephone.data
            account_number = form.account.data
            password = form.password.data
            # user = User.query.filter(User.telephone == account_number, password == password).first() or \
            #        User.query.filter(User.email == account_number, password == password).first()
            user = User.query.filter(User.telephone == account_number).first() or \
                   User.query.filter(User.email == account_number).first()
            print(f'login user {user}')
            if user and user.verify_password(password):
                login_user(user, remember=True)
                # session['user_id'] = user.id
                # session.permanent = True
                # return redirect(url_for('main.index'))
                flash("登录成功")
                return jsonify({"code": 200, "message": ""})
            return jsonify({"code": 401, "message": "手机号或密码错误"})
        print('Error: {}'.format(form.errors))
        message = form.errors.popitem()[1][0]
        return jsonify({"code": 401, "message": message})


auth.add_url_rule('/login/', view_func=LoginView.as_view('login'))


@auth.route('/logout/')
def logout():
    logout_user()
    # return redirect(url_for('main.index'))
    return redirect(request.referrer)


@auth.route('/register_by_email/', methods=['GET', 'POST'])
def register_by_email():
    if request.method == "POST":
        form = RegistrationByEmailForm()
        if form.validate():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            user = User(username=username, password=password, email=email)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_mail_thread2(user.email, 'comfirmation', 'email/confirm', user=user, token=token)
            # return render_template('after_sent_email.html')
            # return redirect(url_for('.login'))
            return jsonify({"code": 200, "message": "邮件已发送"})
        print(f'Error: {form.errors}')
        message = form.errors.popitem()[1][0]
        return jsonify({"code": 401, "message": message})
    return render_template('registration_email.html')


@auth.route('/confirm/<token>/')
@login_required
def confirm(token):
    if current_user.confirm(token):
        return redirect(url_for('main.index'))
    return 'unconfirmed page.'


@auth.route('/confirm')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail_thread2(current_user.email, 'comfirmation', 'email/confirm', user=current_user, token=token)
    return render_template('after_sent_email.html')


@auth.route('/sms_captcha/', methods=['GET', 'POST'])
def sms_captcha():
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
        redis_instance.set(telephone, captcha)
        print('*' * 30, f'redis sms_captcha {redis_instance.get(telephone).decode("utf-8")}', '*' * 30)
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
    # send_mail2(subject='captcha code', to=email, template='email/change_email', user=current_user, token=token,body=captcha,
    #            captcha_code=captcha)
    # send_mail(to=email, subject='captcha code', template='email/change_email', user=current_user, token=token,
    # captcha_code=captcha)
    send_mail_thread2(to=email, subject='captcha code', template='email/change_email', user=current_user, token=token,
                      captcha_code=captcha)
    print('*' * 30, f'generate email captcha: {captcha}', '*' * 30)
    zlcache.set(email, captcha)
    redis_instance.set(email, captcha)
    print('*' * 30, f'redis captcha {redis_instance.get(email).decode("utf-8")}', '*' * 30)
    return jsonify({"code": 200, "message": ""})


@auth.route('/change_telephone/', methods=['GET', 'POST'])
@login_required
def change_telephone():
    if request.method == 'POST':
        form = ChangeTelephoneForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            current_user.telephone = telephone
            db.session.commit()
            # return redirect(url_for('main.index'))
            return jsonify({"code": 200, "message": "手机号修改成功"})
        print(f'Error: {form.errors}')
        message = form.errors.popitem()[1][0]
        return jsonify({"code": 401, "message": message})
    return render_template('auth/change_telephone.html')


@auth.route('/change_email/', methods=['GET', 'POST'])
@login_required
def change_email():
    if request.method == 'POST':
        form = ChangeEmailForm(request.form)
        if form.validate():
            print(f'captcha is: {form.captcha.data}')
            email = form.email.data
            # g.user.email = email
            current_user.email = email
            db.session.commit()
            return jsonify({"code": 200, "message": "邮箱修改成功"})
        print(form.errors)
        message = form.errors.popitem()[1][0]
        return jsonify({"code": 401, "message": message})
    return render_template('change_email.html')


@auth.route('/changepassword/', methods=['GET', 'POST'])
@login_required
def changepassword():
    if request.method == 'POST':
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
    return render_template('change_password.html')


@auth.route('/password_reset/', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
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
    return render_template('reset_password.html')


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
