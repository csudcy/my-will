import re

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class ImprovedHelpPlugin(WillPlugin):

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

            print plugins
            plugins = [plugin.strip() for plugin in plugins if re.match(search_re, plugin, flags=re.DOTALL)]
            print plugins

            if plugins:
                output += "<br/><br/><b>%s</b>:" % k
                for plugin in sorted(plugins):
                    if ":" in plugin:
                        index = plugin.find(":")
                        plugin = "<b>%s</b>%s" % (plugin[:index], plugin[index:])
                    output += "<br/> &nbsp; %s" % plugin

        self.say(output, message=message, html=True)

    @respond_to("^programmer help")
    def programmer_help(self, message):
        all_regexes = self.load("all_listener_regexes")
        output = "Here's everything I know how to listen to:"
        for r in all_regexes:
            output += "\n%s" % r

        self.reply(message, output)
