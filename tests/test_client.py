import unittest
from datetime import datetime
from hashlib import md5
from flask import url_for
from app import create_app, db
from app.models import Role, User
from app.auth.redis_config import redis_instance


class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        # self.response_data = response.data.decode('utf-8')
        self.assertTrue('注册'.encode(encoding='utf-8') in response.data)
        self.assertTrue('注册' in response.get_data(as_text=True))
        # self.assertTrue('注册' in self.response_data)

    def test_register_and_login(self):
        response = self.client.post('/register_by_email/', data={
            'username': 'falonie',
            'password': 'falonie',
            'repeat_password': 'falonie',
            'email': 'falonie@falonie.com'
        })
        # self.assertTrue(response.status_code == 200)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('邮件已发送'.encode('utf-8') and '前往查收'.encode('utf-8') in response.data)
        self.assertTrue(User.query.filter(User.username == 'falonie').first() is not None)
        # self.assertTrue('前往查收'.encode('utf-8') in response.data)

        # response = self.client.post(url_for('auth.login'), data={
        #     'account': 'falonie@falonie.com',
        #     'password': 'falonie'
        # })

        t = datetime.now()
        sign = md5((str(t) + '18888888888' + 'werqewr2jmvspo2938lwsop').encode('utf-8')).hexdigest()
        self.client.post('/sms_captcha/', data={
            'telephone': '18888888888',
            'timestamp': t,
            'sign': sign
        })
        # self.assertTrue(redis_instance.get('18888888888').decode('utf-8') == sign)
        # response=self.client.post(url_for('auth.register'),data={
        #     'telephone': '18888888888',
        #     'username': 'falonie',
        #     'password': 'falonie',
        #     'repeat_password': 'falonie',
        #     'sms_captcha': redis_instance.get('18888888888').decode('utf-8'),
        # })

        self.client.post('/login', data={
            'account': 'falonie@falonie.com',
            'password': 'falonie'
        })

        # self.client.get(url_for('main.index'))
        response = self.client.get('/')
        # self.assertTrue(response.status_code == 200)
        # self.assertTrue('seems'.encode('utf-8') in response.data)
        # self.assertTrue('falonie'.encode('utf-8') in response.data)

        user = User.query.filter(User.email == 'falonie@falonie.com').first()
        self.assertTrue(user.email == 'falonie@falonie.com')
        self.assertTrue(user.confirmed == False)
        token = user.generate_confirmation_token()
        self.client.get(url_for('auth.confirm', token=token))
        self.assertTrue(user.confirmed == True)

        # r = self.client.get(url_for('auth.logout'))
        self.client.get('/logout')
        r = self.client.get('/')
        self.assertTrue('注册'.encode('utf8') in r.data)
