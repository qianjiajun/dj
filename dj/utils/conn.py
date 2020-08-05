import json
import os

from dj.utils.cache import RedisCache
from django.conf import settings

from dj.utils.sql import MsMysql, MsOracle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")


class ConnUtil:
    db_size = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    @staticmethod
    def get_settings(settings_name):
        return settings.CUSTOM_SETTINGS[settings_name]

    @staticmethod
    def get_redis(db: int = None):
        redis_settings = settings.REDIS_CONN
        if db not in ConnUtil.db_size:
            db = redis_settings['db']
        return RedisCache(host=redis_settings['host'], port=redis_settings['port'], db=db,
                          password=redis_settings['password'])

    @staticmethod
    def get_db(db_name='master'):
        db_settings = settings.DATABASE_CONN[db_name]
        if db_settings['dbType'] == 'mysql':
            return MsMysql(host=db_settings['host'], user=db_settings['user'], password=db_settings['password'],
                           database=db_settings['database'], port=db_settings['port'])
        elif db_settings['dbType'] == 'oracle':
            return MsOracle(username=db_settings['username'], password=db_settings['password'], url=db_settings['url'])
        else:
            raise Exception("数据库错误，当前配置信息有误，请检查, {info}".format(info=json.dumps(db_settings)))
