from dotenv import load_dotenv
import json
import os
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
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'], "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack workspace developer 
# console.
web_client = WebClient(token=os.environ['BOT_TOKEN'])

# Functions we'd implement would be here.
def parsing(self):
        #split the function, so that all the instances of s,m,h,d and any spaces are separated
        #but still kept
        splits = re.split(r"([s|m|h|d| ])",self)
        #remove all of the empty spaces from the newly created array after the split to create
        #the resulting array
        result = [x for x in splits if x != '' and x != ' ']
        return result

def calculation(self):
        #initialize accumulator
        i = 0
        #initialize result paramter
        res = 0
        #traverse through the array
        while i < len(self):
                if i + 1 < len(self):
                        #if there is still at least one more spot in the array, then there
                        #is a possibliity that the next spot in the array is one of the s,m,h,d
                        #characters, so check to see if it is any o those characters
                        if self[i + 1] == 's':
                                res = res + int(self[i])
                                 i = i + 2
                        elif self[i + 1] == 'm':
                                res = res + (int(self[i]) * 60)
                                i = i + 2
                        elif self[i + 1] == 'h':
                                res = res + (int(self[i]) * 3600)
                                i = i + 2
                        elif self[i + 1] == 'd':
                                res = res + (int(self[i]) * 86400)
                                i = i + 2
                        else:
                                #if the next spot in the array is none of those characters, then
                                #since all of the extra spaces have already been removed, then the
                                #next part of the array is another random letter, so remove that letter
                                #with split
                                 tmp = self[i].split('[a-z]')
                                #since no s,m,h,d was specificied, default to calculating seconds
                                #per minute
                                res = res + (int(tmp[0]) * 60)
                                i = i + 1
                else:
                        tmp = re.split(r"([a-z])",self[i])
                        res = res + (int(tmp[0]) * 60)
                        i = i + 1

        return res

@bot_app.route('/meetup',methods = ['POST'])
def meetup(self):
        step1 = parsing(self)
        step2 = calculation(step1)
        return step2


def wait_message(ts,channel,meetremind):
        data = {channel : meetremind}
        db.reminder[ts] = data
def in_five(ts):
        return db.reminder[ts] != NULL
                                

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
    
