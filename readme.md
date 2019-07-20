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

## Dashboard

InstaDM works with an [modified version of InstaPy Dashboard](https://github.com/CamTosh/instapy-dashboard). 

> [InstaPy Dashboard](https://github.com/converge/instapy-dashboard) is an Open Source project developed by @converge to visualize Instagram accounts progress and real-time InstaPy logs on the browser. 





<a href="https://www.paypal.me/camtosh">
  <img hspace="0" alt="paypalme" src="http://codeinpython.com/tutorials/wp-content/uploads/2017/09/PayPal-ME-300x300.jpg.png" width=100 />
Buy me a 🍺 
