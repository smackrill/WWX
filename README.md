# WWX
WWX is a discord bot that will collects a data set and updates the data set automatically.  The data collected is the number of images uploaded by a user in a given channel.

The Bot has two commands programmed into it:
  ,popcount "@user" <- Initial database population on target user.  This searches the message history for the past X days, default is 90 on specified channel ID's.
  ,count "@user" <- This command will make the bot send a message in the channel with the current number of images cataloged in the database file for a user.

How to set up:
  git clone https://github.com/smackrill/WWX  (Hopefully I got this working!!)
  cd WWX\ 
  sudo chmod +rwx Messagecounter.py

You will want to edit the python file with your channel ID's and the amount of days you want popcount to search back, as well as your bot token.

If you are running your bot on an ubuntu box like I do (I have a raspberry pi running this) You can set your bot to run 24/7 and restart automatically with the following:

EDIT THIS IN LATER
