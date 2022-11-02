import unittest
import bot
from flask import Response
from bot import bot_app

bot_app.testing = True

# Make seperate classes depending on what particular features you want to test.
# Could also make multiple test files. This is just an example class I made, 
# feel free to remove or delete. Run the tests here via this command: 
# python -m unittest test.py
class TestMessageHandlingExample(unittest.TestCase): 
    # Expected JSON responses for the relevant events you want to handle for your feature can be 
    # found here: https://api.slack.com/events?filter=Events
    def setUp(self):
        self.payload = {}
    def test_function(self):
        self.payload = {"hi":"hi"}
        self.assertEqual(self.payload, {"hi":"hi"})
"""
A test suite for the handle_message_event() function which tests the two 
functions that are used inside: check_valid_payload() and parse_payload().
- The first test is going to check whether the check_valid_payload() function
determines whether the payload is missing any information
- The second test is going to check whether parse_payload() is able to determine 
whether the subtype of the message event is irrelevant and thus returns an empty dictionary,
whether the user ID is the same as the bot ID (message sent by the bot) and thus returns an empty dictionary,
or if everything is fine and it returns a valid dictionary with the useful information.
"""
class TestCheckingPayload(unittest.TestCase):
    def setUp(self):
        self.payload = {
                            "type": "message",
                            "channel": "C2147483705",
                            "user": "U2147483697",
                            "text": "Hello world",
                            "ts": "1355517523.000005"
                        }
        self.bad_payload = {
                                "type": "message",
                                "channel": "",
                                "user": "U2147483697",
                                "text": "Hello world",
                                "ts": "1355517523.000005"
                            }
        self.bad_payload2 = {
                                "type": "message",
                                "channel": "C2147483705",
                                "user": "",
                                "text": "Hello world",
                                "ts": "1355517523.000005"
                            }

    def test_valid_payload(self):
        print("TESTING THE VALID PAYLOAD\n")
        self.assertTrue(bot.check_valid_payload(self.payload))
        self.assertFalse(bot.check_valid_payload(self.bad_payload))
        self.assertFalse(bot.check_valid_payload(self.bad_payload2))

    def test_parsing_payload(self):
        print("TESTING PARSING THE PAYLOAD\n")
        bot_id1 = "U2147483697"
        bot_id2 = "U2147483698"
        expected_output = {
                            "type": "message",
                            "channel": "C2147483705",
                            "user": "U2147483697",
                            "text": "Hello world",
                            "ts": "1355517523.000005"
                          }
        self.assertEqual(bot.parse_payload(self.payload, bot_id1), {})
        self.assertEqual(bot.parse_payload(self.payload, bot_id2), expected_output)

class TestHandlingWorkspace(unittest.TestCase):
    def setUp(self):
        self.payload = {
                            "type": "channel_created",
                            "channel": {
                                "id": "C024BE91L",
                                "name": "fun",
                                "created": 1360782804,
                                "creator": "U024BE7LH"
                            }
                        }
    
    def test_channel_creation(self):
        bot_id1 = "U2147483697"
        bot_id2 = "U024BE7LH"
        print("TESTING CHANNEL CREATION")
        # print(self.payload.get("channel").get("creator"))
        self.assertTrue(bot.check_id(self.payload, bot_id1))
        self.assertFalse(bot.check_id(self.payload, bot_id2))


if __name__ == '__main__':
    unittest.main()