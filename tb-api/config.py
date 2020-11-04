# -*- encoding: utf-8 -*-

class Config(object):
    video_url = ""
    UPLOAD_FOLDER = ""


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True


class DatabaseConfig(object):
    mysql_conn = {
        "host": "39.96.57.39",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "db": "behavior_data",
        "charset": 'utf8'
    }