from flask import Flask, current_app, render_template
from celery import Celery
from flask_mail import Message, Mail
# from exts import mail
# import config
from config import config
from app import create_app

app = Flask(__name__)
app.config.from_object(config['default'])
mail = Mail()
mail.init_app(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)


# @celery.task
# def send_mail(subject, recipients, body):
#     message = Message(subject=subject, recipients=recipients, body=body)
#     mail.send(message)

@celery.task
def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=[to], sender=current_app.config['MAIL_DEFAULT_SENDER'])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # msg.body = render_template('email/reset_password' + '.txt', **kwargs)
    # msg.html = render_template('email/reset_password' + '.html', **kwargs)
    mail.send(msg)
    # thr = Thread(target=send_async_email, args=[app, msg])
    # thr.start()
    # return thr


@celery.task
def send_mail2(to, subject, body, template=None, **kwargs):
    message = Message(subject=subject, recipients=[to], sender=current_app.config['MAIL_DEFAULT_SENDER'], body=body)
    message.html = render_template(template + '.html', **kwargs)
    message.body = render_template(template + '.txt', **kwargs)
    # Message()
    mail.send(message)

# send_mail2('python',['541002901@qq.com'],'python')
