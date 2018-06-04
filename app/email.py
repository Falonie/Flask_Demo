from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail, Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail_thread(to, subject, body, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=[to], sender=app.config['MAIL_DEFAULT_SENDER'], body=body)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def send_mail_thread2(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=[to], sender=app.config['MAIL_DEFAULT_SENDER'])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # msg.body = render_template('email/reset_password' + '.txt', **kwargs)
    # msg.html = render_template('email/reset_password' + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
