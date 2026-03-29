## Open-source
We're making it open-source in order to keep the bot alive, since I haven't found much time to update it. Feel free to contribute with your own changes, I'd be happy to review them.

In order to make it open-source I also had to delete the html files that broke github's policy, you can get your own visiting any site with a lot of <a> tags with the content you want to search through and put it into a new folder called "games_html"

## Config
The bot needs a config.json with your own api keys for offline testing, it should be like that:
```
{
	"TOKEN": "",
	"API_KEY": "",
	"CSE_GAMES_ID": "00d83e25ab9eb4085",
	"CSE_BOOKS_ID": "96b1bfe3793b44922",
	"VIRUSTOTAL_API_KEY": "",
  "STEAM_WEB_API_KEY": "not needed anymore", 
	"FFMPEG_LOCATION": "ffmpeg-7.0.2/ffmpeg"
} 
```
The "API_KEY" in question is your Google console api key only needed for games online searches, the cse IDS are already preset, you can change to your own or just use mines.
