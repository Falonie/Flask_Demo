import unittest
from flask import url_for
from app import create_app, db
from app.models import Role, User, Permission, Question, Comment


class UserModelTestCase(unittest.TestCase):
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

    def test_password_setter(self):
        u = User(password='falonie')
        self.assertTrue(u.password_hash is not None)

    def test_password_varification(self):
        u = User(password='falonie')
        self.assertTrue(u.verify_password('falonie'))
        self.assertFalse(u.verify_password('faloniee'))

    def test_valid_confirmation_token(self):
        u = User(username='falonie', password='falonie')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_change_password(self):
        u = User(username='falonie', password='falonie')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.verify_password('falonie'))
        u.password = 'abc123'
        db.session.commit()
        self.assertTrue(u.verify_password('abc123'))
        self.assertFalse(u.verify_password('falonie'))

    def test_change_email(self):
        u = User(email='falonie@falonie.com')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.email == 'falonie@falonie.com')
        u.email = 'falonie2@falonie.com'
        db.session.commit()
        self.assertFalse(u.email == 'falonie@falonie.com')
        self.assertTrue(u.email == 'falonie2@falonie.com')

    def test_roles_and_permissions(self):
        u = User(email='falonie@falonie.com')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.can(Permission.COMMENT) and u.can(Permission.WRITE_ARTICLES) and
                        u.can(Permission.FOLLOW) and u.role.name == 'User')
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS) or u.can(Permission.ADMINISTER))
        admin = User(email='541002901@qq.com')
        db.session.add(admin)
        db.session.commit()
        self.assertTrue(admin.role.name == 'Administrator' and admin.can(Permission.ADMINISTER))
        self.assertTrue(admin.is_administrator())

    def test_public_article_and_comment(self):
        user = User(email='falonie@falonie.com')
        db.session.add(user)
        db.session.commit()
        post = Question(id=10, title='post_title', content='post_content')
        post.users = user
        db.session.add(post)
        db.session.commit()
        self.assertTrue(Question.query.filter(Question.id == 10).first() is not None)
        comment = Comment(id=1, content='comment_content')
        comment.users = user
        comment.questions = post
        db.session.add(comment)
        db.session.commit()
        self.assertTrue(Comment.query.filter_by(id=1).first() is not None)

    def test_public_article_and_comment2(self):
        response = self.client.post(url_for('main.question'), data={
            'title': 'test_title',
            'content': 'content'
        })
        self.assertTrue(response.status_code == 302)
        self.assertTrue(Question.query.filter(Question.title == 'test_title').first() is not None)
        response = self.client.get(url_for('main.index'))
        # self.assertTrue('test_title'.encode('utf8') in response.data)