from utils.funtions import get_mysql_url


class Config():

    SQLALCHEMY_DATABASE_URI= get_mysql_url()
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY= 'secret_key'

    SESSION_TYPE='redis'

