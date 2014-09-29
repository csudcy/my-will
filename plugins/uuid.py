import uuid

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class EmoticonPlugin(WillPlugin, HipchatEmoticonsMixin):

    @respond_to("^uuid me")
    def single(self, message):
        self.reply(message, uuid.uuid4())
