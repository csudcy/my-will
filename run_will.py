#!/usr/bin/env python
from clint.textui import puts
from will.main import WillBot
import settings


"""
The below is copied from https://github.com/skoczen/will/blob/master/will/main.py
It seems that sleekxmpp resolves URLs to IPs if no address is provided to connect
( see https://github.com/fritzy/SleekXMPP/blob/master/sleekxmpp/clientxmpp.py#L149 )
Therefore, we'll provide an address!
"""
class MyWillBot(WillBot):
    def connect(self, *args, **kwargs):
        # Forcibly set the XMPP address
        kwargs['address'] = ('chat.hipchat.com', 5222)
        WillBot.connect(self, *args, **kwargs)


if __name__ == '__main__':
    bot = MyWillBot()
    bot.bootstrap()
