# Otaku

`Otaku` is an open source Discord Music Bot.

![Otaku GIF Demo](img/Otaku.png)

Contents
========

 * [Why?](#why)
 * [Invite Link](#invite-link)
 * [Installation](#installation)
 * [Usage](#usage)
 * [Configuration](#configuration)
 * [Currently Working On](#working-on)
 * [Want to Contribute?](#want-to-contribute)

### Why

I wanted to make a Discord Music Bot just like groovy and Rythm which is open to world for contributions.

+ Plays from search keyword
+ Plays from link
+ Supports many sites: https://ytdl-org.github.io/youtube-dl/supportedsites.html
+ Has extra categories other than Music like FUN, UTILITIES, etc.

And is the first discord bot which I am maintaining.

### Invite Link

[![Invite Link](https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://apsweb.design/)

### Installation
---

Instead of hosting your own I recommend **inviting the Otaku bot to your server**

**If you still want to host it then**

**Make a bot on discord developers portal and give the bot Admin Access**

**Copy the _TOKEN_ of your bot**(Pss. Its secret. Don't ever share it even with your close friends.)

**Heroku**

<img src="https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white" /> | `https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white`

**Installing on VPS**

1. Clone the repository to your Local Machine
    + `$ git clone https://github.com/AmreshSinha/Otaku`
    + `$ cd Otaku`
2. Install all the requirements given in `requirements.txt`:
    + `$ pip install -r requirements.txt`
3. Install ffmpeg
    + `$ sudo apt update`
    + `$ sudo apt install ffmpeg`
5. Make a `.env` file in the same directory. (Yes exactly .env)
    + `$ sudo nano .env`
    + And paste your Discord Bot Token in it like
    + `TOKEN = "YOUR-DISCORD-BOT-TOKEN"` (Yes "" included)
6. Ensure you have python 3.8 or above
7. Now its time to run it
    + `$ python3 main.py`
8. If you accidentally close the Terminal then the bot will go down and you will have to repeat Step-7
9. To Avoid this you can use `Screen`. Google it for usage.

I Still advise you to use the already hosted bot instead. Here's the [Invite Link](#invite-link).

### Usage

These are the Currently Usable Commands

Music:
    + `!join`   Joins a voice channel
    + `!link`   Plays from a URL (Supported: https://bit.ly/3yYrdbc)
    + `!play`   Plays by Search
    + `!queue`  Adds Song in Queue
    + `!stop`   Stops and disconnects the bot from voice
    + `!stream` Streams from a url (same as yt, but doesn't predownload)
    + `!volume` Changes the player's volume
    
Random:
    + `!choose` Helps Selecting Between Words Randomly
    + `!random` Generates a Random Number between Input Number 1 and Input Number 2
    
### Configuration

+ `.env` file for Discord Bot Token
+ No Other Configurations.

### Currently Working On

1. Queue Feature
2. More Utility Features
3. Fun Features
4. Pause Feature
5. etc

### Want to Contribute?
---

You can add your feature in your fork and make a Pull Request, I will check it out :)
