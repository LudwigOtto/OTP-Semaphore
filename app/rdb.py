from redis import Redis, RedisError
from user import User

class RDB():
    def __init__(self, host='localhost', port=6379):
        self.redis = Redis(host=host, port=port, decode_responses=True)

    def add_user(self, user):
        self.redis.incrby('u_count',1)
        self.redis.sadd('users', user.email)
        h_obj = "user:"+user.email
        self.redis.hset(h_obj, 'email', user.email)
        self.redis.hset(h_obj, 'pswdh', user.password_hash)
        self.redis.hset(h_obj, 'id', self.redis.get('u_count'))

    def is_existed_user(self, email):
        return self.redis.sismember('users', email)

    def query_user(self, email):
        h_obj = "user:"+email
        user = User(email)
        user.set_pwdhash(self.redis.hget(h_obj, 'pswdh'))
        user.set_id(self.redis.hget(h_obj, 'id'))
        return user

    def debug(self):
        print(self.redis.keys())
