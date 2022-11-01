import unittest
from bot import *

# Filename: test_activity_warning.py
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
        self.payload = {slash_cmd}
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
        self.assertEqual(self.payload, {cmd_output, expected_cmd_output})
    
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
        self.payload = {slash_cmd}
        payload = self.payload
        # Now we indicate our expected output
        # Note: this is an ephemeral message. This message will only be visible
        # To the user who called the command
        if payload["text"] == "":
            # Payload is empty, disable indefinitely
            downtime_response = "Activity warnings disabled indefinitely."
        else:
            # We were given a downtime for activity warnings, set accordingly
            downtime_response = "Activity warnings disabled for " + payload.text + "."

        cmd_output ={
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
        self.assertEqual(self.payload, {cmd_output, expected_cmd_output})

if __name__ == '__main__':
    unittest.main()