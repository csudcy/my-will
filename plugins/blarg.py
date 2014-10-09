from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class BlargPlugin(WillPlugin):

    @hear("blarg")
    def blarg(self, message):
        return self.reply(message, 'Hi Danny!')
