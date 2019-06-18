import json
from selenium import webdriver
from time import sleep

def scrollToDown(driver):
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

if __name__ == '__main__':
	config = json.loads(open('config.json', 'r').read())
	
	username = config['config']['username']
	password = config['config']['password']
	targets = config['config']['targets']
	message = config['config']['message']

	selectors = config['selectors']
	
	options = webdriver.ChromeOptions()

	# options.add_argument("--headless")	
	mobile_emulation = {
	"userAgent": 'Mozilla/5.0 (Linux; Android 4.0.3; HTC One X Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'
	}
	options.add_experimental_option("mobileEmulation", mobile_emulation)                         

	driver = webdriver.Chrome(options=options)
	driver.set_window_position(0, 0)
	driver.set_window_size(414, 736)
	
	# homepage
	driver.get('https://instagram.com')
	sleep(3)
	driver.find_elements_by_css_selector(selectors['home_to_login_button'])[0].click()
	sleep(2)
	
	# login
	print('Login with {}'.format(username))
	scrollToDown(driver)
	driver.find_element_by_name(selectors['username_field']).send_keys(username)
	driver.find_element_by_name(selectors['password_field']).send_keys(password)
	driver.find_elements_by_css_selector(selectors['button_login'])[2].click()
	sleep(5)
	
	# DM
	for user in targets:
		print('Send message to {}'.format(user))
		driver.get('https://www.instagram.com/direct/new/')
		driver.find_element_by_name(selectors['search_user']).send_keys(user)
		sleep(1)

		# Select user
		elements = driver.find_elements_by_css_selector(selectors['select_user'])
		elements[2].click()
		sleep(3)
		
		# Go to page
		elements[0].click()
		sleep(3)
		driver.find_elements_by_xpath("*//textarea")[0].send_keys(message)
		sleep(4)
		buttons = driver.find_elements_by_css_selector(selectors['send'])
		buttons[len(buttons)-1].click()
		sleep(100)











