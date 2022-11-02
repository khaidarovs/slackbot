import unittest
import bot
from flask import Response
from bot import bot_app

bot_app.testing = True

# TestSlashCommandHandling contains a test suite for handle_slash_command and 
# the set of functions that are directly called in response to 
# handle_slash_command parsing a valid payload. These functions would solely
# be determining if the parameters of the requested commands are valid, and
# if so are calling the relevant command implementation functions to carry the 
# command out. 
class TestSlashCommandHandling(unittest.TestCase): 
    def setUp(self):
        # Command names 
        self.meetup_command = "/meetup"
        self.enable_activity_warnings_command = "/enable_activity_warnings"
        self.disable_activity_warnings_command = "/disable_activity_warnings"
        self.set_activity_warning_threshold_command = "/set_activity_warning_threshold"
        self.set_activity_warning_content_command = "/set_activity_warning_content"
        self.enable_mood_messages_command = "/enable_mood_messages"
        self.disable_mood_messages_command = "/disable_mood_messages"
        self.join_class_command = "/join_class"
        # The string messages, when returned back to handle_slash_command, 
        # sends a private message in the Slack channel where the command 
        # was invoked, to only the user who invoked the slash command.
        self.invalid_meetup_command_response = "Sorry! I couldn't understand the parameters you put for the command. Be sure for the time (1st parameter) you include nonnegative numbers."
        self.invalid_activity_warning_threshold_response = "Sorry! The number of messages can only be a number and greater than 0. Please try again."
        self.invalid_time_format_response = "Sorry! I couldn't recognize your time format. Please include nonnegative numbers in your input and try again."
        self.invalid_course_format_response = "Sorry! I can't recognize your class input. Be sure that it follows the following format: <four letter department name> <5 number course code>"
        # Valid acknowledgement response to Slack's HTTP POST request. Indicates 
        # successful command invocation for us since the relevant actions would
        # have been done in the workspace prior to this response being returned.
        self.valid_payload_response = Response(status=200)
        # Used only in handle_slash_command.
        self.defective_payload_response = Response(status=400)
    
    # ---------- Payload construction helper functions for tests. ----------
    # For every command, if the payload does not contain any valid channel 
    # information("channel_id" and "channel_name" attributes are either missing
    # or invalid), the payload would be considered defective. This is because 
    # in carrying out these commands the bot needs to know where the command 
    # was invoked from. 
    def make_defective_payload(self, command, text):
        return {
            'team_id': 'team-id', 'team_domain': 'team-domain', 
            'channel_name': '', 'user_id': 'user-id', 
            'user_name': 'user-name', 'command': command, 'text': text
            }
    def make_non_defective_payload(self, command, text):
        return {
            'team_id': 'team-id', 'team_domain': 'team-domain', 
            'channel_id': 'channel-id', 'channel_name': 'channel-name', 
            'user_id': 'user-id', 'user_name': 'user-name', 
            'command': command, 'text': text
        }
    
    # Note that for testing we don't need to account for the slash command 
    # itself being incorrectly typed, since Slack only sends over payload 
    # information if the user chose or typed a valid slash command they 
    # wanted to use, from within the workspace. handle_slash_command function 
    # partly exists to reduce the number of endpoints Slack sends a slash 
    # command to, which helps for simplifying live testing.
    def test_handle_slash_command_defective_payload(self):
        defective_payload = self.make_defective_payload(self.enable_activity_warnings_command, '')
        with bot_app.test_client() as client:
            client.post(defective_payload['command'], data=defective_payload)
            actual_response = bot.handle_slash_command()
            self.assertEqual(actual_response, self.defective_payload_response)
    def test_handle_slash_command_valid_payload(self):
        # /enable_activity_warnings_command and /enable_mood_messages_command 
        # don't have parameters to parse, so handle_slash_command() would call
        # directly the implementation functions instead of sending them to 
        # additional handler functions. 
        valid_payload = self.make_non_defective_payload(self.enable_activity_warnings_command, '')
        with bot_app.test_client() as client:
            client.post(valid_payload['command'], data=valid_payload)
            actual_response = bot.handle_slash_command()
            self.assertEqual(actual_response, self.valid_payload_response)

    def test_is_time_format_valid(self):
        # Invalid time format: time needs to contain nonnegative numbers. If 
        # none or invalid units (h, d, m, s), seconds per minute are assumed. 
        # Empty string would return false on the grounds of containing no 
        # nonnegative numbers. 
        self.assertFalse(bot.is_time_format_valid("not-valid-time"))
        self.assertFalse(bot.is_time_format_valid("-12s"))
        self.assertTrue(bot.is_time_format_valid("1d"))
        self.assertTrue(bot.is_time_format_valid("10 10"))
        self.assertTrue(bot.is_time_format_valid("1d2s"))
        self.assertTrue(bot.is_time_format_valid("30s30s"))

    # ---------- handle_disable_activity_warnings_invocation(payload) ----------
    def test_valid_disable_activity_warnings_invocation(self):
        valid_payload = self.make_non_defective_payload(self.disable_activity_warnings_command, '2h')
        actual_response = bot.handle_disable_activity_warnings_invocation(valid_payload)
        self.assertEqual(actual_response, self.valid_payload_response)
    def test_invalid_disable_activity_warnings_invocation(self):
        invalid_payload = self.make_non_defective_payload(self.disable_activity_warnings_command, 'not-valid-time')
        actual_response = bot.handle_disable_activity_warnings_invocation(invalid_payload)
        self.assertEqual(actual_response, self.invalid_time_format_response)

    # ---------- handle_set_activity_warning_threshold_invocation(payload) ----------
    def test_valid_set_activity_warning_threshold_invocation(self):
        valid_payload = self.make_non_defective_payload(self.set_activity_warning_threshold_command, '2')
        actual_response = bot.handle_set_activity_warning_threshold_invocation(valid_payload)
        self.assertEqual(actual_response, self.valid_payload_response)
    def test_invalid_set_activity_warning_threshold_invocation(self):
        invalid_payload_zero = self.make_non_defective_payload(self.set_activity_warning_threshold_command, '0')
        actual_response = bot.handle_set_activity_warning_threshold_invocation(invalid_payload_zero)
        self.assertEqual(actual_response, self.invalid_activity_warning_threshold_response)
        invalid_payload_negative = self.make_non_defective_payload(self.set_activity_warning_threshold_command, '-1')
        actual_response = bot.handle_set_activity_warning_threshold_invocation(invalid_payload_negative)
        self.assertEqual(actual_response, self.invalid_activity_warning_threshold_response)
        invalid_payload_nonnumber = self.make_non_defective_payload(self.set_activity_warning_threshold_command, 'a1')
        actual_response = bot.handle_set_activity_warning_threshold_invocation(invalid_payload_nonnumber)
        self.assertEqual(actual_response, self.invalid_activity_warning_threshold_response)

    # ---------- handle_set_activity_warning_content_invocation(payload) ----------
    def test_valid_set_activity_warning_content_invocation(self):
        valid_payload = self.make_non_defective_payload(self.set_activity_warning_content_command, '')
        actual_response = bot.handle_set_activity_warning_content_invocation(valid_payload)
        self.assertEqual(actual_response, self.valid_payload_response)

    # ---------- handle_disable_mood_messages_invocation(payload) ----------
    def test_valid_disable_mood_messages_invocation(self):
        valid_payload = self.make_non_defective_payload(self.disable_mood_messages_command, '10m')
        actual_response = bot.handle_disable_mood_messages_invocation(valid_payload)
        self.assertEqual(actual_response, self.valid_payload_response)
    def test_invalid_disable_mood_messages_invocation(self):
        invalid_payload = self.make_non_defective_payload(self.disable_mood_messages_command, "-1s")
        actual_response = bot.handle_disable_mood_messages_invocation(invalid_payload)
        self.assertEqual(actual_response, self.invalid_time_format_response)

    # ---------- handle_join_class_invocation(payload) ----------
    def test_valid_handle_join_class_invocation(self):
        valid_payload = self.make_non_defective_payload(self.join_class_command, 'CSMC 22001')
        actual_response = bot.handle_join_class_invocation(valid_payload)
        self.assertEqual(actual_response, self.valid_payload_response)
    def test_invalid_handle_join_class_invocation(self):
        # Current class input rules (specific to UChicago courses): 
        # <four letter department name> <5 number course code>
        invalid_payload_empty = self.make_non_defective_payload(self.join_class_command, '')
        actual_response = bot.handle_join_class_invocation(invalid_payload_empty)
        self.assertEqual(actual_response, self.invalid_course_format_response)
        invalid_payload_len_wrong = self.make_non_defective_payload(self.join_class_command, 'C 2')
        actual_response = bot.handle_join_class_invocation(invalid_payload_len_wrong)
        self.assertEqual(actual_response, self.invalid_course_format_response)

    # ---------- handle_meetup_invocation(payload) ----------
    # Testing for an issue related to user parameter input for /meetup command.
    def test_invalid_handle_meetup_invocation(self):
        # Mandatory time string parameter doesn't correspond to a valid time format.
        invalid_payload = self.make_non_defective_payload(self.meetup_command, 'not-a-valid-time')
        actual_response = bot.handle_meetup_invocation(invalid_payload)
        self.assertEqual(actual_response, self.invalid_meetup_command_response)
    # test_valid_meetup_optionals_invocation and test_valid_meetup_no_optionals_invocation
    # test the ability to parse the optional vs. mandatory parameter invoked by user.
    def test_valid_meetup_optional_invocation(self):
        # Testing for a valid input for /meetup command, with the optional parameters too.
        # Parameters are put in order: first date, location, then reminder.
        valid_command_payload_optional = self.make_non_defective_payload(self.meetup_command, "1d,location")
        actual_response = bot.handle_meetup_invocation(valid_command_payload_optional)
        self.assertEqual(actual_response, self.valid_payload_response)
    def test_valid_meetup_no_optional_invocation(self):
        # Testing for a valid input for /meetup command, with only it's mandatory parameter.
        valid_command_payload_no_optionals_1 = self.make_non_defective_payload(self.meetup_command, "1d")
        actual_response = bot.handle_meetup_invocation(valid_command_payload_no_optionals_1)
        self.assertEqual(actual_response, self.valid_payload_response)
        valid_command_payload_no_optionals_2 = self.make_non_defective_payload(self.meetup_command, "2d 6s")
        actual_response = bot.handle_meetup_invocation(valid_command_payload_no_optionals_2)
        self.assertEqual(actual_response, self.valid_payload_response)

if __name__ == '__main__':
    unittest.main()