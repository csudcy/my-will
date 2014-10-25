import json
import re

from memoize import Memoizer
import requests


NO_ORDER = 'Sorry, I don\'t know your coffee order :('
SET = 'Ok, your coffee order is now {order}'
CLEAR = 'Ok, I\'ve removed your coffee order'
GET = 'Your coffee order is {order}'
GET_ALL_USER_ORDER = '@{user}: {order}'
GET_ALL_ORDERS = """Here are the orders:
{orders}
"""

PARTICIPANTS_URL = "https://{server}/v2/room/{room_id}/participant?auth_token={token}"

store = {}
memo = Memoizer(store)

class Coffee(object):
    KEY = 'coffee_orders'

    def __init__(self, load, save, server, token):
        self.load = load
        self.save = save
        self.server = server
        self.token = token

    _orders = None
    @property
    def orders(self):
        if self._orders is None:
            # Load the orders
            self._orders = self.load(self.KEY, {})
        return self._orders

    def _save_orders(self):
        self.save(self.KEY, self.orders)

    @memo(max_age=60)
    def get_users(self, room_id):
        """
        Get everyone in room_id
        """
        url = PARTICIPANTS_URL.format(
            server=self.server,
            token=self.token,
            room_id=room_id,
        )
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(
            url,
            headers=headers
        )
        data = response.json()
        if 'error' in data:
            raise Exception('Hipchat error: %s' % data['error']['message'])

        return [item['mention_name'] for item in data['items']]

    def set(self, user, order):
        """
        Set the users order
        """
        # Save the new order
        self.orders[user] = order
        self._save_orders()
        return SET.format(order=order)

    def clear(self, user):
        """
        Clear the users order
        """
        if not user in self.orders:
            return NO_ORDER
        del self.orders[user]
        self._save_orders()
        return CLEAR

    def reset(self):
        """
        Reset all orders
        """
        self.orders.clear()
        self._save_orders()

    def get(self, user):
        """
        Get the users order
        """
        if not user in self.orders:
            return NO_ORDER
        order = self.orders[user]
        return GET.format(order=order)

    def get_all(self, room_id=None):
        """
        Get lots of orders
        """
        if room_id:
            # Get everyone in room_id
            users = self.get_users(room_id)
        else:
            # Just return everyone
            users = self.orders.keys()

        # Get all the orders
        orders = []
        unknown_users = []
        for user in users:
            orders.append(
                GET_ALL_USER_ORDER.format(
                    user=user,
                    order=self.orders.get(user, 'I dont know :(')
                )
            )
        orders.sort()

        return GET_ALL_ORDERS.format(
            orders='\n'.join(orders)
        )

if __name__ == '__main__':
    store = {}
    def save(key, value):
        store[key] = value
    def load(key, default=None):
        return store.get(key, default)
    server = 'api.hipchat.com'
    token = '<V2 API token goes here>'
    room_id = '<Room_id goes here>'

    def check():
        c_check = Coffee(load, save, server, token)
        print 'alice : ', c_check.get('alice')
        print 'bob   : ', c_check.get('bob')
        print 'claire: ', c_check.get('claire')
        print c_check.get_all()
        print

    c = Coffee(load, save, server, token)
    check()
    print c.set('alice', 'Skinny decaf soy milk latte with pixie sprinkles')
    check()
    print c.set('bob', 'Triple espresso')
    check()
    print c.set('claire', 'Hot chocolate')
    check()
    print c.clear('bob')
    check()
    print c.clear('claire')
    check()
    print c.clear('alice')
    check()

    print c.set('alice', 'Skinny decaf soy milk latte with pixie sprinkles')
    print c.set('bob', 'Triple espresso')
    print c.set('claire', 'Hot chocolate')
    check()
    print c.reset()
    check()

    if room_id:
        print c.get_users(room_id)
        print c.get_all(room_id)
