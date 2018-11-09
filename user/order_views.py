from datetime import datetime

from flask import Blueprint, request, session, render_template, jsonify

from user.models import House, Order
from utils import status_code

order_blueprint = Blueprint('order', __name__)


@order_blueprint.route('/order/', methods=['POST'])
def order():
    """作为租客下单"""
    if request.method == 'POST':
        dict = request.form
        house_id = int(dict.get('house_id'))

        begin_date = datetime.strptime(dict.get('begin_date'), '%Y-%m-%d')
        end_date = datetime.strptime(dict.get('end_date'), '%Y-%m-%d')
        # 验证数据有效性
        if not all([house_id, begin_date, end_date]):
            return jsonify(status_code.PARAMS_ERROR)
        if begin_date > end_date:
            return jsonify(status_code.ORDER_START_END_TIME_ERROR)
        # 查询房屋对象
        try:
            house = House.query.get(house_id)
        except:
            return jsonify(status_code.DATABASE_ERROR)
        # 创建订单对象
        order = Order()
        order.user_id = session['user_id']
        order.house_id = house_id
        order.begin_date = begin_date
        order.end_date = end_date
        order.days = (end_date - begin_date).days + 1
        order.house_price = house.price
        order.amount = order.days * order.house_price

        try:
            order.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)

        return jsonify(status_code.OK)


@order_blueprint.route('/order/<int:id>/', methods=['PUT'])
def status(id):
    """选择接单还是拒单"""
    if request.method == 'PUT':
        # 获取订单状态
        status = request.form.get('status')
        # 查找订单对象
        order = Order.query.get(id)
        # 修改订单状态
        order.status = status
        # 如果是拒单,添加原因
        if status == 'REJECTED':
            if request.form.get('comment'):
                order.comment = request.form.get('comment')
            else:
                return jsonify(status_code.PARAMS_ERROR)

        try:
            order.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
        return jsonify(status_code.OK)


@order_blueprint.route('/orders/', methods=['GET', 'POST'])
def orders():
    # 作为租客，提交的订单
    if request.method == 'GET':
        return render_template('orders.html')


@order_blueprint.route('/renter/', methods=['GET'])
def renter():
    # 作为租客 查看我的订单
    if request.method == 'GET':
        user_id = session['user_id']
        orders = Order.query.filter(Order.user_id == user_id).order_by(Order.id.desc())
        order_list = [order.to_dict() for order in orders]
        return jsonify(olist=order_list)


@order_blueprint.route('/lorders_list/', methods=['GET'])
def lorders_list():
    # 作为房东，查看客户订单接口
    if request.method == 'GET':
        user_id = session['user_id']
        # 查询当前用户的所有房屋
        hlist = House.query.filter(House.user_id == user_id)

        hid_list = [house.id for house in hlist]
        # 根据房屋编号查看订单
        order_list = Order.query.filter(Order.house_id.in_(hid_list)).order_by(Order.id.desc())
        # 构造结果
        olist = [order.to_dict() for order in order_list]
        # for olist1 in olist:
        #     image=olist1['image']
        #
        #     image1='\%s'%olist1['image']
        #     image=image1
        #
        #
        #
        #     print(image)
        #
        #
        # print('11111')
        return jsonify(olist=olist)


@order_blueprint.route('/lorders/')
def lorders():
    # 作为房东可以查看客户提交的订单
    if request.method == 'GET':
        return render_template('lorders.html')


@order_blueprint.route('/booking/', methods=['GET', 'POST'])
def booking():
    # 进入预定页面
    if request.method == 'GET':
        return render_template('booking.html')
