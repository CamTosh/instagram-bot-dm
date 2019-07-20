from selenium import webdriver
from random import randint
from time import sleep
import logging
import sqlite3

class InstaDM(object):
	
	def __init__(self, username, password, headless=True, instapy_workspace=None):
		self.selectors = {
	      "home_to_login_button": ".WquS1 a",
	      "username_field": "username",
	      "password_field": "password",
	      "button_login": "._0mzm-",
	      "search_user": "queryBox",
	      "select_user": "._0mzm-",
	      "textarea": "textarea",
	      "send": "button"
	    }

		# Selenium config
		options = webdriver.ChromeOptions()

		if headless:
			options.add_argument("--headless")
		
		mobile_emulation = {
			"userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
		}
		options.add_experimental_option("mobileEmulation", mobile_emulation)                         

		self.driver = webdriver.Chrome(options=options)
		self.driver.set_window_position(0, 0)
		self.driver.set_window_size(414, 736)
		
		# Instapy init DB
		self.instapy_workspace = instapy_workspace
		self.conn = None
		self.cursor = None
		if self.instapy_workspace != None:
			self.conn = sqlite3.connect(self.instapy_workspace + "InstaPy/db/instapy.db")
			self.cursor = CONN.cursor()

			cursor = CONN.execute(```
				SELECT count(*)
				FROM sqlite_master
				WHERE type='table'
				AND name='message';
			```)
			count = cursor.fetchone()[0]

			if count == 0:
				CONN.execute(```
					CREATE TABLE "message" (
						"username"	TEXT NOT NULL UNIQUE,
						"message"	TEXT DEFAULT NULL,
						"sent_message_at"	TIMESTAMP
					);
				```)

		try:
			self.login(username, password)
		except Exception as e:
			logging.error(e)

	def login(self, username, password):
		# homepage
		self.driver.get('https://instagram.com')
		self.__randomSleep__(3, 5)
		self.driver.find_elements_by_css_selector(self.selectors['home_to_login_button'])[0].click()
		self.__randomSleep__(2, 4)
		
		# login
		logging.info('Login with {}'.format(username))
		self.__scrolldown__()
		self.driver.find_element_by_name(self.selectors['username_field']).send_keys(username)
		self.driver.find_element_by_name(self.selectors['password_field']).send_keys(password)
		self.driver.find_elements_by_css_selector(self.selectors['button_login'])[2].click()
		self.__randomSleep__()

	def sendMessage(self, user, message):
		logging.info('Send message {} to {}'.format(message, user))
		self.driver.get('https://www.instagram.com/direct/new/')
		self.driver.find_element_by_name(self.selectors['search_user']).send_keys(user)
		self.__randomSleep__()

		# Select user
		elements = self.driver.find_elements_by_css_selector(self.selectors['select_user'])
		elements[2].click()
		self.__randomSleep__()
		
		# Go to page
		elements[0].click()
		self.__randomSleep__()
		self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)

		self.__randomSleep__()
		buttons = self.driver.find_elements_by_css_selector(self.selectors['send'])
		buttons[len(buttons)-1].click()

		if self.conn != None:
			self.cursor.execute('INSERT INTO message (username, message) VALUES(?, ?)', (user, message))
			self.conn.commit()

		self.__randomSleep__()

	def sendGroupMessage(self, users, message):
		logging.info('Send group message {} to {}'.format(message, str(users)))
		self.driver.get('https://www.instagram.com/direct/new/')

		searchInput = self.driver.find_element_by_name(self.selectors['search_user'])
		usersAndMessages = []
		for user in users:
			if self.conn != None:
				usersAndMessages.append((user, message))
			searchInput.send_keys(user)
			self.__randomSleep__()

			# Select user
			elements = self.driver.find_elements_by_css_selector(self.selectors['select_user'])
			elements[2].click()
			self.__randomSleep__(2, 4)
			#searchInput.clear()
		
		# Go to page
		elements[0].click()
		self.__randomSleep__()
		self.driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)
		self.__randomSleep__()
		buttons = self.driver.find_elements_by_css_selector(self.selectors['send'])
		buttons[len(buttons)-1].click()

		if self.conn != None:
			self.cursor.executemany('''
				INSERT OR IGNORE INTO message (username, message) VALUES(?, ?)
			''', usersAndMessages)
			self.conn.commit()

		self.__randomSleep__()


	def __randomSleep__(self, min = 2, max = 10):
		t = randint(min, max)
		logging.info('Wait {} seconds'.format(t))
		sleep(t)

	def __scrolldown__(self):
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


