''' import modules'''
from db.dbsetup import open_connection


class Order(object):

    ''' Question Model '''
    def __init__(self, order_desc):
        self.order_desc = order_desc
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("insert into orders(order_desc) values('{}')".format(order_desc))
        cur.close()
        conn.commit()


class Menu(object):

    ''' Menu Model '''
    def __init__(self, item, cost):
        self.item = item
        self.cost = cost
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("insert into menu(item,cost) values('{}',{})".format(item, cost))
        cur.close()
        conn.commit()
