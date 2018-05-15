# @auth.route('/register/', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm(request.form)
#     # if request.method == 'POST':
#     return_to = request.referrer
#     print(return_to)
#     if form.validate():
#         username = form.username.data
#         telephone = form.telephone.data
#         password = form.password.data
#         user = User(username=username, telephone=telephone, password=password)
#         db.session.add(user)
#         db.session.commit()
#         print('return to :{}'.format(return_to))
#         return redirect(url_for('.login'))
#         # return render_template('register.html', return_to=return_to)
#     print(form.errors)
#     # flash(message='{}'.format(form.errors))
#     return render_template('register.html')

