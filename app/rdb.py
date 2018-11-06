from redis import Redis, RedisError
from user import User

class RDB():
    def __init__(self, host='localhost', port=6379):
        self.redis = Redis(host=host, port=port, decode_responses=True)

    def add_user(self, user):
        self.redis.sadd('users', user.email)
        h_obj = "user:"+user.email
        self.redis.hset(h_obj, 'email', user.email)
        self.redis.hset(h_obj, 'pswdh', user.password_hash)

    def verify_user(self, user):
        h_obj = "user:"+user.email
        return user.check_password(self.redis.hget(h_obj, 'pswdh'))
    
    def is_existed_user(self, user):
        return self.redis.sismember('users', user.email)

    def debug(self):
        print(self.redis.keys())
