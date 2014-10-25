import uuid

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class UUIDPlugin(WillPlugin):

    @respond_to("^uuid me$")
    def uuid_me(self, message):
        """
        uuid me: Generate a UUID v4
        """
        self.reply(message, str(uuid.uuid4()))
