from dotenv import load_dotenv
import os
# File imports 
import activity_warnings_bot
import convo_summary_bot
import mood_messages_bot
import bot_meetup
import onboarding
# Flask import
from flask import Flask, Response, request
# Slack platform related imports
from slack_sdk import WebClient
from slackeventsapi import SlackEventAdapter
# Time related imports
from datetime import date, datetime, timedelta
from twisted.internet import reactor, task
from multiprocessing import Process
import pytz
# Firebase related imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# For live testing demo purposes
check_channel_test = False # set to True for live testing check_channel
'''
For testing the voting to archive process:
with vote_test true, you can run /trigger_voting and /trigger_activity_warning. 
Note for /trigger_voting, make sure that you create a channel that has an end 
date at today's date.
'''
vote_test = True # set to true for live testing voting for archive
vote_results_test = True # set to true for live testing voting results

global_curr_time_voting = datetime.now(pytz.timezone('US/Central'))

# Loads the tokens from the ".env" file, which are set up as environment 
# variables. Done to prevent security risks related to revealing the bot 
# token and signing secret in public. 
load_dotenv() 

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> 
# "App Credentials" sections of the Slack workspace developer console.
SIGNING_SECRET = os.environ['SIGNING_SECRET']
# You can find the bot token in the "OAuth & Permissions" section of the Slack 
# workspace developer console.
SLACK_BOT_TOKEN = os.environ['BOT_TOKEN']

web_client = WebClient(token=SLACK_BOT_TOKEN) # Allows communication with Slack

# "/slack/events" is the endpoint that you would attach to the end
# of the ngrok link when inputting the request URL in the "Event Subscriptions" 
# -> "Enable Events" section of the Slack workspace developer console.  
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", bot_app)

test_token = "test_token" # To prevent more function calls then necessary when testing.
bot_id = "bot_id"
# Team and token IDs used to ensure payload information is coming from the correct 
# workspace. 
test_team_id = "team_id" # Used in other files
actual_team_id = test_team_id
actual_bot_user_id = ""
try:
    # Retrieving the bot and team ids and token from the correct workspace, being the 
    # workspace specified by the tokens in the .env file. 
    auth_test_payload = web_client.auth_test()
    bot_id = auth_test_payload["bot_id"]
    actual_team_id = auth_test_payload["team_id"]
    actual_bot_user_id = auth_test_payload["user_id"]
except:
    pass

'''
Firebase related initializers
Note: need to put the JSON file in the same directory as this file
'''
# Fetch the service account key JSON file contents
directory = os.getcwd()
cred = credentials.Certificate(directory + '/slackbot-software-firebase-adminsdk-xxfr0-f706556aac.json')#'/slackbot-software-firebase-adminsdk-xxfr0-f706556aac.json')

votes_app = None
if 'slackbot-software-default-rtdb' not in firebase_admin._apps:
    # Initialize the app with a service account, granting admin privileges
    votes_app = firebase_admin.initialize_app(cred, options={
        'databaseURL': 'https://slackbot-software-default-rtdb.firebaseio.com/'}, 
        name='slackbot-software-default-rtdb'
    )
else:
    votes_app = firebase_admin.get_app(name='slackbot-software-default-rtdb')

ref = db.reference('channels', app=votes_app)

"""
Checks if the payload is valid (i.e. has all the fields that we need for processing).
The fields that we need are:
    - team (workspace) ID
    - channel ID
    - user ID
"""
def check_valid_event_payload(payload, team_id):
    print("check_valid_payload is being tested\n")
    if "event" not in payload:
        return False
    event = payload["event"]
    if ("token" not in payload or payload["token"] == "") or ("team_id" not in payload or payload["team_id"] != team_id) or ("type" not in event or event["type"] == "") or ("channel" not in event or event["channel"] == "") or ("user" not in event or event["user"] == ""):
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
        info["channel_id"] = payload["event"]["channel"]
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
    if (check_valid_event_payload(payload, actual_team_id)) == False:
        return Response(status=400)
    # Indicator of a potential channel creation event, since a channel_join 
    # message event can occur 
    if "subtype" in payload["event"] and payload["event"]["subtype"] == "channel_join" and payload["event"]["user"] != bot_id:
        handle_workspace_channels(payload) 
        onboarding.welcome_new_user(payload)
    info_dict = parse_payload(payload) 
    if "text" in info_dict and actual_bot_user_id != payload["event"]["user"]:
        mood_messages_bot.check_send_mood_message(info_dict, {"text": info_dict["text"]})
    return Response(status=200)

# Changed handle_workspace_channels from iteration 1 by making the 
# conversations_info api call, to get channel information first.
# That way channel creator information can be retrieved. 
# We intend to air on the side of caution in trying to archive channels,
# with archiving only being done on public channels. Archiving private 
# channels that the bot is not a part of is impossible at the moment.
def handle_workspace_channels(payload):
    try: 
        #check if the person who created the channel is the bot or a person
        #to delete the channel the function should make an API call
        channel_rv = web_client.conversations_info(channel=payload["event"]["channel"])
        if not channel_rv["ok"]:
            print(channel_rv["error"]) 
            return Response(status=400) 
        if (check_id(channel_rv, actual_bot_user_id) == False):
            #channel creator id doesn't equal bot id 
            #archive the channel
            channel_id = payload["event"]["channel"]
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
    except:
        Response(status=200) # can't archive private channel that the bot is not in 
    return Response(status=200)

# Determines if the slash command payload is defective. Created since the slash 
# command payload differs from the event payload. 
def check_valid_slash_command_payload(payload, team_id):
    if ("token" not in payload or payload["token"] == "") or ("team_id" not in payload or payload["team_id"] != team_id) or ("channel_id" not in payload or payload["channel_id"] == "") or ("user_id" not in payload or payload["user_id"] == ""):
        return False
    return True

# handle_slash_command is the default function called when a slash command is 
# sent by a user in the workspace. Payload sent by Slack is parsed for 
# determining whether it's defective or not, and if not then the relevant 
# handle function for the command is called. 
@bot_app.route('/slash-command', methods=['POST'])
def handle_slash_command():
    global vote_test
    global vote_results_test
    payload = request.form.to_dict()
    if check_valid_slash_command_payload(payload, actual_team_id) == False:
        return Response(status=400)
    try:
        rv = web_client.conversations_members(channel=payload["channel_id"])
        found = False
        for id in rv["members"]:
            if actual_bot_user_id == id:
                found = True
        if not found:
            return "StudyRoom Bot needs to be added to the channel first. Type @ and then click the bot to get Slackbot to invite it."
    except Exception as e:
        return "StudyRoom Bot needs to be added to the channel first. Type @ and then click the bot to get Slackbot to invite it."
    resp = Response(status=200)
    # payload['command'] will always be valid slash command due to Slack 
    # platform filtering for that. 
    if payload['command'] == "/meetup":
        resp = handle_meetup_invocation(payload)
    elif payload['command'] == "/enable_activity_warnings":
        if payload["token"] != test_token: 
            activity_warnings_bot.enable_activity_warnings(payload) 
    elif payload['command'] == "/disable_activity_warnings":
        resp = handle_disable_activity_warnings_invocation(payload)
    elif payload['command'] == "/set_activity_warning_threshold":
        resp = handle_set_activity_warning_threshold_invocation(payload)
    elif payload['command'] == "/set_activity_warning_content":
        if payload["token"] != test_token:
            activity_warnings_bot.set_activity_warnings_content(payload) 
    elif payload['command'] == "/set_mood_message_content":
        if payload["token"] != test_token:
            mood_messages_bot.set_mood_messages_content(payload) 
    elif payload['command'] == "/enable_mood_messages":
        if payload["token"] != test_token: 
            mood_messages_bot.enable_mood_messages(payload) 
    elif payload['command'] == "/disable_mood_messages":
        resp = handle_disable_mood_messages_invocation(payload)
    elif payload['command'] == "/join_class":
        resp = handle_join_class_invocation(payload)
    elif payload["command"] == "/vote_archive":
        resp = handle_vote(payload)
    elif payload["command"] == "/summarize_conversation":
        if payload["token"] != test_token: 
            # Call conversation summarizer function 
            convo_summary_bot.summarize_conversation(payload)
    elif payload["command"] == "/help":
        resp = "Visit the README.md in https://github.com/khaidarovs/slackbot for slash command instructions and a general overview of the bot!"
    elif payload["command"] == "/trigger_activity_warning": 
        if payload["token"] != test_token:  
            activity_warnings_bot.check_send_activity_warning({"token": payload["token"], "channel_id": payload["channel_id"]})
    elif payload["command"] == "/trigger_voting":
        vote_results_test = False
        vote_test = True
        if payload["token"] != test_token:
            archive_channel(payload["channel_id"])
    elif payload["command"] == "/trigger_check_vote_results":
        vote_test = False
        vote_results_test = True
        if payload["token"] != test_token:
            archive_channel(payload["channel_id"])
    return resp

# handle_vote keeps track of voting for deciding whether to archive the channel or not. 
def handle_vote(payload):
    choice = payload["text"].strip()
    if choice != "Y" and choice != "N":
        return "Vote should be only be \"Y\" for yes, or \"N\" for no." 
    try: 
        end_date = ref.child(payload["channel_id"]).child("end_date").get() 
        if check_date(end_date) == 0: # Message was sent on the set end date. 
            # user_id and channel_id fields are always in the payload at this point 
            # in order to be valid payloads in the first place.
            users_ref = ref.child(payload["channel_id"]).child('users')
            users_ref.update({
                payload["user_id"] : choice
            })
            return "Vote was recorded successfully!" # EDIT!
        # Message was not sent on the end date. 
        if check_date(end_date) == -1: 
            return "Sorry! The voting period for voting to archive the channel has passed."
    except:
        # Voting hasn't been recorded in database yet. 
        return "Sorry! The voting period for voting to archive the channel has not started yet."
    return Response(status=200) 

# Determines if the parameter to /set_activity_warning_threshold{n_message} 
# is valid.
def handle_set_activity_warning_threshold_invocation(payload):
    params = payload['text']
    invalid_resp = "Sorry! The number of messages can only be a number and greater than 0. Please try again."
    params_split = params.split(" ")
    if len(params) == 0 or len(params_split) > 1 or params_split[0].isnumeric() == False or int(params_split[0]) <= 0:
        return invalid_resp
    if payload["token"] != test_token: 
        activity_warnings_bot.set_activity_warnings_threshold(payload)
    return Response(status=200)

# Determines if the parameter to /join_class is valid. 
def handle_join_class_invocation(payload):
    params_text = payload['text'].strip().split(" ")
    invalid_params_resp = "Sorry! You need to input 2 parameters (class department-class code, and class end date), as follows: <four letter department name>-<5 number course code> MM-DD-YYYY."
    invalid_class_resp = "Sorry! I can't recognize your class input. Be sure that it follows the following format: <four letter department name>-<5 number course code>"
    invalid_date_resp = "Sorry! I can't recognize your class end date input. Be sure that it follows the following format: MM-DD-YYYY"
    invalid_past_date_resp = "Sorry! Your requested date choice has already occurred in the please. Please set up a future end date."
    if len(params_text) != 2:
        return invalid_params_resp 
    class_params_text = params_text[0].split("-")
    if len(class_params_text) != 2 or len(class_params_text[0]) != 4 or len(class_params_text[1]) != 5:
        return invalid_class_resp
    dept_param = class_params_text[0]
    code_param = class_params_text[1]
    date_param = params_text[1]
    for i in range(len(dept_param)):
        if dept_param[i].isnumeric():
            return invalid_class_resp 
    for i in range(len(code_param)):
        if code_param[i].isnumeric() == False:
            return invalid_class_resp 
    end_date = ""
    try: 
        end_date = datetime.strptime(date_param, '%m-%d-%Y')
    except:
        return invalid_date_resp
    today_date = datetime.now()
    if end_date.date() < today_date.date(): # if the requested end date occurs before today's date
        return invalid_past_date_resp
    if payload["token"] != test_token:
        try:
            rv = onboarding.handle_onboarding(params_text[0], payload["user_id"])
            if ref.get() == None:
                ref.child(rv["channel"]["id"]).set({'end_date': date_param})
            elif rv["channel"]["id"] not in ref.get():
                ref.child(rv["channel"]["id"]).set({'end_date': date_param})
        except Exception as e:
            return str(e)
    return "Joined class! You can find the channel in the \"Channels\" sections of the workspace."

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
    try:
        ts = 0
        if location != "":
            ts = bot_meetup.meetup(params[0], payload, location) # payload["type"] gets updated
        else:
            ts = bot_meetup.meetup(params[0], payload) # payload["type"] gets updated
        if ts >= 10368000: # Slack only be able to schedule a message up to 120 days into the future
            return "Sorry! The date is too long into the future!"
        if payload["token"] != test_token:
            success = bot_meetup.handle_message_scheduling(message=payload["type"], channel_id=payload["channel_id"], location=location, ts=ts) 
            if not success:
                return Response(status=400)
    except:
        return "Sorry! I couldn't understand the parameters you put for the command. Be sure for the time (1st parameter) you include nonnegative numbers. The input format should be <time>, <location (optional)>. Remember the comma!"
    return Response(status=200)

# Determines if the parameter to /disable_activity_warnings{string downtime} is 
# valid. 
def handle_disable_activity_warnings_invocation(payload):
    invalid_resp = "Sorry! I couldn't recognize your time format. Please include an input with nonnegative numbers or an empty input and try again. Note that an empty input means an indefinite disabling, but you can still re-enable!"
    if payload["token"] != test_token and payload["text"].strip() == "": # check for indefinite removal request
        activity_warnings_bot.disable_activity_warnings(payload) 
    elif is_time_format_valid(payload['text']) == False: # invalid time format requests
        return invalid_resp
    elif payload["token"] != test_token: # valid time format requests 
        if payload["text"].strip() != "":
            # convert time to days, since currently we only account for day inputs
            future_time = timedelta(seconds=bot_meetup.meetup(payload["text"], payload))
            payload["text"] = str(future_time.days) + "d"
        activity_warnings_bot.disable_activity_warnings(payload) 
    return Response(status=200)

# Determines if the parameter to /disable_mood_messages{string downtime} is 
# valid.
def handle_disable_mood_messages_invocation(payload):
    invalid_resp = "Sorry! I couldn't recognize your time format. Please include an input with nonnegative numbers or an empty input and try again. Note that an empty input means an indefinite disabling, but you can still re-enable!"
    if payload['text'].strip() != "" and is_time_format_valid(payload['text'].strip()) == False: 
        return invalid_resp
    if payload["token"] != test_token:
        if payload["text"].strip() != "":
            future_time = timedelta(seconds=bot_meetup.meetup(payload["text"], payload))
            payload["text"] = str(future_time.days) + "d"
        mood_messages_bot.disable_mood_messages(payload) 
    return Response(status=200)

#Checks whether we have reached the end date of the channel
#if we did, returns 0, if not return -1, if we're 1 day after the end_date, return 1
def check_date(*end_date):
    #global global_curr_time_voting
    global vote_test
    global vote_results_test
    if len(end_date) > 1:
        vote_test = False
        vote_results_test = False
    end_date = end_date[0]
    today = date.today()
    ending_date = datetime.strptime(end_date, "%m-%d-%Y").date()
    day_after = ending_date + timedelta(days=1)
    if vote_test: 
        return 0
    if vote_results_test:
        return 1
    if today == ending_date:
        return 0
    elif today == day_after:
        return 1
    else:
        return -1

#Sends a message to the channel asking people to vote for or against archiving the channel
def send_poll_msg(channel_id, text):
    msg_rv = web_client.chat_postMessage(channel=channel_id, text=text)
    if (not msg_rv["ok"]):
        print(msg_rv["error"])
        return Response(status=400)    
    return msg_rv

#Checks poll results by traversing through the database and recording
#user responses (Y/N or X)
def check_poll_results(channel_id):
    json_dict = ref.get()
    channel_users = json_dict[channel_id]['users']
    total_users = len(channel_users)
    y_count = 0
    n_count = 0
    for key in channel_users:
        if (channel_users[key] == 'Y'):
            y_count += 1
        elif (channel_users[key] == 'N'):
            n_count += 1
    if (y_count > total_users / 2):
        return 1
    else:
        return 0

#This function is called every 24hours to check if today is the end date
#If we have reached the end date, it sends out a message to the chat asking users to vote
#for or against archiving the channel.
#The next day it counts up the votes and either archives the channel or keeps it.
def archive_channel(channel_id): 
    global vote_test
    global vote_results_test
    json_dict = ref.get()
    if json_dict == None:
        return Response(status=200)
    end_date = ""
    if channel_id in json_dict and 'end_date' in json_dict[channel_id]:
        end_date = json_dict[channel_id]['end_date']
    else:
        return Response(status=200)
    if check_date(end_date) == 0: 
        #global_curr_time_voting = datetime.now(pytz.timezone('US/Central'))
        #Send a poll to the channel asking whether members want to delete the group
        #Get channel members and add them to the database:
        members_rv = web_client.conversations_members(channel=channel_id)
        if (not members_rv["ok"]):
            print(members_rv["error"])
            return Response(status=400)
        members_list = members_rv['members']
        members_dict = {}
        for member in members_list:
            if member != actual_bot_user_id: # ignore the bot as being counted as a member
                members_dict[member] = 'X'
        channel_ref = ref.child(channel_id)
        channel_ref.set({
            'end_date': end_date,
            'users': members_dict
        })
        #Send message to the chat
        msg_text = "Last day of class! If you are in favor of archiving this channel, message me with the command `/vote_archive YorN` (for example, `/vote_archive Y` or `/vote_archive N`). I will count up the votes at the end of the day!"
        #vote_test = False
        #vote_results_test = False
        return send_poll_msg(channel_id, msg_text)
    elif check_date(end_date) == 1:
        if check_poll_results(channel_id) == 1:
            archive_rv = web_client.conversations_archive(channel=channel_id) 
            if (not archive_rv["ok"]):
                print(archive_rv["error"])
                return Response(status=400) 
            ref.child(channel_id).delete()
        else:
            pass
        vote_test = False
        vote_results_test = False

# Updates the list of channels in the workspace and calls archive_channel, 
# check_send_activity_warning, and check_send_mood_message for each channel
def check_channels():
    global check_channel_test
    global vote_test
    global vote_results_test 
    curr_time = datetime.now(pytz.timezone('US/Central'))
    if (curr_time.hour == 0 and curr_time.minute == 0) or check_channel_test: # midnight US central time  
        rv = web_client.conversations_list(exclude_archived=True, types="public_channel,private_channel")
        if (not rv["ok"]):
            print(rv["error"])
            return Response(status=400) 
        channels = rv['channels']
        for channel in channels:
            # Currently if there is a private channel that exists the bot made it will not join and archive that channel. 
            if ("is_channel" in channel and channel['is_channel']) and ("is_general" in channel and channel['is_general'] == False) and channel["is_member"] == True: 
                archive_channel(channel['id'])
                sent_aw = activity_warnings_bot.check_send_activity_warning({"token":"not_test_token", "channel_id":channel["id"]})
        check_channel_test = False # prevent from entering if statement every minute during live testing
        vote_results_test = False
        vote_test = False

# failsafe function for in case the check channel process fails for some reason. 
def onLoopError(failure):
    print(failure.getBriefTraceback())
    reactor.stop()

# run check_channels 
def do_channel_check():
    loopChannelCheck = task.LoopingCall(check_channels)
    loopDeferred = loopChannelCheck.start(60) #60=every minute
    loopDeferred.addErrback(onLoopError)
    reactor.run()

# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    # Enables a running of daily channel check code and flask app simultaneously. 
    p = Process(target=do_channel_check)
    p.start()
    bot_app.run(debug=True, use_reloader=False, threaded=True)
    p.join()