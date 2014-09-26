#!/usr/bin/env python
from will.main import WillBot


"""
The below is copied from https://github.com/skoczen/will/blob/master/will/main.py
It seems that sleekxmpp resolves URLs to IPs if no address is provided to connect
( see https://github.com/fritzy/SleekXMPP/blob/master/sleekxmpp/clientxmpp.py#L149 )
Therefore, we'll provide an address!
"""
class MyWillBot(WillBot):
    def connect(*args, **kwargs):
        if 'address' not in kwargs:
            kwargs['address'] = (settings.HIPCHAT_SERVER, 5222)
        WillBot.connect(self, *args, **kwargs)


if __name__ == '__main__':
    bot = MyWillBot()
    bot.bootstrap()
