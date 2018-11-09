import os

from flask import render_template, Blueprint, session, jsonify, request, Config

from user.models import User, House, Facility, HouseImage, Area, Order
from user.user_views import user_blueprint
from utils import status_code
from utils.settings import UPLOAD_DIR, HOUSE_DIR

house_blueprint=Blueprint('house',__name__)


@house_blueprint.route('/newhouse/',methods=['GET'])
def newhouse():
    return render_template('newhouse.html')

@house_blueprint.route('area_facility/', methods=['GET'])
def area_facility():
    areas=Area.query.all()
    facilities=Facility.query.all()
    areas_info=[area.to_dict() for area in areas]
    facility_info=[facility.to_dict() for facility in facilities]
    return jsonify(code=status_code.OK,areas_info=areas_info,facility_info=facility_info)


@house_blueprint.route('/newhouse/',methods=['POST'])
def newhouse_save():
    form=request.form
    # 创建对象并保存
    house=House()
    house.user_id = session['user_id']
    house.area_id = form.get('area_id')
    house.title = form.get('title')
    house.price = form.get('price')
    house.address = form.get('address')
    house.room_count = form.get('room_count')
    house.acreage = form.get('acreage')
    house.beds = form.get('beds')
    house.unit = form.get('unit')
    house.capacity = form.get('capacity')
    house.deposit = form.get('deposit')
    house.min_days = form.get('min_days')
    house.max_days = form.get('max_days')
    facilities = request.form.getlist('facility')
    for f_id in facilities:
        facility=Facility.query.get(f_id)
        # 添加房源和设备的多对多关系
        house.facilities.append(facility)
    house.add_update()
    # 返回结果
    return jsonify(code=status_code.OK,house_id=house.id)


@house_blueprint.route('/image/',methods=['POST'])
def image():
    # 获取房屋编号
    house_id=request.form.get('house_id')
    # 获取图片
    file=request.files
    if 'house_image' in file:
        house_image=request.files.get('house_image')
        user_id=session['user_id']
        if house_image:
            house_image.save(os.path.join(HOUSE_DIR,house_image.filename))

        # 保存图片在house_image表中
        house_img=HouseImage()
        house_img.house_id=house_id
        img_url=os.path.join(HOUSE_DIR,house_image.filename)
        img_url='\%s'%img_url
        house_img.url=img_url
        house_img.add_update()

        # 设置房屋首图
        house=House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url=img_url
            house.add_update()
        return jsonify(code=status_code.OK,img_url=img_url)



@house_blueprint.route('/house_info/')
def house_info():
    # 判断当前登陆系统的用户是否实名认证，如果实名认证，返回该用户的房屋信息
    user=User.query.get(session['user_id'])
    if user.id_card:
        # 已经完成实名认证
        houses=House.query.filter(House.user_id==session['user_id']).all()
        house_info=[house.to_dict() for house in houses]
        return jsonify(code=status_code.OK,house_info=house_info)
    else:
        # 没有实名认证
        return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


@house_blueprint.route('/myhouse/',methods=['GET'])
def myhouse():
    return render_template('myhouse.html')




@house_blueprint.route('/detail/',methods=['GET'])
def detail():
    return render_template('detail.html')


@house_blueprint.route('/detail/<int:id>/',methods=['GET'])
def house_detail(id):
    house=House.query.get(id)
    # 查询设备信息
    facility_list=house.facilities
    facility_dict_list=[facility.to_dict() for facility in facility_list]
    # 判断当前房屋信息是否为当前登陆者所发布信息，如果是隐藏发布按钮
    booking=1
    if 'user_id' in session:
        if house.user_id==session['user_id']:
            booking=0
    return jsonify(code=status_code.OK,house_detail=house.to_full_dict(),facility_list=facility_dict_list,booking=booking)


@house_blueprint.route('/index/')
def index():
    user_id=session.get('user_id')
    print(user_id)
    return render_template('index.html')



@house_blueprint.route('/hindex/')
def my_index():
    # 获取登录信息
    username=''
    if 'user_id' in session:
        user=User.query.get(session['user_id'])
        username=user.name
        code=status_code.OK
    else:
        code=''
    # 返回5个房屋信息
    # 获取房屋的轮播图
    hlist=House.query.order_by(House.id.desc()).all()[:5]
    hlist2=[house.to_dict() for house in hlist]

    # 查找地区信息
    area_list=Area.query.all()
    area_dict_list=[area.to_dict() for area in area_list]
    return jsonify(code=code,name=username,hlist=hlist2,alist=area_dict_list)

    # houses=House.query.filter(House.index_image_url!='').order_by('-id')[:3]
    # houses_info=[house.to_full_dict() for house in houses]
    #
    # return jsonify(code=status_code.OK,username=username,house_info=houses_info)
    #

@house_blueprint.route('/search/')
def search():
    return render_template('search.html')


@house_blueprint.route('/searchall/',methods=['GET'])
def searchall():
    dict=request.args

    sort_key=dict.get('sk')
    a_id=dict.get('aid')
    begin_date=dict.get('sd')
    end_date=dict.get('ed')

    houses=House.query.filter_by(area_id=a_id)
    # 不能查询自己发布的房源，排除当前用户发布的房屋
    if 'user_id' in session:
        hlist=houses.filter(House.user_id!=(session['user_id']))
    # 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除这些房间
    order_list=Order.query.filter(Order.status!='REJECTED')
    # 情况一
    order_list1=Order.query.filter(Order.begin_date>=begin_date,Order.end_date<=end_date)
    order_list2=order_list.filter(Order.begin_date<begin_date,Order.end_date>end_date)
    order_list3=order_list.filter(Order.end_date>=begin_date,Order.end_date<=end_date)
    order_list4 =order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)
    # 获取订单中的房屋编号
    house_ids=[order.house_id for order in order_list2]
    for order in order_list3:
        house_ids.append(order.house_id)
    for order in order_list4:
        if order.house_id not in house_ids:
            house_ids.append(order.house_id)
    # 查询排除入住时间和离开时间在预约时间内的房屋订单信息
    hlist=hlist.filter(House.id.notin_(house_ids))
    # 排序规则，默认根据最新排序
    sort=House.id.desc()
    if sort_key == 'booking':
        sort = House.order_count.desc()
    elif sort_key == 'price-inc':
        sort = House.price.asc()
    elif sort_key == 'price-des':
        sort = House.price.desc()
    hlist = hlist.order_by(sort)
    hlist = [house.to_dict() for house in hlist]

    # 获取区域信息
    area_list=Area.query.all()
    area_dict_list=[area.to_dict() for area in area_list]

    return jsonify(code=status_code.OK,houses=hlist,areas=area_dict_list)


@house_blueprint.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


