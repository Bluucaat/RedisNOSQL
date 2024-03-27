

import redis

host = '172.22.233.176'

r_port=6379
r=redis.Redis(host, r_port, decode_responses=True)
print(r.get('alma'))

r.sadd('s10', 'alma', 'korte')
r.sadd('s10', 'kigyo')

print(r.smembers('s10'))
for i in r.smembers('s10'):
    print(i)