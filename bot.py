from dotenv import load_dotenv
import os
from slack import WebClient
from flask import Flask, Response
from slackeventsapi import SlackEventAdapter

# Loads the tokens from the ".env" file, which are set up as environment 
# variables. Done to prevent security risks related to revealing the bot 
# token and signing secret in public. 
#load_dotenv()

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> 
# "App Credentials" sections of the Slack workspace developer console.
# By "/slack/events" is the endpoint that you would attach to the end
# of the ngrok link when inputting the request URL in the "Event Subscriptions" 
# -> "Enable Events" section of the Slack workspace developer console.  
# os.environ['SIGNING_SECRET']
slack_event_adapter = SlackEventAdapter("SIGNING_SECRET", "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack 
# workspace developer console.
# os.environ['BOT_TOKEN']
web_client = WebClient(token="BOT_TOKEN")

# Functions we'd implement would be here.
"""
Checks if the payload is valid (i.e. has all the fields that we need for processing).
"""
def check_valid_payload(payload):
    print("check_valid_payload is being tested\n")
    valid = True
    return valid

"""
Parses the payload and returns a shortened dictionary object with the relevant information.
In case the subtype is irrelevant OR the user ID is the same as the bot ID, 
meaning the event was triggered by a bot replying in the chat, return an empty dictionary.
"""
def parse_payload(payload, bot_id):
    print("parse_payload is being tested\n")
    info = {}
    if (payload.get("user") == bot_id):
        return info
    else:
        info = payload
    return info

def check_id(payload, bot_id):
    print("check_id is being tested\n")
    rv = True
    if (payload.get("channel").get("creator") == bot_id):
        rv = False
    return rv

@slack_event_adapter.on('message')
def handle_message_event(payload):
    #TODO
    #Check if the payload is valid
    #If it is, parse the payload and return a useful information dictionary
    if (check_valid_payload(payload)):
        bot_id = "1"
        info_dict = parse_payload(payload, bot_id)
        #Call the relevant function and pass info_dict as parameter    
    return Response(status=501)

@slack_event_adapter.on('channel_created')
def handle_workspace_channels(payload):
    #check if the person who created the channel is the bot or a person
    #to delete the channel the function should make an API call
    #look at payload["channel"]["creator"]
    #to get the bot id - do an api call
    bot_id = "1"
    if (check_id(payload, bot_id)):
        #do nothing
        pass
    else:
        #delete the channel
        pass


# handle_slash_command is the default function called when a slash command is 
# sent by a user in the workspace. Payload sent by Slack is parsed for 
# determining whether it's defective or not, and if not then the relevant 
# handle function for the command is called. 
# TODO: write function.
@bot_app.route('/slash-command', methods=['POST'])
def handle_slash_command():
    return Response(status=501)

# handle_meetup_invocation determines if the parameters for the requested 
# /meetup{string time, [optional: location]} command are valid.
# TODO: write function.
def handle_meetup_invocation(payload):
    return Response(status=501)

# Determines if the parameter to /set_activity_warning_threshold{n_message} 
# is valid.
# TODO: write function.
def handle_set_activity_warning_threshold_invocation(payload):
    return Response(status=501)

# Determines if the parameter to /set_activity_warning_content{string value} 
# is valid. 
# TODO: write function.
def handle_set_activity_warning_content_invocation(payload):
    return Response(status=501)

# Determines if the parameter to /join_class{class number} is valid. 
# TODO: write function.
def handle_join_class_invocation(payload):
    return Response(status=501)

# is_time_format_valid checks if the time string contains nonnegative numbers 
# or not. time_format is measured relative to the time a command was invoked, 
# and is used for commands pertaining to scheduling future 
# events/notifications. Note that this function does not actually compute the 
# time, just determines if it is computable. 
# TODO: write function.
def is_time_format_valid(time_format):
    return False

# /disable_activity_warnings{string downtime} 
# TODO: write function.
def handle_disable_activity_warnings_invocation(payload):
    return Response(status=501)

# /disable_mood_messages{string downtime} 
# TODO: write function.
def handle_disable_mood_messages_invocation(payload):
    return Response(status=501)

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
    