import redis


class RedisCache:

    def __init__(self, password=None, host='127.0.0.1', port=6379, db=0, decode_responses=True, charset='utf8'):
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.decode_responses = decode_responses
        self.charset = charset
        self.pool = redis.ConnectionPool(host=self.host,
                                         port=self.port,
                                         password=self.password,
                                         db=self.db,
                                         decode_responses=self.decode_responses,
                                         encoding=self.charset)

    @staticmethod
    def redis():
        return RedisCache(host='10.10.10.21', port=6379, db=11, password=123456)

    def set_ex(self, key, value, seconds):
        _redis = redis.Redis(connection_pool=self.pool)
        _redis.set(key, value, ex=seconds)
        _redis.close()

    def set(self, key, value):
        _redis = redis.Redis(connection_pool=self.pool)
        _redis.set(key, value)
        _redis.close()

    def get(self, key):
        _redis = redis.Redis(connection_pool=self.pool)
        data = _redis.get(key)
        _redis.close()
        return data

    def delete(self, key):
        _redis = redis.Redis(connection_pool=self.pool)
        _redis.delete(key)
        _redis.close()
