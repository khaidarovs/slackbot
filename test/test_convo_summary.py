import unittest
from unittest.mock import patch
from iter2_activity_mood_convo_bot import *
import requests

# Filename: test_convo_summary.py
# 
# Purpose: Test suite containing unit tests for the functionality of the
# conversation summary of the Slack Bot

class Test_Slash_Command_Activity_Warnings(unittest.TestCase): 
    # Expected JSON responses for the relevant events you want to handle for your feature can be 
    # found here: https://api.slack.com/events?filter=Events
    def setUp(self):
        self.payload = {}
    
    # Tests the functionality of the conversation summary feature, which posts
    # a message in chat summarizing the messages in the past N hours (specified
    # by user doing the slash cmd). This tests if there are 0 msgs in past N hr
    def test_convo_summary_0_msgs(self):
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "dummy_messages":[],
        "hrs":5
        }
        self.payload = input
        n_msgs, msg_sent = summarize_conversation(self.payload)
        self.assertEqual(n_msgs, 0)
        self.assertFalse(msg_sent)

    # Tests the functionality of the conversation summary feature, which posts
    # a message in chat summarizing the messages in the past N hours (specified
    # by user doing the slash cmd). This tests if there are some msgs in the 
    # past N hrs, and also checks if the parse_messages
    def test_conv_summary_some_msgs(self):
        input = {
        "token":"test_token_1",
        "channel_id":"CTEST1",
        "dummy_messages":[
            {"text": "I missed class today. Can somebody explain the observer pattern please?"},
            {"text": "Sure, I can explain. It may be easier if we discuss this over the phone"},
            {"text": "OK. Let's meet up at 7pm today"},
            {"text": "I can't make 7pm, can we do later?"},
            {"text": "Sure, let's meet at 9pm tonight"},
            {"text": "Sounds good, do we want to discuss anything else?"},
            {"text": "I wanted to talk also review the interpretor pattern."},
            {"text": "Ok cool. The interpretor pattern is also confusing for me"}
        ],
        "hrs": 5
        }
        self.payload = input
        n_msgs, msg_sent = summarize_conversation(self.payload)
        self.assertEqual(n_msgs, len(input.get('dummy_messages')))
        self.assertTrue(msg_sent)

    #Tests the functionality of the summarizer_model(), to see whether it is sending
    #the right message to the chat
    def test_summary_model(self):
        input_msg = "I missed class today. Can somebody explain the observer pattern please? Sure, I can explain. It may be easier if we discuss this over the phone OK. Let's meet up at 7pm today I can't make 7pm, can we do later? Sure, let's meet at 9pm tonight Sounds good, do we want to discuss anything else? I wanted to talk also review the interpretor pattern. Ok cool. The interpretor pattern is also confusing for me"
        summary = summary_model(input_msg)
        output_msg = " It may be easier if we discuss this over the phone OK. Let's meet up at 7pm today I can't make 7pm, can we do later? Sure, let's meet at 9pm tonight Sounds good, do we want to discuss anything else?"
        self.assertEqual(summary, output_msg)

        
