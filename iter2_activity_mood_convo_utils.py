# This file contains shared variables between activity, mood, and conversation
# for iteration 2. 

from dotenv import load_dotenv
import json
import os
from slack import WebClient
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import firebase_admin
from firebase_admin import credentials, db
import time
from nltk import download
import matplotlib.pyplot as plt
from nltk.sentiment import SentimentIntensityAnalyzer

load_dotenv()

cred = credentials.Certificate(os.environ['SVC_ACCT_KEY'])
firebase_admin.initialize_app(cred, {
    'databaseURL': os.environ['DBURL']
})
ref = db.reference('slackbot/')

# Load the tokens from the ".env" file, which are set up as environment variables. 
# You'll need the signing secret and bot token from the Slack developer console 
# for a workspace, which you put in a file you make called ".env". It prevents a 
# security risk related to revealing secret keys in public. 

bot_app = Flask(__name__)

# You can find the signing secret token in the "Basic Information" -> "App Credentials" sections 
# of the Slack workspace developer console. By "/slack/events" is the endpoint that you would
# attach to the end of the ngrok link when inputting the request URL in the "Event Subscriptions"
# -> "Enable Events" section of the Slack workspace developer console.  
SIGNING_SECRET = os.environ['SIGNING_SECRET']
BOT_TOKEN = os.environ['BOT_TOKEN']
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", bot_app)

# You can find the bot token in the "OAuth & Permissions" section of the Slack workspace developer 
# console.

web_client = WebClient(token=BOT_TOKEN)
