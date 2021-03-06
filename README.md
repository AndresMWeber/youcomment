<h1 align="center">
  <a href="http://www.reddit.com/u/youtube_comment_bot">YouComment</a>
</h1>
<h3 align="center">
    A bot for comparing top-level youtube comments and reddit comments for a reddit post that centers around a youtube link.
</h3>

[![CircleCI](https://img.shields.io/circleci/project/github/AndresMWeber/youcomment.svg?style=flat-square)](https://circleci.com/gh/AndresMWeber/youcomment)
[![Codacy Badge Coverage](https://img.shields.io/codacy/coverage/1bbac98237544bc49d40ea95ee5e8ffc.svg?style=flat-square)](https://www.codacy.com/app/AndresMWeber/youcomment?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndresMWeber/youcomment&amp;utm_campaign=Badge_Grade)
[![Codacy Badge Grade](https://img.shields.io/codacy/grade/1bbac98237544bc49d40ea95ee5e8ffc.svg?style=flat-square)](https://www.codacy.com/app/AndresMWeber/youcomment?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=AndresMWeber/youcomment&amp;utm_campaign=Badge_Grade)
[![Python Version](https://img.shields.io/badge/python-2.7%20%7C%203.5%20%7C%203.6-blue.svg?style=flat-square)](https://www.python.org/)
[![Heroku App Status](https://heroku-badge.herokuapp.com/?app=youcomment&style=flat)](https://youcomment.herokuapp.com)

[![Github Latest Release](https://flat.badgen.net/github/release/andresmweber/youcomment)](https://github.com/AndresMWeber/youcomment/releases)
[![Github Last Commit](https://flat.badgen.net/github/last-commit/andresmweber/youcomment)](https://github.com/AndresMWeber/youcomment/commits/master)
[![Github Issues](https://flat.badgen.net/github/open-issues/andresmweber/youcomment)](https://github.com/andresmweber/youcomment/issues)
[![Github License](https://flat.badgen.net/github/license/andresmweber/youcomment)](https://github.com/AndresMWeber/youcomment/blob/master/LICENSE.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

# Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Developing](#developing)
   *   [Python/Git set up ](#python-and-git-set-up)
4. [Configuration](#configuration)
   *   [Set up API Access __(CRUCIAL)__](#set-up-api-access)
5. [Meet the Bot](#meet-the-bot)
6. [Contributing](#contributing)
7. [File Descriptions](#file-descriptions)
8. [Changelog](#version-history)
9. [License](#license)

### Installation
#### Python and Git set up 

1) Clone the Repository:

`git clone` <https://github.com/AndresMWeber/youcomment.git>

2) Create a virtual environment for the bot to run in

`python3 -m venv venv --no-site-packages`

3) Activate the virtual env

`source venv/bin/activate`

4) Install requirements

`pip install -r requirements.txt`

### Configuration
#### Set up API Access
*   Create a [Reddit App](http://reddit.com/prefs/apps) as script
*   Obtain a [Youtube API Key](https://console.developers.google.com/apis/credentials): [(tutorial)](https://developers.google.com/youtube/registering_an_application#Create_API_Keys)
*   Set the following environment variables on | [mac](https://stackoverflow.com/questions/7501678/set-environment-variables-on-mac-os-x-lion) | [windows](https://superuser.com/questions/1334129/setting-an-environment-variable-in-windows-10-gpodder) | [linux](https://stackoverflow.com/questions/45502996/how-to-set-environment-variable-in-linux-permanently) |:

| Key                       | Description                                     |
| :--                       | -----------                                     |
| `YC_REDDIT_CLIENT_ID`     | The generated field under "personal use script" |
| `YC_REDDIT_CLIENT_SECRET` | The generated Secret field.                     |
| `YC_REDDIT_USER`          | The username to your reddit bot.                |
| `YC_REDDIT_PASS`          | The password to your reddit bot.                |
| `YC_YOUTUBE_API_KEY`      | The API Key you generated for Youtube.          |

*   __WARNING:__ without these environment variables set, the program will not function.

### Usage

You have the option of running the bot in a few different ways:

__Python__

```python
from youcomment.bot import YouCompareBot
bot = YouCompareBot()
bot.run()
```

```python
import youcomment.bot
```

__CLI__

```shell
$ youcomment
```

### Developing

You can run tests using a couple options while within the top git repo folder:
*   `python setup.py test`
*   `python -m unittest discover`

### Meet the Bot

My current test subreddit it is active in is here:

<https://reddit.com/r/you_comment_bot>

Feel free to make a new post if you want to test the bot

### Contributing

*   If you want to help please feel free to do it.
*   If you need help please fell free to ask me.
*   If you find any bug or exploit please tell me: I will try to fix them or if you want you can fix them and I will include your changes in the project.
*   If you find a way to improve the bot, please share it with everybody.

### File Descriptions
---

| File                                | Description                                                  |
| :---                                | :----------                                                  |
| `youcomment/`                       | A module for comparing reddit and youtube top-level comments |
| `youcomment/bot.py`                 | The actual bot                                               |
| `youcomment/reddit.py`              | The handler for all reddit api commands                      |
| `youcomment/youtube.py`             | The handler for all youtube api commands                     |
| `youcomment/database.py`            | The database manager file                                    |
| `youcomment/config.py`              | The configuration file                                       |
| `youcomment/version.py`             | Contains only the project version number                     |
| `youcomment/data/template.md` | The message template                                         |
| `tests/`                            | Tests                                                        |
| `.circleci/config.yml`              | CircleCI configuration file                                  |

### Version History
[__Changelog__](CHANGELOG.md)

### License
[__MIT License__](LICENSE.md)

