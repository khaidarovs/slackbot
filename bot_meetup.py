from multiprocessing.connection import wait
from dotenv import load_dotenv
import os
import time
import math
import asyncio
import re
from slack import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter
import firebase_admin
from firebase_admin import credentials, db

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

# Functions we'd implement would be here.
def parsing(self):
    # split the function, so that all the instances of s,m,h,d and any spaces are separated
    # but still kept
    splits = re.split(r"([s|m|h|d| ])", self)
    # remove all of the empty spaces from the newly created array after the split to create
    # the resulting array
    result = [x for x in splits if x != '' and x != ' ']
    return result


def calculation(self, payload, location):
    # added 2 more paramters, the payload, so that the payload can be updated
    # with the message that will be created, and the location that can be added to the
    # message if a location is given.
    # initialize accumulator
    i = 0
    # initialize result paramter
    res = 0
    # initialize thestring varaiable
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
                # decide whether the number is 1, and if so, do not put an s at the end of
                # the unit
                if int(self[i]) == 1:
                    var1 = var1 + " second"
                else:
                    var1 = var1 + " seconds"
                if i + 2 >= len(self):
                    # if this is the last sequence of numbers in the array, then add an exclamation
                    # point to end the sentence, otherwise 'and' is added.
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
                # if no s,m,h,d are used, add 'minutes' to the string variable
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
    # update the message of the payload paramter of this function to reflect
    # the time input
    payload["type"] = str(var1)
    # also change the ts of the payload to the result
    payload["ts"] = res
    return res


@bot_app.route('/meetup', methods=['POST'])
def meetup(*text):
    step1 = parsing(text[0])
    # check to see if there is a location paramter entered into the function
    if len(text) == 3:
        # if so include the lcoation in the calcuation portion
        ts = calculation(step1, text[1], text[2])
    else:
        ts = calculation(step1, text[1], None)
    return ts

# Sends a message later
def wait_message(payload, meetremind):
    # adds the new data of the the timestamp to new database
    data = {payload.get('channel'): meetremind}
    res = timestamps.child(str(math.trunc(payload.get('ts'))))
    res.set(data)

# checks if a reminder is in the next five minutes
def in_five(payload):
    # changed the paramter from timestamp to payload, because it can take the newly updated payload's
    # timestamp to check if it is within 5 minutes of the current time.
    ts = int(payload.get('ts'))
    res = timestamps.child(str(ts))
    if res.get() == {payload.get('channel'): "reminder for meetup"}:
        # determines whether a specified timestamp of the payload is within 5 min of current time
        if ts <= time.time() + 300:
            return True
        else:
            return False
    else:
        return False

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
