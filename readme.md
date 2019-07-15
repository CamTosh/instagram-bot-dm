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

## Work's with InstaPY

Use `instapy_workspace` param on constructor: 

```python
from instadm import InstaDM

if __name__ == '__main__':
	# Auto login
	insta = InstaDM(
		username='your_username',
		password='your_password',
		headless=False,
		instapy_workspace='workspace/'
	)
```

InstaDM create table `followers` if not exists.
```sql
CREATE TABLE "followers" (
	"username"	TEXT NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"detected_at"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"message"	TEXT DEFAULT NULL,
	"sent_message_at"	TIMESTAMP
);
```

Buy me a 🍺 : [Paypal](https://www.paypal.me/camtosh/7)