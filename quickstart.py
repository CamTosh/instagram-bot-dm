from instadm import InstaDM

if __name__ == '__main__':
	# Auto login
	insta = InstaDM(username='your_username', password='your_password', headless=False)
	
	# Send message
	insta.sendMessage(user='username_target', message='Hey !')
	
	# Send group message
	insta.sendGroupMessage(users=['user1', 'user2'], message='Hey !')