import os
import re

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import LoginManager

from utils.settings import UPLOAD_DIR

login_manager=LoginManager()

from user.models import db, User
from utils import status_code
from utils.funtions import is_login

user_blueprint=Blueprint('user',__name__)

# login_manager=LoginManager()


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建成功'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

@user_blueprint.route('/register/',methods=['GET','POST'])
def register():
    # form=UserRegisterForm()
    if request.method=='GET':
        return render_template('register.html')
    if request.method=='POST':
        form=request.form
        # ImmutableMultiDict([('mobile', '12'), ('passwd', '12'), ('passwd2', '12')])
        mobile=form.get('mobile')
        passwd=form.get('passwd')
        passwd2=form.get('passwd2')
        if not all([mobile,passwd,passwd2]):
            return jsonify(status_code.USER_LOGIN_PARAMS_ERROR)
        if not re.match(r'^1\d{10}$',mobile):
            return jsonify(status_code.USER_LOGIN_PHONE_ERROR)
        if User.query.filter(User.phone==mobile).count():
            return jsonify(status_code.USER_REGISTER_USER_PHONE_EXSITS)
        user=User()
        user.phone=mobile
        user.name=mobile
        user.password=passwd
        try:
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except:
            return jsonify(status_code.USER_REGISTER_USER_ERROR)


@user_blueprint.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
       return render_template('login.html')
    if request.method == 'POST':
        form=request.form
        mobile=form.get('mobile')
        passwd=form.get('password')
        if not all(['mobile','passwd']):
            return jsonify(status_code.USER_LOGIN_PARAMS_ERROR)
        if not re.match(r'^1\d{10}$',mobile):
            return jsonify(status_code.USER_LOGIN_PHONE_ERROR)
        user=User.query.filter(User.phone==mobile).first()
        if user:
            # pwd_hash=user.pwd_hash
            if not user.check_pwd(passwd):
                return jsonify(status_code.USER_LOGIN_PASSWORD_ERROR)
            else:
                session['user_id']=user.id
                return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.USER_LOGIN_USER_NOT_EXSITS)


@user_blueprint.route('/my/')
@is_login
def my():
        user_id=session['user_id']
        user=User.query.get(user_id)
        img_avatar=user.avatar
        if img_avatar==None:
            img_file=None
        # 'upload\\banner04.jpg'
        else:
            img_file='/static/media/'+img_avatar
        name=user.name
        phone=user.phone
        return render_template('my.html',img_file=img_file,name=name,phone=phone)


@user_blueprint.route('/profile/',methods=['GET','PUT'])
@is_login
def profile():
    if request.method=='GET':
        session_id = session['user_id']
        user = User.query.all()[session_id-1]
        avatar=user.avatar
        if avatar==None:
            avatar=''

        else:
           avatar='/static/media/'+ avatar + '/'


        # upload_avatar_path = User.query.get('avatar')
        # avatar_url='/static/media/'+upload_avatar_path

        return render_template('profile.html',avatar=avatar)


    if request.method=='PUT':
        form=request.form
        file=request.files
        if 'avatar' in file:
            avatar=request.files.get('avatar')
            user_id=session['user_id']
            # 保存图片
            if avatar:
                # os.path.join(file,name)
                # 第一个参数file是要进入的文件夹路径，当前在file文件，要进入file文件下，name是给进入的目录命名
                avatar.save(os.path.join(UPLOAD_DIR,avatar.filename))
                # 修改用户头像

            user=User.query.get(user_id)
            upload_avatar_path=os.path.join('upload',avatar.filename)
            user.avatar=upload_avatar_path
            user.add_update()
            return jsonify(code=status_code.OK,avatar=upload_avatar_path)
        elif 'name' in form:
            name=form.get('name')
            # 先判断用户名是否存在
            if User.query.filter(User.name==name).count():
                return jsonify(status_code.USER_REGISTER_USER_IS_EXSITS)
            else:
                user=User.query.get(session['user_id'])
                user.name=name
                user.add_update()

                return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.PARAMS_ERROR)

@user_blueprint.route('/show_id/')
def show_id():
    user_id = session['user_id']
    # 根据编号查询当前用户
    user = User.query.get(user_id)
    # 返回用户的真实姓名、身份证号
    id_card = user.id_card
    id_name = user.id_name
    return jsonify(user.to_auth_dict())



@user_blueprint.route('/auth/',methods=['GET','POST'])
@is_login
def auth():
    if request.method=='GET':
        return render_template('auth.html')
    if request.method == 'POST':
        id_name=request.form.get('id_name')
        id_card=request.form.get('id_card')
        if not all([id_name,id_card]):
            return jsonify(status_code.PARAMS_ERROR)
        # 判断身份证是否合法
        # if not re.match(r'^[1-9]\d{17}$',id_card):
        #     return jsonify(status_code.USER_REGISTER_AUTH_ERROR)
        try:
            user=User.query.get(session['user_id'])
        except:
            return jsonify(status_code.DATABASE_ERROR)
            # 判断身份证是否存在
        if user.id_card == id_card:
            return jsonify(status_code.USER_REGISTER_USER_IS_EXSITS)
        try:
            user.id_card=id_card
            user.id_name=id_name
            user.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(status_code.SUCCESS,id_card=id_card,id_name=id_name)



@user_blueprint.route('/logout/',methods=['DELETE'])
def logout():
    if request.method=='DELETE':
        # del session['user_id']
        # 删除session中的user_id
        session.pop('user_id')
        return jsonify(status_code.SUCCESS)
