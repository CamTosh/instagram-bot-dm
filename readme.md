# Instagram Direct Message Bot

Send direct and group message with Instagram bot. Work with Python 3.7.2 and Selenium.

## Example : 

```python
from instadm import InstaDM

if __name__ == '__main__':
	# Auto login
	insta = InstaDM(username='your_username', password='your_password', headless=False)
	
	# Send message
	insta.sendMessage(user='username_target', message='Hey !')
	
	# Send message
	insta.sendGroupMessage(users=['user1', 'user2'], message='Hey !')
```


Buy me a 🍺 : [Paypal](https://www.paypal.me/camtosh/7)