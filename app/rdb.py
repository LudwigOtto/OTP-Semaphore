from redis import Redis, RedisError
from user import User

class RDB():
    def __init__(self, host='localhost', port=6379):
        self.redis = Redis(host=host, port=port, decode_responses=True)

    def add_user(self, user):
        self.redis.incrby('u_count',1)
        self.redis.sadd('u_set', user.email)
        h_obj = "user:"+user.email
        self.redis.hset(h_obj, 'email', user.email)
        self.redis.hset(h_obj, 'pswdh', user.password_hash)
        self.redis.hset(h_obj, 'id', self.redis.get('u_count'))
        uid = "id:"+self.redis.get('u_count')
        self.redis.set(uid, user.email)

    def is_existed_user(self, email):
        return self.redis.sismember('u_set', email)

    def query_user_by_mail(self, email):
        h_obj = "user:"+email
        user = User(email)
        user.set_pwdhash(self.redis.hget(h_obj, 'pswdh'))
        user.set_id(self.redis.hget(h_obj, 'id'))
        return user

    def query_user_by_id(self, id):
        uid = "id:"+id
        email = self.redis.get(uid)
        user = User(email)
        #user.set_pwdhash(self.redis.hget(h_obj, 'pswdh'))
        user.set_id(id)
        return user

    def add_user_liveSession(self, user, otp_code, session_key):
        h_obj = "live:"+user.email
        self.redis.hset(h_obj, session_key, otp_code)

    def check_user_liveSession(self, user, otp_code, session_key):
        h_obj = "live:"+user.email
        code = self.redis.hget(h_obj, session_key)
        if code == otp_code:
            return 1
        else:
            return -1 if code in self.redis.hvals(h_obj) else 0

    def drop_user_liveSession(self, user, session_key):
        h_obj = "live:"+user.email
        self.redis.hdel(h_obj, session_key)

    def debug(self):
        print(self.redis.keys())
