# Tech-Talk-Bot

Tech-Talk-Bot is a bot for GroupMe running on the Heroku application enviroment. Given a authenticate GroupMe bot_id, this bot parses through the messages of the group and responds to users when called with "!bot". It can respond to a few simple commands:
- "weather: given a zip code, it gives the current weather with tempature highs and lows for the day in fahrenheit
- "heroku status": lets the user know if the bot is working
- "scoreboard": shows the top 5 most liked posts of the last week
- "remind": shows the meeting time for the group

If any commands are given outside of these, it lets the user know the command was not recognized.
