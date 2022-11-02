import unittest
from bot import *

# Filename: test_activity_warnings.py
# 
# Purpose: Test suite containing unit tests for the functionality of the
# activity warnings of the Slack Bot

class Test_Slash_Command_Activity_Warnings(unittest.TestCase): 
    # Expected JSON responses for the relevant events you want to handle for your feature can be 
    # found here: https://api.slack.com/events?filter=Events
    def setUp(self):
        self.payload = {}
        
    # This test case tests the functionality of the function
    # enable_activity_warnings() 
    def test_enable_activity_warnings(self):

        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/enable_activity_warnings",
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
                "text": "*Enabled activity warnings.*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Activity warning threshold is set to 5 (default)."
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = enable_activity_warnings(self)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        # self.assertTrue(activity_warnings_enabled) uncomment for implementing
    
    # This test case tests the functionality of the function
    # disable_activity_warnings(), where activity warnings are disabled
    # indefinitely (no parameter given in the function)
    def test_disable_activity_warnings_indefinite(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_activity_warnings",
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
                "text": "*Disabled activity warnings.*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Activity warnings disabled indefinitely."
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = disable_activity_warnings(self)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        # uncomment when implementing
        # self.assertFalse(activity_warnings_enabled)
        # self.assertEqual("", activity_warnings_downtime)
    # This test case tests the functionality of the function
    # disable_activity_warnings(), where activity warnings are disabled
    # for a specified definite downtime
    def test_disable_activity_warnings_definite_minutes(self):
        # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/disable_activity_warnings",
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
        downtime_response = "Activity warnings disabled for " + payload["text"] + "."
        expected_cmd_output ={
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Disabled activity warnings.*"
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
        cmd_output = disable_activity_warnings(self)
        # Now check our values
        self.assertEqual(cmd_output, expected_cmd_output)
        # uncomment when implementing 
        # self.assertEqual("3d", activity_warnings_downtime)
    
    # This test case is for set_activity_warning_content function where 
    # no text is given (reset to original)
    def test_set_activity_warnings_content_none(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_content",
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
                "text": "*Set activity warnings content to:*"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Let's get more active!"
                    }
                }
            ]
        }
        # This is where we call the function
        cmd_output = set_activity_warnings_content(self)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        # Uncomment when implementing
        # self.assertEqual(activity_warnings_content, "Let's get more active!")
    
        # This test case is for the set_activity_warning_threshold function, and 
    # tests to make sure the message returned by the bot is correct
    def test_set_activity_warnings_threshold(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_threshold",
            "text":"10",
            "response_url":"https://hooks.slack.com/commands/1234/5678",
            "trigger_id":"13345224609.738474920.8088930838d88f008e0",
            "api_app_id":"A123456"
        }
        self.payload = slash_cmd
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        expected_cmd_output = {
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Set activity warning threshold to 10.*"
            }
        }
            ]
        }
        # This is where we call the function
        cmd_output = set_activity_warnings_threshold(self)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        # self.assertEqual(10, activity_warnings_threshold) #Uncomment when implementing
    
    # This test case is for set_activity_warning_content function where 
    # text is given 
    def test_set_activity_warnings_content_given(self):
    # First let's set input of the slash command
        slash_cmd = {
            "token":"test_token_1",
            "team_id":"T0001",
            "team_domain":"test_domain",
            "channel_id":"C2147483705",
            "channel_name":"Test_Channel_1",
            "user_id":"U2147483697",
            "user_name":"Test_User_1",
            "command":"/set_activity_warning_content",
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
                "text": "*Set activity warnings content to:*"
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
        cmd_output = set_activity_warnings_content(self)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
        # uncomment when implementing
        # self.assertEqual(activity_warnings_content, "lol")

    # This test case is for check_activity, a function called by the script 
    # that checks how many messages have been sent in a channel in the past 24hr
    def test_check_activity(self):
        # Set what we expect
        expected_cmd_output = 10
        
        # This is where we call the function
        cmd_output = check_activity(self)

        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)

    # This test case is for send_activity_warning, a function called by the 
    # script that sends a message to the channel encouraging users to chat
    def test_send_activity_warning(self):
        # Set what we expect
        expected_cmd_output = {
        "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": activity_warnings_content
            }
        }
            ]
        }
        # This is where we call the function
        cmd_output = send_activity_warning(self)
        # Now check our values
        self.assertEqual(expected_cmd_output, cmd_output)
    
if __name__ == '__main__':
    unittest.main()