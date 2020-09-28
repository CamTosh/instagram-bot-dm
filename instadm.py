from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from random import randint, uniform
from time import sleep
import logging
import sqlite3

DEFAULT_IMPLICIT_WAIT = 30


class InstaDM(object):
    
    def __init__(self, username, password, headless=True, instapy_workspace=None, profileDir=None):
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
        
        if profileDir:
            options.add_argument("user-data-dir=profiles/" + profileDir) 

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
        if self.instapy_workspace is not None:
            self.conn = sqlite3.connect(self.instapy_workspace + "InstaPy/db/instapy.db")
            self.cursor = self.conn.cursor()

            cursor = self.conn.execute("""
                SELECT count(*)
                FROM sqlite_master
                WHERE type='table'
                AND name='message';
            """)
            count = cursor.fetchone()[0]

            if count == 0:
                self.conn.execute("""
                    CREATE TABLE "message" (
                        "username"    TEXT NOT NULL UNIQUE,
                        "message"    TEXT DEFAULT NULL,
                        "sent_message_at"    TIMESTAMP
                    );
                """)

        try:
            self.login(username, password)
        except Exception as e:
            logging.error(e)

    def login(self, username, password):
        # homepage
        self.driver.get('https://instagram.com')
        self.__random_sleep__(3, 5)
        self.driver.find_elements_by_css_selector(self.selectors['home_to_login_button'])[0].click()
        self.__random_sleep__(2, 4)
        
        # login
        logging.info('Login with {}'.format(username))
        self.__scrolldown__()
        self.driver.find_element_by_name(self.selectors['username_field']).send_keys(username)
        self.driver.find_element_by_name(self.selectors['password_field']).send_keys(password)
        self.driver.find_elements_by_css_selector(self.selectors['button_login'])[2].click()
        self.__random_sleep__()

    def sendMessage(self, user, message):
        logging.info('Send message {} to {}'.format(message, user))
        self.driver.get('https://www.instagram.com/direct/new/')
        self.__random_sleep__(5, 7)

        self.__wait_for_element__(self.selectors['search_user'], "name")
        self.__type_slow__(self.selectors['search_user'], "name", user)
        self.__random_sleep__()

        # Select user
        elements = self.driver.find_elements_by_css_selector(self.selectors['select_user'])
        elements[2].click()
        self.__random_sleep__()
        
        # Go to page
        elements[0].click()
        self.__random_sleep__()
        self.__wait_for_element__("*//textarea", "xpath")
        self.__type_slow__("(*//textarea)[1]", "xpath", message)
        self.__random_sleep__()

        buttons = self.driver.find_elements_by_css_selector(self.selectors['send'])
        buttons[len(buttons)-1].click()

        if self.conn is not None:
            self.cursor.execute('INSERT INTO message (username, message) VALUES(?, ?)', (user, message))
            self.conn.commit()

        self.__random_sleep__()

    def sendGroupMessage(self, users, message):
        logging.info(f'Send group message {message} to {users}')
        self.driver.get('https://www.instagram.com/direct/new/')
        self.__random_sleep__(5, 7)

        usersAndMessages = []
        for user in users:
            if self.conn is not None:
                usersAndMessages.append((user, message))

            self.__wait_for_element__(self.selectors['search_user'], "name")
            self.__type_slow__(self.selectors['search_user'], "name", user)
            self.__random_sleep__()

            # Select user
            elements = self.driver.find_elements_by_css_selector(self.selectors['select_user'])
            elements[2].click()
            self.__random_sleep__(2, 4)

        # Go to page
        elements[0].click()
        self.__random_sleep__()
        self.__wait_for_element__("*//textarea", "xpath")
        self.__type_slow__("(*//textarea)[1]", "xpath", message)
        self.__random_sleep__()
        buttons = self.driver.find_elements_by_css_selector(self.selectors['send'])
        buttons[len(buttons)-1].click()

        if self.conn is not None:
            self.cursor.executemany("""
                INSERT OR IGNORE INTO message (username, message) VALUES(?, ?)
            """, usersAndMessages)
            self.conn.commit()

        self.__random_sleep__()

    def __get_element__(self, element_tag, locator):
        """Wait for element and then return when it is available"""
        try:
            locator = locator.upper()
            dr = self.driver
            if locator == 'ID' and self.is_element_present(By.ID, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_id(element_tag))
            elif locator == 'NAME' and self.is_element_present(By.NAME, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_name(element_tag))
            elif locator == 'XPATH' and self.is_element_present(By.XPATH, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_xpath(element_tag))
            elif locator == 'CSS' and self.is_element_present(By.CSS_SELECTOR, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_css_selector(element_tag))
            else:
                logging.info(f"Error: Incorrect locator = {locator}")
        except Exception as e:
            logging.error(e)
        logging.info(f"Element not found with {locator} : {element_tag}")
        return None

    def is_element_present(self, how, what):
        """Check if an element is present"""
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def __wait_for_element__(self, element_tag, locator, timeout=30):
        """Wait till element present. Max 30 seconds"""
        result = False
        self.driver.implicitly_wait(0)
        locator = locator.upper()
        for i in range(timeout):
            try:
                if locator == 'ID' and self.is_element_present(By.ID, element_tag):
                    result = True
                    break
                elif locator == 'NAME' and self.is_element_present(By.NAME, element_tag):
                    result = True
                    break
                elif locator == 'XPATH' and self.is_element_present(By.XPATH, element_tag):
                    result = True
                    break
                elif locator == 'CSS' and self.is_element_present(By.CSS_SELECTORS, element_tag):
                    result = True
                    break
                else:
                    logging.info(f"Error: Incorrect locator = {locator}")
                    break
            except Exception as e:
                logging.error(e)
                print(f"Exception when __wait_for_element__ : {e}")
                pass
            sleep(0.99)
        else:
            print(f"Timed out. Element not found with {locator} : {element_tag}")
        self.driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
        return result

    def __type_slow__(self, element_tag, locator, input_text=''):
        """Type the given input text"""
        try:
            self.__wait_for_element__(element_tag, locator, 5)
            element = self.__get_element__(element_tag, locator)
            actions = ActionChains(self.driver)
            actions.click(element).perform()
            for s in input_text:
                element.send_keys(s)
                sleep(uniform(0.1, 0.2))

        except Exception as e:
            logging.error(e)
            print(f'Exception when __typeSlow__ : {e}')

    def __random_sleep__(self, minimum=10, maximum=20):
        t = randint(minimum, maximum)
        logging.info(f'Wait {t} seconds')
        sleep(t)

    def __scrolldown__(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


