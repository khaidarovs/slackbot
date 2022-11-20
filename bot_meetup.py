from multiprocessing.connection import wait
from dotenv import load_dotenv
import os
import time
import asyncio
import re
from slack import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter

# Load the tokens from the ".env" file, which are set up as environment variables.
# You'll need the signing secret and bot token from the Slack developer console
# for a workspace, which you put in a file you make called ".env". It prevents a
# security risk related to revealing secret keys in public.
load_dotenv()

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> "App Credentials" sections
# of the Slack workspace developer console. By "/slack/events" is the endpoint that you would
# attach to the end of the ngrok link when inputting the request URL in the "Event Subscriptions"
# -> "Enable Events" section of the Slack workspace developer console.
slack_event_adapter = SlackEventAdapter(
    os.environ['SIGNING_SECRET'], "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack workspace developer
# console.
web_client = WebClient(token=os.environ['BOT_TOKEN'])

# Global Storage
# This is an inefficient way to store data, but it is a temporary solution until we are able to
# implement fireBase into our project.
global db 
db = {"reminder": {}}

# Functions we'd implement would be here.
def parsing(self):
    # split the function, so that all the instances of s,m,h,d and any spaces are separated
    # but still kept
    splits = re.split(r"([s|m|h|d| ])", self)
    # remove all of the empty spaces from the newly created array after the split to create
    # the resulting array
    result = [x for x in splits if x != '' and x != ' ']
    return result

def calculation(self,payload,location):
    # initialize accumulator
    i = 0
    # initialize result paramter
    res = 0
    #initialize the different string varaiables
        if location != None:
                var1 = "meetup at " + str(location) + " in "
        else:
                var1 = "meetup in "
    # traverse through the array
    while i < len(self):
        if i + 1 < len(self):
            # if there is still at least one more spot in the array, then there
            # is a possibliity that the next spot in the array is one of the s,m,h,d
            # characters, so check to see if it is any o those characters
            if self[i + 1] == 's':
               var1 = var1 + self[i]
                                if int(self[i]) == 1:
                                        var1 = var1 + " second"
                                else:
                                        var1 = var1 + " seconds"
                                if i + 2 == len(self):
                                        var1 = var1 + "!"
                                else:
                                        var1 = var1 + " and "
                res = res + int(self[i])
                i = i + 2
            elif self[i + 1] == 'm':
                 var1 = var1 + self[i]
                                if int(self[i]) == 1:
                                        var1 = var1 + " minute"
                                else:
                                        var1 = var1 + " minutes"
                                print(i + 2)
                                if i + 2 == len(self):
                                        var1 = var1 + "!"
                                else:
                                        var1 = var1 + " and "
                res = res + (int(self[i]) * 60)
                i = i + 2
            elif self[i + 1] == 'h':
                 var1 = var1 + self[i]
                                if int(self[i]) == 1:
                                        var1 = var1 + " hour"
                                else:
                                        var1 = var1 + " hours"
                                if i + 2 == len(self):
                                        var1 = var1 + "!"
                                else:
                                        var1 = var1 + " and "
                res = res + (int(self[i]) * 3600)
                i = i + 2
            elif self[i + 1] == 'd':
                var1 = var1 + self[i]
                                if int(self[i]) == 1:
                                        var1 = var1 + " day"
                                else:
                                        var1 = var1 + " days"
                                if i + 2 == len(self):
                                        var1 = var1 + "!"
                                else:
                                        var1 = var1 + " and "
                res = res + (int(self[i]) * 86400)
                i = i + 2
            else:
                # if the next spot in the array is none of those characters, then
                # since all of the extra spaces have already been removed, then the
                # next part of the array is another random letter, so remove that letter
                # with split
                tmp = self[i].split('[a-z]')
                # since no s,m,h,d was specificied, default to calculating seconds
                # per minute
                var1 = var1 + tmp[0]
                                if tmp[0] == 1:
                                        var1 = var1 + " minute!"
                                else:
                                        var1 = var1 + " minutes!"
                res = res + (int(tmp[0]) * 60)
                i = i + 1
        else:
            tmp = re.split(r"([a-z])", self[i])
            var1 = var1 + tmp[0]
                        if tmp[0] == 1:
                                var1 = var1 + " minute"
                        else:
                                var1 = var1 + " minutes!"
            res = res + (int(tmp[0]) * 60)
            i = i + 1
    return res

@bot_app.route('/meetup', methods=['POST'])
def meetup(*text):
    step1 = parsing(text[0])
    if len(text) == 3:
        ts = calculation(step1,self[1],self[2])
    else:
        ts = calculation(step1,self[1],None)
    #Waiting on cross-implimentation between core and meetup
    #wait_message(ts + time.time(), desiredchannel, "reminder for meetup")
    return ts

# Sends a message later
def wait_message(ts, channel, remindMessage):
    db["reminder"][ts] = {}
    db["reminder"][ts].update({channel: remindMessage})
    return

# checks if a reminder is in the next five minutes
def in_five(ts):
    found = False
    events = list(db["reminder"].keys())
    # reads each time stamp
    for event in events:
        # is within five minutes
        FIVE_MINUTES = 300
        if (event - time.time() < FIVE_MINUTES):
            found = True
            # reads each channel of that time stamp
            locations = list(db["reminder"][event].keys())
            # iterates through channels for each time stamp
            for location in locations:
                delayedMessage(db["reminder"][event][location],
                               location, event - time.time())
            del db["reminder"][event]
    return found

# sends a message after a delay
async def delayedMessage(message, location, delay):
    await asyncio.sleep(delay)
    sendMessage(message, location)

# sends a message
def sendMessage(message, location):
    web_client.chat_postMessage(channel=location, text=message)

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
