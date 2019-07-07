import json
from instadm import InstaDM

if __name__ == '__main__':
	config = json.loads(open('config.json', 'r').read())
	
	username = config['config']['username']
	password = config['config']['password']
	
	selectors = config['selectors']

	insta = InstaDM(username, password, selectors)
	
	messages = config['config']['messages']
	targets = config['config']['targets']

	for user in targets:
		msg = choice(messages)
		insta.sendMessage(user, msg)