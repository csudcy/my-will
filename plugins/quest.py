from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.quest import quest

class QuestPlugin(WillPlugin):


    @respond_to("^start a quest game$")
    def quest_start(self, message):
        if quest.status == 'ended':
            response =  quest.start_quest(message.sender.nick)
            self.reply(message, response)
        else:
            self.reply(message, "Sorry, {0} a quest is already in progress".format(message.sender.nick))

    @respond_to("^join$")
    def quest_join(self, message):
        if quest.add_user(message.sender.nick):
            self.reply(message, "You are added to the quest {0}!".format(message.sender.nick))

    @respond_to("^end quest game$")
    def quest_end(self, message):
        if quest.user_in_quest(message.sender.nick) and quest.status == 'started':
            quest.end_quest()
            self.reply(message, "You ended the quest to the quest {0}!".format(message.sender.nick))
        else:
            self.reply(message, "There is no game in progress")

    @respond_to("^north$")
    def move_north(self, message):
        if quest.users_turn(message.sender.nick) and quest.status == 'started':
            response = quest.move_north(message)
            print 'response from move north {0}'.format(response)
            self.reply(message, response)

    @respond_to("^south$")
    def move_south(self, message):
        if quest.users_turn(message.sender.nick) and quest.status == 'started':
            response = quest.move_south(message)
            self.reply(message, response)

    @respond_to("^east$")
    def move_east(self, message):
        if quest.users_turn(message.sender.nick) and quest.status == 'started':
            response = quest.move_east(message)
            self.reply(message, response)

    @respond_to("^west$")
    def move_west(self, message):
        if quest.users_turn(message.sender.nick) and quest.status == 'started':
            response = quest.move_west(message)
            self.reply(message, response)

    @respond_to("^use (?P<item>.*)$")
    def use(self, message, item):
        print 'using'
        if quest.users_turn(message.sender.nick) and quest.status == 'started':
            response = quest.use(item)
            print 'response to use is {0}'.format(response)
            self.reply(message, response)

    @respond_to("^attack (?P<monster>.*)$")
    def attack(self, message, monster):
        print 'attacking'
        if quest.users_turn(message.sender.nick) and quest.status == 'started':
            response = quest.attack(monster)
            print 'response to atack is {0}'.format(response)
            self.reply(message, response)

    @respond_to("^pick up (?P<item>.*)$")
    def pick_up(self, message, item):
        print 'picking up'
        if quest.users_turn(message.sender.nick) and quest.status == 'started':
            response = quest.pick_up(item)
            print 'response to pick up is {0}'.format(response)
            self.reply(message, response)
