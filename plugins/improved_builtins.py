import re

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class ImprovedBuiltinsPlugin(WillPlugin):

    @respond_to("^help(?P<search>.*?)$")
    def help(self, message, search):
        """help ___: Search help for ___"""
        plugin_groups = self.load("help_modules", default=[])

        self.reply(message, 'Sure thing!')
        output = "Here's what I know how to do:"

        search = search.strip()
        if search:
            search_re = '.*%s.*' % search
        else:
            search_re = '.+'

        for k in sorted(plugin_groups, key=lambda x: x[0]):
            plugins = plugin_groups[k]

            plugins = [plugin.strip() for plugin in plugins if re.match(search_re, plugin, flags=re.DOTALL)]

            if plugins:
                output += "<br/><br/><b>%s</b>:" % k
                for plugin in sorted(plugins):
                    if ":" in plugin:
                        index = plugin.find(":")
                        plugin = "<b>%s</b>%s" % (plugin[:index], plugin[index:])
                    output += "<br/> &nbsp; %s" % plugin

        self.say(output, message=message, html=True)

    @respond_to("^programmer help(?P<search>.*?)$")
    def programmer_help(self, message, search):

        # Prepare our search
        search = search.strip()
        if search:
            search_re = '.*%s.*' % search
        else:
            search_re = '.+'

        # Get the list of all regexes Will listens for
        all_regexes = self.load("all_listener_regexes")

        # Output everything that matches our search
        output = "Here's everything I know how to listen to:"
        for r in all_regexes:
            if re.match(search_re, r, flags=re.DOTALL):
                output += "\n%s" % r

        self.reply(message, output)

    @respond_to("^roster rooms$")
    def list_rooms(self, message):
        context = {"rooms": self.available_rooms.values(),}
        self.say(rendered_template("rooms.html", context), message=message, html=True)

    @respond_to("^roster users$")
    def list_roster(self, message):
        context = {"internal_roster": self.internal_roster.values(),}
        self.say(rendered_template("roster.html", context), message=message, html=True)

    @respond_to("^roster update$")
    def update_rooms(self, message):
        # Clear & update the roster
        self.save('will_roster', {})
        self.reply(message, "Rooms & users cleared")
        self.reply(message, "IMPORTANT: You must now manually restart me to refresh the rooms list!")
