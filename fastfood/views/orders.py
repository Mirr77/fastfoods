''' import modules '''
from flask import jsonify, request
from fastfood.views import api
from fastfood.models.orders import Order, Menu
from db.dbsetup import open_connection


@api.route('/')
def index():
    return jsonify({'message': 'THIS IS V1 Fast Foods'})


@api.route('users/orders', methods=['POST', 'GET'])
def orders():
    ''' Make an order '''
    conn = open_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        order_desc = request.get_json('order_desc')['order']
        user_id = request.get_json('user_id')['user_id']

        if not order_desc or order_desc == " ":
            response = jsonify({"message": "You have not made an order"})
            response.status_code = 400
            return response

        if not request.json:
            response = jsonify({"message": "incorrect request format"})
            response.status_code = 400
            return response

        Order(str(order_desc))
        cur.execute("update users set orders = array_append(orders, '{}') where user_id = {}".format(order_desc, user_id))
        conn.commit()
        return jsonify({'message': "your order has been created"})

    user_id = request.get_json('user_id')['user_id']
    cur.execute("select orders from users where user_id ={}".format(user_id))
    orders = cur.fetchall()
    return jsonify({"orders": orders})


@api.route('/orders/<order_id>', methods=['GET', 'DELETE'])
def get_order(order_id):
    ''' Get one order function '''
    if request.method == 'GET':
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("select * from orders where order_id = {}".format(order_id))
        order = cur.fetchone()

    if len(order) == 0:
        response = jsonify({"message": "Cannot find that order"})
        response.status_code = 404
        return response

    return jsonify({"order": order})

    conn = open_connection()
    cur = conn.cursor()
    cur.execute("delete from orders where order_id = {}".format(order_id))
    cur.close()
    return jsonify({'message': " Order deleted successfully"})


@api.route('/menu', methods=['POST','GET'])
def menu():
    if request.method == 'GET':
        item = request.get_json('item')['item']
        cost = request.get_json('cost')['cost']

        Menu(str(item), cost)
        return jsonify({'message': "entry has been made to menu"})