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
        self.redis.hset(h_obj, 'valid', "True")
        uid = "id:"+self.redis.get('u_count')
        self.redis.set(uid, user.email)

    def is_existed_user(self, email):
        return self.redis.sismember('u_set', email)

    def is_valid_user(self, user):
        h_obj = "user:"+user.email
        return self.redis.hget(h_obj, 'valid') == "True"

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
        user.set_id(id)
        return user

    def add_user_liveSession(self, user, otp_code, session_key):
        h_obj = "live:"+user.email
        key_code = session_key+":code"
        key_used = session_key+":used"
        self.redis.hset(h_obj, key_code, otp_code)
        self.redis.hset(h_obj, key_used, "False")

    def check_user_liveSession(self, user, otp_code, session_key):
        h_obj = "live:"+user.email
        key_code = session_key+":code"
        key_used = session_key+":used"
        is_used = self.redis.hget(h_obj, key_used)
        if is_used == "True":
            return -1
        code = self.redis.hget(h_obj, key_code)
        if code == otp_code:
            self.redis.hset(h_obj, key_used, "True")
            return 1
        else:
            return -1 if code in self.redis.hvals(h_obj) else 0

    def drop_user_liveSession(self, user, session_key):
        h_obj = "live:"+user.email
        key_code = session_key+":code"
        key_used = session_key+":used"
        self.redis.hdel(h_obj, key_code)
        self.redis.hdel(h_obj, key_used)

    def block_user(self, user):
        h_obj = "user:"+user.email
        self.redis.hset(h_obj, 'valid', "False")

    def debug(self):
        print(self.redis.keys())
