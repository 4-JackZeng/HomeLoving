import os


MYSQL_DATABASES={
    'DRIVER':'mysql',
    'DH':'pymysql',
    'ROOT':'root',
    'PASSWORD':'123456',
    'HOST':'127.0.0.1',
    'PORT':'3306',
    'NAME':'homeloving'
}



BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# static
STATIC_DIR=os.path.join(BASE_DIR,'static')

# templates路径
TEMPLATES_DIR=os.path.join(BASE_DIR,'templates')
# 上传路径
UPLOAD_DIR=os.path.join(os.path.join('static','media'),'upload')

HOUSE_DIR=os.path.join(os.path.join(os.path.join('static','media'),'upload'),'house')