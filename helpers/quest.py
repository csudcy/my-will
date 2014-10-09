from random import random
import ujson as json

class Quest(object):

	#status = 'ended'
	status = 'started'
	coordinates = [0,0]
	#users = []
	users = ['test']
	turn = 0
	dungeon_map = {
		'[0,0]':{
			'description':
				'This is the start room. Nothing is here except a creeping dread which is now seeping into your soul. You can go north',
			'items':{
				'RedBull': {
					'uses': {
						'inc_health': 2
					}
				}
			}
		},
		'[0,1]':{
			'description':
				'Deeper now. Some sounds echo from the next room. Something huge rears its head about you, it\'s a SharkInATornade!',
			'monsters':[
				{
					'name': 'SharkInATornado',
					'health': 3,
					'power': 1
				}
			]
		}
	}
	#dungeon_map = {<json dump of array coords>, {'description': <string>, 'items': <items>, 'monsters': [{'name': <name>, 'health': <int>, 'power': <int> ]}}
	items = {}
	#items = {<name>: {'description': <string>, 'uses': {<item>: <response> }}}
	health = 10
	luck = 0.5

	def start_quest(self, name):
		self.status = 'started'
		self.turn = 0
		self.users.append(name)
		return 'Those who want to be a part of the quest say aye:' + self.dungeon_map[json.dumps(self.coordinates)]['description']

	def add_user(self, name):
		if self.status == 'started':
			self.users.append(name)

	def users_turn(self, name):
		if name == self.users[turn]:
			return True
		else:
			return False

	def user_in_quest(self, name):
		if name in self.users: 
			return True
		else:
			return False

	def end_quest(self):
		if self.status == 'started':
			self.status == 'ended'
		else:
			return 'The game hasn\'t begun yet you numpty'

	def move_north(self, message):
		next_move = [self.coordinates[0], self.coordinates[1]+1]
		return self.try_move(message, next_move)


	def move_south(self, message):
		next_move = [self.coordinates[0], self.coordinates[1]+1]
		return self.try_move(message, next_move)


	def move_east(self, message):
		next_move = [self.coordinates[0]+1, self.coordinates[1]]
		return self.try_move(message, next_move)


	def move_west(self, message):
		next_move = [self.coordinates[0]-1, self.coordinates[1]]
		return self.try_move(message, next_move)


	def try_move(self, message, next_move):
		if json.dumps(next_move) in self.dungeon_map.keys():
			self.coordinates = next_move
			self.on_return(self.dungeon_map[json.dumps(next_move)]['description'])
		else: 
			self.on_return('Sorry {0}, but you can\'t move there'.format(message.sender.nick))

	def use(self, entry):
		for item in self.items.keys():
			if item in str(entry).lower():
				for use in self.items[item]['uses'].keys():
					if use in str(entry).lower():
						response = self.use_item(use, message)
						self.on_return_monster('You successfully used {0} in conjunction with {1}, causing {2}'.format(item, use, reponse))
					return self.on_return_monster('Sorry you can\'t use {0} like that'.format(item))
		return self.on_return_monster('Sorry you don\'t have that item')

	def attack(self, entry):
		for monster in self.dungeon_map[json.dumps(self.coordinates)].get('monsters', []):
			if monster['name'] in str(entry).lower():
				return self.attack_monster(monster, message)
	
		self.on_return_monster('There are no monsters of that name')
		
	def pick_up(self, entry):
		for item in self.dungeon_map[json.dumps(self.coordinates)].get('items', {}).keys():
			if item in str(entry).lower():
				items.update(self.dungeon_map[json.dumps(self.coordinates)].get('items')[item])
				del self.dungeon_map[json.dumps(self.coordinates)].get('items')[item]
				self.on_return_monster('You now have {0} in your inventory'.format(item))
		self.on_return_monster('That item is not here')

	def monster_attack(self):
		for monster in self.dungeon_map[json.dumps(self.coordinates)].get('monsters', []):
			if random() < self.luck:
				self.health = self.health - monster['power']
				return 'but the {0} then dealt you {1} damage'.format(monster['name'], monster['power'])
			if self.health <= 0:
				self.status ='ended'
				return 'The {0} slowly dismembers you in truely terrifying ways. You are dead'.format(monster['name'])
		return ''

	def on_return_monster(self, response):
		self.turn = self.turn + 1 % len(self.users)
		monster_response = self.monster_attack()
		return response + monster_response

	def on_return(self,response):
		self.turn = self.turn + 1 % len(self.users)
		return response

	def use_item(self, use, message):
		if 'inc health' in self.items[item]['uses'][use]:
			self.health =+ self.items[item]['uses'][use]['inc_health']
			return 'You increased your health by {0} to {1}'.format(self.items[item]['uses'][use]['inc_health'], self.health)
		elif 'kill_monster' in self.items[item]['uses'][use]:
			if len(self.dungeon_map[json.dumps(self.coordinates)].get('monsters'), []) > 1:
				for monster in self.dungeon_map[json.dumps(self.oordinates)].get('monsters', []):
					if monster['name'] in message:
						del monster
						return 'You killed the {0}'.format(monster)
		else:
			self.status = 'ended'
			return 'The item did something charmingly unexpected, and now you are dead'

	def attack_monster(self, monster):
		if random() < self.luck:
			monster['health'] = moster['health'] - self.power
			return 'The {0} took {1} damage'.format(monster['name'], monster['power'])
		else: 
			return 'You missed'

quest = Quest()

class TestObject(object):
	pass

if __name__ == '__main__':
	message = TestObject()
	setattr(message, 'sender', TestObject())	
	message.sender.nick = 'Test'
	print quest.pick_up('RedBull')
	print quest.move_north(message)
	print quest.attack('SharkInATornado')
	print quest.attack('SharkInATornado')
	print quest.attack('SharkInATornado')
	print quest.attack('SharkInATornado')
