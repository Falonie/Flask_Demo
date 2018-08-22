from datetime import datetime
from hashlib import md5

# print(type(b'注册'))
print(type(b'Stranger'))
print(b'Stranger')
print('注册'.encode(encoding='utf-8'))
print(type('注册'.encode(encoding='utf-8')))
# print('注册'.encode(encoding='utf8').decode(encoding='ASCII'))

# app = Flask(__name__)
# with app.test_request_context():
#     print(url_for('main.index'))
print(str(datetime.now()))
print(type(datetime.now()))
print(type(str(datetime.now())))
print(md5((str(datetime.now()) + '18888888888' + 'werqewr2jmvspo2938lwsop').encode('utf-8')).hexdigest())
print(0x80, 0xff)
print("\u6709\u54ea\u4e9b\u5f88\u6709\u610f\u601d\u7684\u51b7\u77e5\u8bc6\uff1f")
print(type("\u6709\u54ea\u4e9b\u5f88\u6709\u610f\u601d\u7684\u51b7\u77e5\u8bc6\uff1f"))