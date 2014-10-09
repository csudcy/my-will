from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers import quest

class QuestPlugin(WillPlugin):


	@respond_to("^start a quest")
	def quest_start(self, message):
	if not quest.is_started:
		quest.start_quest(message.sender.nick)
	else: 
		self.say("Sorry, {0} a quest is already in progress".format(message.sender.nick))

	@respond_to("^aye$"))
	def quest_join(self, message):
		if quest.add_user(message.sender.nick):
			self.say("You are added to the quest {0}!".format(message.sender.nick))

	@respond_to("^end quest"))
	def quest_end(self, message):
		if quest.user_in_quest(messsage.sender.nick) and quest.status == 'started':
			quest.end_quest()
			self.say("You ended the quest to the quest {0}!".format(message.sender.nick))


	@respond_to("^north$")
	def move_north(self, message):
		if quest.users_go(messsage.sender.nick) and quest.status == 'started':
			response = quest.move_north(message)
			self.say(response)

	@respond_to("^north$")
	def move_south(self, message):
		if quest.users_go(messsage.sender.nick) and quest.status == 'started':
			response = quest.move_south(message)
			self.say(response)

	@respond_to("^east$")
	def move_east(self, message, e):
		if quest.users_go(messsage.sender.nick) and quest.status == 'started':
			response = quest.move_east(message)
			self.say(response)

	@respond_to("^east$")
	def move_west(self, message, e):
		if quest.users_go(messsage.sender.nick) and quest.status == 'started':
			response = quest.move_west(message)
			self.say(response)

	@respond_to("^use (?P<item>.*)$")
	def use(self, message, item):
		if quest.users_go(messsage.sender.nick) and quest.status == 'started':
			response = quest.use(item)
			self.say(response)

	@respond_to("^use (?P<monster>.*)$")
	def attack(self, message, monster):
		if quest.users_go(messsage.sender.nick) and quest.status == 'started':
			response = quest.attack(monster)
			self.say(response)

	@respond_to("^pick up (?P<item>.*)$")
	def pick_up(self, message, item):
		if quest.users_go(messsage.sender.nick) and quest.status == 'started':
			response = quest.pick_up(item)
			self.say(response)

	"""
	@hear('^($')
	def quest_response(self, message):
		if quest.user_whos_go(message.sender.nick):
			response = quest.enter_instruction(message)
			self.say(response)
	"""

    #@respond_to("^define (?P<word>[a-zA-Z]+)$")
    #def define(self, message, word):
    #    """
    # #   define ___: Get the definition of a word
    # #   """
    #    return self.reply(message, self.dictionary.get_definition(word))
