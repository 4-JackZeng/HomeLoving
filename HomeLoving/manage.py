
from flask_script import Manager

from utils.user import  create_user

app=create_user()


manager=Manager(app=app)

if __name__ == '__main__':
    manager.run()
