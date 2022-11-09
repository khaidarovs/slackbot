
import unittest
from unittest.mock import patch
from bot import *
import requests

# Filename: test_mood_messages.py
# 
# Purpose: Test suite containing unit tests for the functionality of the
# mood messages of the Slack Bot

class Test_Slash_Command_Mood_Messages(unittest.TestCase): 
    # Expected JSON responses for the relevant events you want to handle for your feature can be 
    # found here: https://api.slack.com/events?filter=Events
    def setUp(self):
        self.payload = {}
        
    # This test case tests the functionality of the function
    # enable_mood_messages() 
    def test_enable_mood_messages(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/mood_messages",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Enabled mood messages.*"
            }
        }
        ]
        }
        #This is where we call the function
        cmd_output = enable_mood_messages(self)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        self.assertTrue(mood_messages_enabled.get()) 
    
    # This test case tests the functionality of the function
    # disable_mood_messages(), where mood messages are disabled
    # indefinitely (no parameter given in the function)
    def test_disable_mood_messages_indefinite(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_mood_messages",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        payload = self.payload
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command

        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Disabled mood messages.*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Mood messages disabled indefinitely."
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = disable_mood_messages(self)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        # uncomment when implementing
        self.assertFalse(mood_messages_enabled.get())
        self.assertEqual("", mood_messages_downtime.get())
    # This test case tests the functionality of the function
    # disable_mood_messages(), where mood messages are disabled
    # for a specified definite downtime
    def test_disable_mood_messages_definite_minutes(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_mood_messages",
            "text":"3d",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        payload = self.payload
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        downtime_response = "Mood messages disabled for " + payload["text"] + "."
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Disabled mood messages.*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": downtime_response
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = disable_mood_messages(self)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        self.assertEqual("3d", mood_messages_downtime.get())
    
    # This test case is for set_mood_warning_content function where 
    # no text is given (reset to original)
    def test_set_mood_messages_content_none(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_mood_messages_content",
            "text":"",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set mood messages content to:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Let's be more positive!"
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = set_mood_messages_content(self)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        self.assertEqual(mood_message_content.get(), "Let's be more positive!")
    
    
    # This test case is for set_mood_warning_content function where 
    # text is given 
    def test_set_mood_messages_content_given(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_mood_messages_content",
            "text":"lol",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set mood messages content to:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "lol"
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = set_mood_messages_content(self)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        # uncomment when implementing
        self.assertEqual(mood_message_content.get(), "lol")

        # This test case is for check_mood, a function called by the script 
    # that assesses the general mood of the group chat and outputs either 1, 0, or -1
    # 1 being positive, 0 being neutral, and -1 being negative
    def test_check_mood(self):
        #check when mood is negative
        inp = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "I am so sad",
        }
        # Set what we expect
        expected_cmd_output = -1

        # Call the function
        cmd_output = check_mood(self, inp)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

        #Test for when the mood is neutral
        inp1 = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "I am so neutral",
        }
        # Set what we expect
        expected_cmd_output = 0

        #Call the function
        cmd_output = check_mood(self, inp1)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

        #Test for when the mood is neutral
        inp2 = {
        "token": "z26uFbvR1xHJEdHE1OQiO6t8",
        "channel": "C2147483705",
        "user": "U2147483697",
        "text": "I am so happy!",
        }
        # Set what we expect
        expected_cmd_output = 1

        #Call the function
        cmd_output = check_mood(self, inp2)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

    # This test case is for send_mood_warning, a function called by the 
    # script that sends a message to the channel encouraging users to chat
    def test_send_mood_message(self):
        input = {
            "token":"test_token_1",
            "channel_id":"C2147483705"
        }
        self.payload = input
        # Set what we expect
        expected_cmd_output ={"blocks": [{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Mood Message*"
        }},{
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": mood_message_content.get()
        }}]}
        # This is where we call the function
        cmd_output = send_mood_message(self)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
    
if __name__ == '__main__':
    unittest.main()