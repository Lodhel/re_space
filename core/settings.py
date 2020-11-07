
DEBUG = False

#  DataBase
DB = {
    "name_db": "re_space",
    "user": "postgres",
    "password": "q319546",
    "host": "localhost",
    "client": "postgresql"
}

if not DEBUG:
    try:
        from local_settings import *
    except ImportError:
        pass

