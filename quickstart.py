from instadm import InstaDM
from selenium import webdriver
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  
# Check if the current version of chromedriver exists
# and if it doesn't exist, download it automatically,
# then add chromedriver to path

if __name__ == '__main__':
	# Auto login
	insta = InstaDM(username='your_username', password='your_password', headless=False)
	
	# Send message
	insta.sendMessage(user='username_target', message='Hey !')
	
	# Send group message
	insta.sendGroupMessage(users=['user1', 'user2'], message='Hey !')