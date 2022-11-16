from dotenv import load_dotenv
import os
# File imports 
import activity_warnings_bot
import mood_messages_bot
import bot_meetup
import onboarding
# Flask import
from flask import Flask, Response, request
# Slack platform related imports
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

# Loads the tokens from the ".env" file, which are set up as environment 
# variables. Done to prevent security risks related to revealing the bot 
# token and signing secret in public. 
# load_dotenv() 

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> 
# "App Credentials" sections of the Slack workspace developer console.
SIGNING_SECRET = "SIGNING_SECRET" # os.environ['SIGNING_SECRET']
# You can find the bot token in the "OAuth & Permissions" section of the Slack 
# workspace developer console.
SLACK_BOT_TOKEN = "SLACK_BOT_TOKEN" # os.environ['SLACK_BOT_TOKEN']
SLACK_SIGNING_SECRET = "SLACK_SIGNING_SECRET" # os.environ['SLACK_SIGNING_SECRET']

web_client = WebClient(token=SLACK_BOT_TOKEN) # Allows communication with Slack

# "/slack/events" is the endpoint that you would attach to the end
# of the ngrok link when inputting the request URL in the "Event Subscriptions" 
# -> "Enable Events" section of the Slack workspace developer console.  
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", bot_app)

test_token = "test_token" # To prevent more function calls then necessary when testing.
bot_id = "bot_id"
# Team and token IDs used to ensure payload information is coming from the correct 
# workspace. 
team_id = "team_id"
token = test_token
try:
    # Retrieving the bot and team ids and token from the correct workspace, being the 
    # workspace specified by the tokens in the .env file. 
    auth_test_payload = web_client.auth_test()
    bot_id = auth_test_payload["bot_id"]
    team_id = auth_test_payload["slack_token"]
    token = auth_test_payload["team_id"]
except:
    pass

"""
Checks if the payload is valid (i.e. has all the fields that we need for processing).
The fields that we need are:
    - token
    - team (workspace) ID
    - channel ID
    - user ID
"""
def check_valid_event_payload(payload, team_id, token):
    print("check_valid_payload is being tested\n")
    if "event" not in payload:
        return False
    event = payload["event"]
    if ("token" not in payload or payload["token"] != token) or ("team_id" not in payload or payload["team_id"] != team_id) or ("type" not in event or event["type"] == "") or ("channel" not in event or event["channel"] == "") or ("user" not in event or event["user"] == ""):
        return False
    return True

"""
Parses the payload and returns a shortened dictionary object with the relevant information.
Fields we need:
    - token
    - user ID
    - channel ID
In case the subtype is irrelevant OR the user ID is the same as the bot ID (handled by bot_message subtype) 
meaning the event was triggered by a bot replying in the chat, return an empty dictionary.
"""
def parse_payload(payload):
    print("parse_payload is being tested\n")
    info = {}
    if ("subtype" in payload["event"]): 
        return info
    else: 
        info["token"] = payload["token"]
        info["user"] = payload["event"]["user"]
        info["channel"] = payload["event"]["channel"]
        info["text"] = payload["event"]["text"]
    return info

# check_id determines if the channel created was made by the bot or 
# not, by comparing ids. Renamed 1st parameter to make it more clear that the 
# channel portion of the Slack POST request payload is being checked. 
def check_id(channel_info, bot_id):
    print("check_id is being tested\n")
    creator_id = channel_info["channel"]["creator"]
    # #general never created by the bot since it's created automatically when 
    # the workspace is created. We want to keep #general channel, so to prevent
    # an attempted archiving, we return true.  
    is_general = channel_info["channel"]["is_general"]
    if creator_id != bot_id and is_general == False:
        return False
    return True

@slack_event_adapter.on('message')
def handle_message_event(payload):
    #Check if the payload is valid
    #If it is, parse the payload and return a useful information dictionary
    payload = request.form.to_dict()
    # Indicator of a potential channel creation event, since a channel_join 
    # message event can occur 
    if "subtype" in payload and payload["subtype"] == "channel_join":
        handle_workspace_channels(payload)
    if (check_valid_event_payload(payload, team_id, token)):
        info_dict = parse_payload(payload)  
        mood_messages_bot.check_mood(info_dict) # call check_send_mood_messages() instead 
        # conversation summarizer function gets called here, with info_dict as parameter
    return Response(status=200)

# Changed handle_workspace_channels from iteration 1 by making the 
# conversations_info api call, to get channel information first.
# That way channel creator information can be retrieved. 
def handle_workspace_channels(payload):
    #check if the person who created the channel is the bot or a person
    #to delete the channel the function should make an API call
    channel_rv = web_client.conversations_info(channel=payload["channel"])
    if not channel_rv["ok"]:
        print(channel_rv["error"]) 
        return Response(status=400) 
    if (check_id(channel_rv, bot_id) == False): 
        #channel creator id doesn't equal bot id 
        #archive the channel
        channel_id = payload["event"]["channel"]["id"]
        #bot joins, https://api.slack.com/methods/conversations.join
        join_rv = web_client.conversations_join(channel=channel_id) 
        if (not join_rv["ok"]):
            print(join_rv["error"])
            return Response(status=400) 
        #bot archives channel, https://api.slack.com/methods/conversations.archive
        archive_rv = web_client.conversations_archive(channel=channel_id) 
        if (not archive_rv["ok"]):
            print(archive_rv["error"])
            return Response(status=400) 
    return Response(status=200)

# Determines if the slash command payload is defective. Created since the slash 
# command payload differs from the event payload. 
def check_valid_slash_command_payload(payload, team_id, token):
    if ("token" not in payload or payload["token"] != token) or ("team_id" not in payload or payload["team_id"] != team_id) or ("channel_id" not in payload or payload["channel_id"] == "") or ("user_id" not in payload or payload["user_id"] == ""):
        return False
    return True

# handle_slash_command is the default function called when a slash command is 
# sent by a user in the workspace. Payload sent by Slack is parsed for 
# determining whether it's defective or not, and if not then the relevant 
# handle function for the command is called. 
@bot_app.route('/slash-command', methods=['POST'])
def handle_slash_command():
    payload = request.form.to_dict()
    if check_valid_slash_command_payload(payload, team_id, token) == False:
        return Response(status=400)
    resp = Response(status=200)
    # payload['command'] will always be valid slash command due to Slack 
    # platform filtering for that. 
    if payload['command'] == "/meetup":
        resp = handle_meetup_invocation(payload)
    elif payload['command'] == "/enable_activity_warnings":
        # if payload["token"] != test_token: # Uncomment the 2 lines after merge
        #    activity_warnings_bot.enable_activity_warnings(payload) 
        pass
    elif payload['command'] == "/disable_activity_warnings":
        resp = handle_disable_activity_warnings_invocation(payload)
    elif payload['command'] == "/set_activity_warning_threshold":
        resp = handle_set_activity_warning_threshold_invocation(payload)
    elif payload['command'] == "/set_activity_warning_content":
        if payload["token"] != test_token:
            activity_warnings_bot.set_activity_warnings_content(payload) 
    elif payload['command'] == "/enable_mood_messages":
        # if payload["token"] != test_token: # Uncomment the 2 lines after merge
        #    mood_messages_bot.enable_mood_messages(payload) 
        pass
    elif payload['command'] == "/disable_mood_messages":
        resp = handle_disable_mood_messages_invocation(payload)
    elif payload['command'] == "/join_class":
        resp = handle_join_class_invocation(payload)
    return resp

# Determines if the parameter to /set_activity_warning_threshold{n_message} 
# is valid.
def handle_set_activity_warning_threshold_invocation(payload):
    params = payload['text']
    invalid_resp = "Sorry! The number of messages can only be a number and greater than 0. Please try again."
    params_split = params.split(" ")
    if len(params) == 0 or len(params_split) > 1 or params_split[0].isnumeric() == False or int(params_split[0]) <= 0:
        return invalid_resp
    # if payload["token"] != test_token: # Uncomment the 2 lines after merge
    #    activity_warnings_bot.set_activity_warnings_threshold(payload)
    return Response(status=200)

# Determines if the parameter to /join_class{class number} is valid. 
def handle_join_class_invocation(payload):
    params = payload['text'].split(" ")
    invalid_resp = "Sorry! I can't recognize your class input. Be sure that it follows the following format: <four letter department name> <5 number course code>"
    if len(params) != 2 or len(params[0]) != 4 or len(params[1]) != 5:
        return invalid_resp
    dept_param = params[0]
    code_param = params[1]
    for i in range(len(dept_param)):
        if dept_param[i].isnumeric():
            return invalid_resp 
    for i in range(len(code_param)):
        if code_param[i].isnumeric() == False:
            return invalid_resp 
    if payload["token"] != test_token:
        onboarding.handle_onboarding(" ".join(params), payload["user_id"])
    return Response(status=200)

# is_time_format_valid checks if the time string contains nonnegative numbers 
# or not. time_format is measured relative to the time a command was invoked, 
# and is used for commands pertaining to scheduling future 
# events/notifications. Note that this function does not actually compute the 
# time, just determines if it is computable. 
def is_time_format_valid(time_format):
    t_len = len(time_format)
    if t_len == 0:
        return False
    has_number = False
    for i in range(t_len):
        if time_format[i] == '-':
            if i + 1 < t_len and time_format[i + 1].isnumeric():
                return False # Existence of negative number in time format.
        if time_format[i].isnumeric():
            has_number = True
    return has_number

# Removed compute_time_format from this file since the other functions have and 
# call an existing implementation that does the same thing, calculating the 
# number of seconds from now that is specified in the given time format. 
# Instead, in this file only checking the validity of the time format is done. 

# handle_meetup_invocation determines if the parameters for the requested 
# /meetup{string time, [optional: location]} command are valid.
def handle_meetup_invocation(payload):
    params = payload['text'].split(", ")
    if len(params) == 1: 
        params = payload['text'].split(",")
    invalid_resp = "Sorry! I couldn't understand the parameters you put for the command. Be sure for the time (1st parameter) you include nonnegative numbers."
    if is_time_format_valid(params[0]) == False:
        return invalid_resp 
    location = ""
    if len(params) > 1:
        location = params[1]
    if payload["token"] != test_token:
        bot_meetup.meetup(params[0], location) 
    return Response(status=200)

# Determines if the parameter to /disable_activity_warnings{string downtime} is 
# valid. 
def handle_disable_activity_warnings_invocation(payload):
    invalid_resp = "Sorry! I couldn't recognize your time format. Please include nonnegative numbers in your input and try again."
    if is_time_format_valid(payload['text']) == False: 
        return invalid_resp
    # if payload["token"] != test_token: # Uncomment the 2 lines after merge
    #   activity_warnings_bot.disable_activity_warnings(payload) 
    return Response(status=200)

# Determines if the parameter to /disable_mood_messages{string downtime} is 
# valid.
def handle_disable_mood_messages_invocation(payload):
    invalid_resp = "Sorry! I couldn't recognize your time format. Please include nonnegative numbers in your input and try again."
    if is_time_format_valid(payload['text']) == False: 
        return invalid_resp
    # if payload["token"] != test_token: # Uncomment the 2 lines after merge
    #    mood_messages_bot.disable_mood_messages(payload) 
    return Response(status=200)

def check_date(end_date):
    #check if today's date is equal to the end_date
    #if it is, return 0, if not return -1, if we're 1 day after the end_date, return 1
    return 0

def archive_channel(): #will be implemented with asyncio, being called periodically (every ~24h)
    end_date = "1/1/1" #date will be pulled from firebase
    if check_date(end_date) == 0:
        #send a poll to the channel asking whether members want to delete the group
        pass
    elif check_date(end_date) == 1:
        #look at the results of the poll
        #if the majority are for, archive the channel
        #otherwise do nothing, keep the channel
        pass
    

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True)
    