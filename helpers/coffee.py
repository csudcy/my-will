NO_ORDER = 'Sorry, I don\'t know your coffee order :('
SET = 'Ok, your coffee order is now {order}'
CLEAR = 'Ok, I\'ve removed your coffee order'
GET = 'Your coffee order is {order}'
GET_ALL_USER_ORDER = '@{user}: {order}'
GET_ALL_ORDERS = """Here are the orders:
{orders}
"""


class Coffee(object):
    KEY = 'coffee_orders'

    def __init__(self, load, save):
        self.load = load
        self.save = save

    _orders = None
    @property
    def orders(self):
        if self._orders is None:
            # Load the orders
            self._orders = self.load(self.KEY, {})
        return self._orders

    def _save_orders(self):
        self.save(self.KEY, self.orders)

    def set(self, user, order):
        # Save the new order
        self.orders[user] = order
        self._save_orders()
        return SET.format(order=order)

    def clear(self, user):
        if not user in self.orders:
            return NO_ORDER
        del self.orders[user]
        self._save_orders()
        return CLEAR

    def reset(self):
        self.orders.clear()
        self._save_orders()

    def get(self, user):
        if not user in self.orders:
            return NO_ORDER
        order = self.orders[user]
        return GET.format(order=order)

    def get_all(self, users=None):
        if users is None:
            users = self.orders.keys()
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

    def check():
        c_check = Coffee(load, save)
        print 'alice : ', c_check.get('alice')
        print 'bob   : ', c_check.get('bob')
        print 'claire: ', c_check.get('claire')
        print c_check.get_all(['alice', 'bob', 'claire'])
        print c_check.get_all()
        print

    c = Coffee(load, save)
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
