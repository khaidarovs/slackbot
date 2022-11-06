import json
import os
from dotenv import load_dotenv
from slack import WebClient
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack_sdk.errors import SlackApiError
from pathlib import Path

env_path = Path('.')/'.env'
load_dotenv(dotenv_path = env_path)

bot_app = Flask(__name__)

slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/slack/events", bot_app)

web_client = WebClient(token=os.environ["BOT_TOKEN"])

# database to store any conversations information
conversations_store = {}
#list of lists of format [[id, channel_name], [id, channel_name]]
channels = []
def fetch_conversations():
    try:
        # Call the conversations.list method using the WebClient
        result = web_client.conversations_list()
        save_conversations(result["channels"])
    except SlackApiError as e:
        logger.error("Error fetching conversations: {}".format(e))

# Put conversations into the JavaScript object
def save_conversations(conversations):
    conversation_id = ""
    for conversation in conversations:
        # Key conversation info on its unique ID
        conversation_id = conversation["id"]
        channels.append([conversation["id"], conversation["name"]])
        # Store the entire conversation object
        # (you may not need all of the info)
        conversations_store[conversation_id] = conversation

fetch_conversations()


#member joined channel event listener
@slack_event_adapter.on('member_joined_channel')
def welcome_new_user(payload):
    event = payload.get('event', {})
    channel_name = get_channel_name(event.get('channel'))
    welcome_text = "Welcome to StudyRoom! To join a class, message me with the command `/join_class SUBJ-#####` (for example, `/join_class CMSC-22001), and I'll add you the study group."
    if(channel_name == 'general'):
        return send_im_message(event.get('user'), welcome_text)
    return True

#returns channel name with a search by id
def get_channel_name(id):
    #TODO next iteration
    pass

#returns private message channel id of the App
def get_im_id(user):
    #TODO next iteration
    pass
#sends a message to the private channel between user and app
def send_im_message(userid, text):
    #TODO next iteration
    pass

def check_channel(channel):
    #access second element in channels (which is list of [id, channel_names]s)
    channel_names = [el[1] for el in channels]
    return channel in channel_names

def handle_onboarding():
    #TODO 
    pass

# web_client.chat_postMessage(channel='#general', text='Hello World!')
# Allows us to set up a webpage with the script, which enables testing using tools like ngrok.
if __name__ == "__main__":
    bot_app.run(debug=True, port=3000)



