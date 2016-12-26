# AphroditeBot
A simple bot that has most of the functionality of SS13's Game -> IRC functionality, except for a Discord server instead.

#Installation

1. First you need to make yourself a Discord bot, and add it to your server. There's plenty of tutorials for doing such online, so I won't go into detail here.
2. You need to replace the file ~/scripts/ircbot_message.py in your SS13 director with the file included in Byond Files.
3. Edit the config.py file appropriately. Keep in mind the quotations and do not delete them. To get your channel IDs, enable Developer mode in Discord, and right click-> Copy ID
4. Gameport is the port that you connect to to play the actual game.
5. triggerString is the sting that the bot listens for
6. Once config.py is set up properly, just run "AphroditeBot.py" and wait for "Bot is ready."

Note: This bot was originally developed to be run on the same machine that your SS13 server runs on. It may work for running on a different machine but I cannot be entirely sure.
