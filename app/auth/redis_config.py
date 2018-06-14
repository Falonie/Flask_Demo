from redis import Redis

redis_instance = Redis(host='127.0.0.1', port=6379, password='falonie')

# redis_instance.set('username', 'Falonie Wang')
# print(redis_instance.get('username'))
# print(redis_instance.get('username').decode('utf-8'))
# print(type('falonie'.encode(encoding='utf-8').decode('utf-8')))
# print(redis_instance.get('telephone'))
# print(redis_instance.get('Falonie_Wang@outlook.com').decode('utf-8'))