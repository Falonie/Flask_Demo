# @auth.route('/register/', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         form = RegistrationForm(request.form)
#         if form.validate():
#             username = form.username.data
#             telephone = form.telephone.data
#             password = form.password.data
#             # email = form.email.data
#             # user = User(username=username, telephone=telephone, password=password, email=email)
#             user = User(username=username, telephone=telephone, password=password, confirmed=True)
#             db.session.add(user)
#             db.session.commit()
#             return jsonify({"code": 200, "message": "注册成功"})
#             # return redirect(url_for('.login'))
#         print('Error: {}'.format(form.errors))
#         message = form.errors.popitem()[1][0]
#         return jsonify({"code": 401, "message": message})
#     return render_template('register.html')


# @auth.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         form = LoginForm(request.form)
#         if form.validate():
#             # telephone = form.telephone.data
#             account_number = form.account.data
#             password = form.password.data
#             # user = User.query.filter(User.telephone == account_number, password == password).first() or \
#             #        User.query.filter(User.email == account_number, password == password).first()
#             user = User.query.filter(User.telephone == account_number).first() or \
#                    User.query.filter(User.email == account_number).first()
#             print('login user {}'.format(user))
#             if user and user.verify_password(password):
#                 login_user(user, remember=True)
#                 # session['user_id'] = user.id
#                 # session.permanent = True
#                 # return redirect(url_for('main.index'))
#                 return jsonify({"code": 200, "message": ""})
#             return jsonify({"code": 401, "message": "手机号或密码错误"})
#         print('Error: {}'.format(form.errors))
#         message = form.errors.popitem()[1][0]
#         return jsonify({"code": 401, "message": message})
#     return_to = request.referrer
#     print('*' * 30, 'login return_to {}'.format(return_to), '*' * 30)
#     return render_template('login.html', return_to=return_to)


# class ChangeTelephoneView(views.MethodView):
#     decorators = [login_required]
#
#     def get(self):
#         return render_template('auth/change_telephone.html')
#
#     def post(self):
#         form = ChangeTelephoneForm(request.form)
#         if form.validate():
#             telephone = form.telephone.data
#             current_user.telephone = telephone
#             db.session.commit()
#             # return redirect(url_for('main.index'))
#             return jsonify({"code": 200, "message": "手机号修改成功"})
#         print('Error: {}'.format(form.errors))
#         message = form.errors.popitem()[1][0]
#         return jsonify({"code": 401, "message": message})
#
#
# auth.add_url_rule('/change_telephone/', view_func=ChangeTelephoneView.as_view('change_telephone'))


# class ChangeEmailView(views.MethodView):
#     decorators = [login_required]
#
#     def get(self, message=None):
#         return render_template('change_email.html', message=message)
#
#     def post(self):
#         form = ChangeEmailForm(request.form)
#         if form.validate():
#             print('captcha is: {}'.format(form.captcha.data))
#             email = form.email.data
#             # g.user.email = email
#             current_user.email = email
#             db.session.commit()
#             return jsonify({"code": 200, "message": "邮箱修改成功"})
#         print(form.errors)
#         message = form.errors.popitem()[1][0]
#         return jsonify({"code": 401, "message": message})
#         # return self.get(message)
#
#
# auth.add_url_rule('/change_email/', view_func=ChangeEmailView.as_view('change_email'))


# class ChangePassword(views.MethodView):
#     decorators = [login_required]
#
#     def get(self, message=None):
#         return render_template('change_password.html', message=message)
#
#     def post(self):
#         form = ChangePasswordForm(request.form)
#         if form.validate():
#             old_password = form.old_password.data
#             new_password = form.password.data
#             print('form validate.')
#             if current_user.verify_password(old_password):
#                 current_user.password = new_password
#                 db.session.commit()
#                 print('verified.')
#                 # return redirect(url_for('main.index'))
#                 return jsonify({"code": 200, "message": "密码修改成功"})
#             return jsonify({"code": 401, "message": '密码错误'})
#         return jsonify({"code": 401, "message": form.errors.popitem()[1][0]})
#
#
# auth.add_url_rule('/changepassword/', view_func=ChangePassword.as_view('changepassword'))


# class PasswordReset(views.MethodView):
#     def get(self):
#         return render_template('reset_password.html')
#
#     def post(self):
#         form = PasswordResetForm(request.form)
#         if form.validate():
#             telephone = form.telephone.data
#             password = form.password.data
#             # sms_captcha = form.sms_captcha.data
#             # sms_captcha_mem = zlcache.get(telephone)
#             user = User.query.filter(User.telephone == telephone).first()
#             # if user and sms_captcha.lower() == sms_captcha_mem.lower():
#             if user:
#                 user.password = password
#                 db.session.commit()
#                 return jsonify({"code": 200, "message": "密码修改成功"})
#             return jsonify({"code": 401, "message": "该手机号未被注册"})
#         return jsonify({"code": 401, "message": form.errors.popitem()[1][0]})
#
#
# auth.add_url_rule('/password_reset_/', view_func=PasswordReset.as_view('password_reset_'))
