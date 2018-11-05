from redis import Redis, RedisError
#from .user import User

class RDB():
    def __init__(self, host='localhost', port=6739):
        self.redis = Redis(host=host, port=port)

    def add_user(self, user):
        pass

    def load_user(self, user):
        pass
