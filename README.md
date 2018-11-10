## [YouComment](http://www.reddit.com/u/youtube_comment_bot)
[![CircleCI](https://circleci.com/gh/AndresMWeber/youcomment.svg?style=svg)](https://circleci.com/gh/AndresMWeber/youcomment)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1bbac98237544bc49d40ea95ee5e8ffc)](https://www.codacy.com/app/AndresMWeber/youcomment?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndresMWeber/youcomment&amp;utm_campaign=Badge_Grade)

A bot for comparing top-level youtube comments and reddit comments for a reddit post that centers around a youtube link.


### Where to look

* `youcomment/youcomment.py`, the actual bot
* `youcomment/reddit.py`, the handler for all reddit api commands
* `youcomment/youtube.py`, the handler for all youtube api commands
* `youcomment/config.py`, the configuration file
* `youcomment/post_template.txt`, the template message
* `youcomment/`, a module for comparing reddit and youtube top-level comments
* `tests/`, tests
* `.circleci/`, CircleCI configuration file

### How to install
##### Install codebase/set up python
* `git clone` https://github.com/AndresMWeber/youcomment.git
* `python3 -m venv venv --no-site-packages`
	* this will create a virtual environment for the bot to run in
* `source venv/bin/activate`
	* activate the bot
* `pip install -r requirements.txt`
	* install requirements

##### Set up API Access (*CRUCIAL*)
* Create a [Reddit App](http://reddit.com/prefs/apps) as script
* Obtain a [Youtube API Key](https://console.developers.google.com/apis/credentials): [(tutorial)](https://developers.google.com/youtube/registering_an_application#Create_API_Keys)
* Set the following environment variables on | [mac](https://stackoverflow.com/questions/7501678/set-environment-variables-on-mac-os-x-lion) | [windows](https://superuser.com/questions/1334129/setting-an-environment-variable-in-windows-10-gpodder) | [linux](https://stackoverflow.com/questions/45502996/how-to-set-environment-variable-in-linux-permanently) |: 
    * `YC_REDDIT_CLIENT_ID` - The generated field under "personal use script"
    * `YC_REDDIT_CLIENT_SECRET` - The generated Secret field.
    * `YC_REDDIT_USER` - The username to your reddit bot.
    * `YC_REDDIT_PASS` - The password to your reddit bot.
    * `YC_YOUTUBE_API_KEY` - The API Key you generated for Youtube.
    - **WARNING:** without these environment variables set, the program will not function.   

### Developing
You can run tests using a couple options while within the top git repo folder:
* `python setup.py test`
* `python -m unittest discover`

### Info / Reddit-related questions / See the bot in action

https://reddit.com/r/test123456123456

Feel free to make a new post if you want to test the bot

### Want to help or want help?

* If you want to help please feel free to do it.
* If you need help please fell free to ask me.
* If you find any bug or exploit please tell me: I will try to fix them or if you want you can fix them and I will include your changes in the project.
* If you find a way to improve the bot, please share it with everybody.

### LICENSE

**MIT License**
