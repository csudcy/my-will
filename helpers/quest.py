from random import random
import ujson as json

class Quest(object):

	status = 'ended'
	coordinates = [0,0]
	users = []
	turn = 0
	dungeon_map = {
		'[0,0]':{
			'description':
				'This is the start room. Nothing is here except a creeping dread which is now seeping into your soul. There is RedBull you can pick up. You can go north',
			'items':[
				{
					'name': 'redbull',
					'use': {
						'inc_health': 2
					}
				}
			]
		},
		'[0,1]':{
			'description':
				'Deeper now. Some sounds echo from the next room. Something huge rears its head about you, it\'s a SharkInATornade!',
			'monsters':[
				{
					'name': 'sharkinatornado',
					'health': 3,
					'power': 1
				}
			]
		}
	}
	#dungeon_map = {<json dump of array coords>, {'description': <string>, 'items': <items>, 'monsters': [{'name': <name>, 'health': <int>, 'power': <int> ]}}
	items = []
	#items = {<name>: {'description': <string>, 'uses': {<item>: <response> }}}
	health = 10
	luck = 0.5
	power = 1

	def start_quest(self, name):
		self.status = 'started'
		self.turn = 0
		self.users.append(name)
		return 'Those who want to be a part of the quest say join:' + self.dungeon_map[json.dumps(self.coordinates)]['description']

	def add_user(self, name):
		if self.status == 'started':
			self.users.append(name)

	def users_turn(self, name):
		if name == self.users[self.turn-1]:
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

	def move_north(self, message):
		next_move = [self.coordinates[0], self.coordinates[1]+1]
		return self.try_move(message, next_move)


	def move_south(self, message):
		next_move = [self.coordinates[0], self.coordinates[1]-1]
		return self.try_move(message, next_move)


	def move_east(self, message):
		next_move = [self.coordinates[0]+1, self.coordinates[1]]
		return self.try_move(message, next_move)


	def move_west(self, message):
		next_move = [self.coordinates[0]-1, self.coordinates[1]]
		return self.try_move(message, next_move)


	def try_move(self, message, next_move):
		print 'trying to move to {0} from {1}'.format(str(next_move), self.coordinates)
		if json.dumps(next_move) in self.dungeon_map.keys():
			self.coordinates = next_move
			return self.before_return(self.dungeon_map[json.dumps(next_move)]['description'], False)
		else: 
			return self.before_return('Sorry {0}, but you can\'t move there'.format(message.sender.nick), False)

	def use(self, entry):
		print 'items are {0}'.format(str(self.items))
		for item in self.items:
			if item['name'] in str(entry).lower():
				#for use in self.items[item]['uses'].keys():
			#		if use in str(entry).lower():
					response = self.use_item(item['use'], message)
					del item
					return self.before_return('You successfully used {0} in conjunction with {1}, causing {2}'.format(item['name'], item['use'], response), True)
			#		return self.before_return('Sorry you can\'t use {0} like that'.format(item), True)
					
		return self.before_return('Sorry you don\'t have that item', True)

	def attack(self, entry):
		print 'monsters to attack are {0}'.format(str(self.dungeon_map[json.dumps(self.coordinates)].get('monsters', [])))
		for monster in self.dungeon_map[json.dumps(self.coordinates)].get('monsters', []):
			if monster['name'] in str(entry).lower():
				print 'attacking {0}'.format(monster['name'])
				return self.attack_monster(monster)
	
		return self.before_return('There are no monsters of that name', True)

	def pick_up(self, entry):
		for item in self.dungeon_map[json.dumps(self.coordinates)].get('items', {}):
			if item['name'] in str(entry).lower():
				self.items.append(item)#self.dungeon_map[json.dumps(self.coordinates)].get('items')[item])
				del item#self.dungeon_map[json.dumps(self.coordinates)].get('items')[item]
				return self.before_return('You now have {0} in your inventory'.format(item['name']), True)
		return self.before_return('That item is not here', True)

	def monster_attack(self):
		print 'monsters to be attacked by are {0}'.format(str(self.dungeon_map[json.dumps(self.coordinates)].get('monsters', [])))
		for monster in self.dungeon_map[json.dumps(self.coordinates)].get('monsters', []):
			if random() < self.luck:
				self.health = self.health - monster['power']
				return ', but the {0} then dealt you {1} damage'.format(monster['name'], monster['power'])
			if self.health <= 0:
				self.status ='ended'
				return 'The {0} slowly dismembers you in truely terrifying ways. You are dead'.format(monster['name'])
		return ''

	def before_return(self, response, monster=True):
		self.turn = self.turn + 1 % len(self.users)
		print self.turn
		if monster:
			monster_response = self.monster_attack()
			return response + monster_response
		else:
			return response

	def use_item(self, use, message):
		if 'inc health' in self.items[item]['uses'][use]:
			self.health =+ self.items[item]['uses'][use]['inc_health']
			return 'an increase in health from {0} to {1}'.format(self.items[item]['uses'][use]['inc_health'], self.health)
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
			monster['health'] = monster['health'] - self.power
			if monster['health'] <= 0:
				del monster
				return self.before_return('You killed the {0}, you absolute bastard. He had wife and children'.format(monster['name']), True)
			return self.before_return('The {0} took {1} damage'.format(monster['name'], monster['power']), True)
		else: 
			return self.before_return('You missed', True)

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
