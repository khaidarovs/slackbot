import unittest
import bot_events_commands
from flask import Response, request
from bot_events_commands import bot_app, test_token, test_team_id
from datetime import date, timedelta

bot_app.testing = True

# Compare if the responses are the same string messages or are the same 
# response types. Moved outside of TestSlashCommandHandling since multiple
# test suites use this function.
def same_responses(resp1, resp2):
    if resp1.__class__.__name__ != resp2.__class__.__name__:
        return False
    resp_type = resp1.__class__.__name__
    if (resp_type == "str" or resp_type == "dict") and resp1 == resp2: 
        return True
    if resp_type == "Response" and resp1.status == resp2.status: 
        return True
    return False

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
        self.enable_mood_messages_command = "/enable_mood_messages"
        self.disable_mood_messages_command = "/disable_mood_messages"
        self.join_class_command = "/join_class"
        self.help_command = "/help"
        # The string messages, when returned back to handle_slash_command, 
        # sends a private message in the Slack channel where the command 
        # was invoked, to only the user who invoked the slash command.
        self.invalid_meetup_command_response = "Sorry! I couldn't understand the parameters you put for the command. Be sure for the time (1st parameter) you include nonnegative numbers."
        self.invalid_activity_warning_threshold_response = "Sorry! The number of messages can only be a number and greater than 0. Please try again."
        self.invalid_disable_response = "Sorry! I couldn't recognize your time format. Please include an input with nonnegative numbers or an empty input and try again. Note that an empty input means an indefinite disabling, but you can still re-enable!"
        self.invalid_course_format_response = "Sorry! I can't recognize your class input. Be sure that it follows the following format: <four letter department name>-<5 number course code>"
        self.invalid_date_response = "Sorry! I can't recognize your class end date input. Be sure that it follows the following format: MM-DD-YYYY"
        self.invalid_past_date_response = "Sorry! Your requested date choice has already occurred in the please. Please set up a future end date."
        self.invalid_vote_choice_response = "Vote should be only be \"Y\" for yes, or \"N\" for no." 
        self.invalid_voting_params_response = "Sorry! You need to input 2 parameters (class department-class code, and class end date), as follows: <four letter department name>-<5 number course code> MM-DD-YYYY."
        self.invalid_voting_past_response = "Sorry! The voting period for voting to archive the channel has passed."
        self.invalid_voting_early_response = "Sorry! The voting period for voting to archive the channel has not started yet."
        self.join_class_success_response = "Joined class! You can find the channel in the \"Channels\" sections of the workspace." # want to more clearly inform users of the channel addition.
        self.help_response = "Visit the README.md in https://github.com/khaidarovs/slackbot for slash command instructions and a general overview of the bot!"
        self.not_in_channel_response = "StudyRoom Bot needs to be added to the channel first. Type @ and then click the bot to get Slackbot to invite it."
        # Valid acknowledgement response status to Slack's HTTP POST 
        # request. Indicates successful command invocation for us since the 
        # relevant actions would have been done in the workspace prior to 
        # this response being returned.
        self.valid_payload_response = Response(status=200)
        self.defective_payload_response = Response(status=400)
    
    # ---------- Payload construction helper functions for tests. ----------
    # For every command, if the payload does not contain any valid channel 
    # information("channel_id" and "channel_name" attributes are either missing
    # or invalid), the payload would be considered defective. This is because 
    # in carrying out these commands the bot needs to know where the command 
    # was invoked from. 
    def make_defective_payload(self, command, text):
        return {
            'token': '', 'team_id': 'team-id', 'team_domain': 'team-domain', 
            'channel_name': '', 'user_id': '', 'user_name': 'user-name', 
            'command': command, 'text': text
            }
    def make_non_defective_payload(self, command, text):
        return {
            'token': test_token, 'team_id': test_team_id, 'team_domain': 'team_domain', 
            'channel_id': 'channel_id', 'channel_name': 'channel_name', 
            'user_id': 'user_id', 'user_name': 'user_name', 'command': command, 
            'text': text
        }
    @bot_app.route('/slash-command', methods=['POST'])
    def mock_handle_slash_command(self, team_id, is_bot_in_channel):
        payload = request.form.to_dict()
        if bot_events_commands.check_valid_slash_command_payload(payload, team_id) == False:
            return Response(status=400)
        resp = Response(status=200)
        if is_bot_in_channel == False:
            return "StudyRoom Bot needs to be added to the channel first. Type @ and then click the bot to get Slackbot to invite it."
        # Keep commands that don't call functions beyond the file, since 
        # functions called beyond file require an actual token. 
        if payload['command'] == "/meetup":
            resp = bot_events_commands.handle_meetup_invocation(payload)
        elif payload['command'] == "/disable_activity_warnings":
            resp = bot_events_commands.handle_disable_activity_warnings_invocation(payload)
        elif payload['command'] == "/set_activity_warning_threshold":
            resp = bot_events_commands.handle_set_activity_warning_threshold_invocation(payload)
        elif payload['command'] == "/disable_mood_messages":
            resp = bot_events_commands.handle_disable_mood_messages_invocation(payload)
        elif payload['command'] == "/join_class":
            resp = bot_events_commands.handle_join_class_invocation(payload)
        elif payload["command"] == "/vote_archive":
            resp = bot_events_commands.handle_vote(payload)
        elif payload["command"] == "/help":
            resp = "Visit the README.md in https://github.com/khaidarovs/slackbot for slash command instructions and a general overview of the bot!"
        return resp

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
            actual_response = self.mock_handle_slash_command(defective_payload['team_id'], True)
            self.assertTrue(same_responses(actual_response, self.defective_payload_response))
    def test_handle_slash_command_valid_payload(self):
        # /enable_activity_warnings_command and /enable_mood_messages_command 
        # don't have parameters to parse, so handle_slash_command() would call
        # directly the implementation functions instead of sending them to 
        # additional handler functions. 
        valid_payload = self.make_non_defective_payload(self.enable_activity_warnings_command, '')
        with bot_app.test_client() as client:
            client.post(valid_payload['command'], data=valid_payload)
            actual_response = self.mock_handle_slash_command(valid_payload['team_id'], True)
            self.assertTrue(same_responses(actual_response, self.valid_payload_response))
            valid_payload = self.make_non_defective_payload(self.help_command, '') 
            client.post(valid_payload['command'], data=valid_payload)
            actual_response = self.mock_handle_slash_command(valid_payload['team_id'], True)
            self.assertTrue(same_responses(actual_response, self.help_response))
            valid_payload = self.make_non_defective_payload(self.enable_activity_warnings_command, '') # command issued when bot is not there
            client.post(valid_payload['command'], data=valid_payload)
            actual_response = self.mock_handle_slash_command(valid_payload['team_id'], False)
            self.assertTrue(same_responses(actual_response, self.not_in_channel_response))

    def test_is_time_format_valid(self):
        # Invalid time format: time needs to contain nonnegative numbers. If 
        # none or invalid units (h, d, m, s), seconds per minute are assumed. 
        # Empty string would return false on the grounds of containing no 
        # nonnegative numbers. 
        self.assertFalse(bot_events_commands.is_time_format_valid("not-valid-time"))
        self.assertFalse(bot_events_commands.is_time_format_valid(""))
        self.assertFalse(bot_events_commands.is_time_format_valid("-12s"))
        self.assertTrue(bot_events_commands.is_time_format_valid("12s-"))
        self.assertTrue(bot_events_commands.is_time_format_valid("1d"))
        self.assertTrue(bot_events_commands.is_time_format_valid("10 10"))
        self.assertTrue(bot_events_commands.is_time_format_valid("10o 10p"))
        self.assertTrue(bot_events_commands.is_time_format_valid("1d2s"))
        self.assertTrue(bot_events_commands.is_time_format_valid("1dy2s"))
        self.assertTrue(bot_events_commands.is_time_format_valid("30s30s"))

    # ---------- handle_disable_activity_warnings_invocation(payload) ----------
    def test_valid_disable_activity_warnings_invocation(self):
        valid_payload = self.make_non_defective_payload(self.disable_activity_warnings_command, '2h')
        actual_response = bot_events_commands.handle_disable_activity_warnings_invocation(valid_payload)
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
    def test_invalid_disable_activity_warnings_invocation(self):
        invalid_payload = self.make_non_defective_payload(self.disable_activity_warnings_command, 'not-valid-time')
        actual_response = bot_events_commands.handle_disable_activity_warnings_invocation(invalid_payload)
        self.assertTrue(same_responses(actual_response, self.invalid_disable_response))

    # ---------- handle_set_activity_warning_threshold_invocation(payload) ----------
    def test_valid_set_activity_warning_threshold_invocation(self):
        valid_payload = self.make_non_defective_payload(self.set_activity_warning_threshold_command, '2')
        actual_response = bot_events_commands.handle_set_activity_warning_threshold_invocation(valid_payload)
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
    def test_invalid_set_activity_warning_threshold_invocation(self):
        invalid_payload_zero = self.make_non_defective_payload(self.set_activity_warning_threshold_command, '0')
        actual_response = bot_events_commands.handle_set_activity_warning_threshold_invocation(invalid_payload_zero)
        self.assertTrue(same_responses(actual_response, self.invalid_activity_warning_threshold_response))
        invalid_payload_negative = self.make_non_defective_payload(self.set_activity_warning_threshold_command, '-1')
        actual_response = bot_events_commands.handle_set_activity_warning_threshold_invocation(invalid_payload_negative)
        self.assertTrue(same_responses(actual_response, self.invalid_activity_warning_threshold_response))
        invalid_payload_nonnumber = self.make_non_defective_payload(self.set_activity_warning_threshold_command, 'a1')
        actual_response = bot_events_commands.handle_set_activity_warning_threshold_invocation(invalid_payload_nonnumber)
        self.assertTrue(same_responses(actual_response, self.invalid_activity_warning_threshold_response))

    # ---------- handle_disable_mood_messages_invocation(payload) ----------
    def test_valid_disable_mood_messages_invocation(self):
        valid_payload = self.make_non_defective_payload(self.disable_mood_messages_command, '10m')
        actual_response = bot_events_commands.handle_disable_mood_messages_invocation(valid_payload)
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
    def test_invalid_disable_mood_messages_invocation(self):
        invalid_payload = self.make_non_defective_payload(self.disable_mood_messages_command, "-1s")
        actual_response = bot_events_commands.handle_disable_mood_messages_invocation(invalid_payload)
        self.assertTrue(same_responses(actual_response, self.invalid_disable_response))

    # ---------- handle_join_class_invocation(payload) ----------
    def test_valid_handle_join_class_invocation(self):
        valid_payload_upper = self.make_non_defective_payload(self.join_class_command, ' CSMC-22001 01-20-2050 ')
        actual_response = bot_events_commands.handle_join_class_invocation(valid_payload_upper)
        self.assertTrue(same_responses(actual_response, self.join_class_success_response))
        valid_payload_lower = self.make_non_defective_payload(self.join_class_command, 'csmc-22001 1-2-2050')
        actual_response = bot_events_commands.handle_join_class_invocation(valid_payload_lower)
        self.assertTrue(same_responses(actual_response, self.join_class_success_response))
    # Added an extra test compared to iteration 1. 
    def test_invalid_handle_join_class_invocation(self):
        # Current class input rules (specific to UChicago courses): 
        # <four letter department name>-<5 number course code>
        # Invalid number of params
        invalid_payload_empty = self.make_non_defective_payload(self.join_class_command, '')
        actual_response = bot_events_commands.handle_join_class_invocation(invalid_payload_empty)
        self.assertTrue(same_responses(actual_response, self.invalid_voting_params_response))
        invalid_payload_spaces = self.make_non_defective_payload(self.join_class_command, 'csmc-22001  01-01-2010') # only a single space allowed
        actual_response = bot_events_commands.handle_join_class_invocation(invalid_payload_spaces)
        self.assertTrue(same_responses(actual_response, self.invalid_voting_params_response))
        invalid_payload_missing_date = self.make_non_defective_payload(self.join_class_command, 'csmc-22001')
        actual_response = bot_events_commands.handle_join_class_invocation(invalid_payload_missing_date)
        self.assertTrue(same_responses(actual_response, self.invalid_voting_params_response))
        # Invalid class input
        invalid_payload_len_wrong = self.make_non_defective_payload(self.join_class_command, 'C-21 1-2-2050')
        actual_response = bot_events_commands.handle_join_class_invocation(invalid_payload_len_wrong)
        self.assertTrue(same_responses(actual_response, self.invalid_course_format_response))
        invalid_payload_too_many = self.make_non_defective_payload(self.join_class_command, 'csmc-22001-a21 1-2-2050')
        actual_response = bot_events_commands.handle_join_class_invocation(invalid_payload_too_many)
        self.assertTrue(same_responses(actual_response, self.invalid_course_format_response))
        # Invalid date (MM-DD-YYYY format, date needs to not be a past date)
        invalid_payload_past_date = self.make_non_defective_payload(self.join_class_command, 'csmc-22001 01-01-2010')
        actual_response = bot_events_commands.handle_join_class_invocation(invalid_payload_past_date)
        self.assertTrue(same_responses(actual_response, self.invalid_past_date_response))
        invalid_payload_wrong_date_format = self.make_non_defective_payload(self.join_class_command, 'csmc-22001 01-02-201')
        actual_response = bot_events_commands.handle_join_class_invocation(invalid_payload_wrong_date_format)
        self.assertTrue(same_responses(actual_response, self.invalid_date_response))

    # ---------- handle_meetup_invocation(payload) ----------
    # Testing for an issue related to user parameter input for /meetup command.
    def test_invalid_handle_meetup_invocation(self):
        # Mandatory time string parameter doesn't correspond to a valid time format.
        invalid_payload = self.make_non_defective_payload(self.meetup_command, 'not-a-valid-time')
        actual_response = bot_events_commands.handle_meetup_invocation(invalid_payload)
        self.assertTrue(same_responses(actual_response, self.invalid_meetup_command_response))
    # test_valid_meetup_optionals_invocation and test_valid_meetup_no_optionals_invocation
    # test the ability to parse the optional vs. mandatory parameter invoked by user.
    def test_valid_meetup_optional_invocation(self):
        # Testing for a valid input for /meetup command, with the optional parameters too.
        # Parameters are put in order: first date, location, then reminder.
        valid_command_payload_optional = self.make_non_defective_payload(self.meetup_command, "1d,location")
        actual_response = bot_events_commands.handle_meetup_invocation(valid_command_payload_optional)
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
        valid_command_payload_optional = self.make_non_defective_payload(self.meetup_command, "1d, location")
        actual_response = bot_events_commands.handle_meetup_invocation(valid_command_payload_optional)
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
    def test_valid_meetup_no_optional_invocation(self):
        # Testing for a valid input for /meetup command, with only it's mandatory parameter.
        valid_command_payload_no_optionals_1 = self.make_non_defective_payload(self.meetup_command, "1d")
        actual_response = bot_events_commands.handle_meetup_invocation(valid_command_payload_no_optionals_1)
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
        valid_command_payload_no_optionals_2 = self.make_non_defective_payload(self.meetup_command, "2d 6s")
        actual_response = bot_events_commands.handle_meetup_invocation(valid_command_payload_no_optionals_2)
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
    
    # check_valid_slash_command_payload tests. Added this test since we found 
    # that the event and slash command payloads differ in their JSON structure.
    # Added more tests and modified current tests compared to iteration 1. 
    def test_check_valid_slash_command_payload(self):
        valid_payload = self.make_non_defective_payload(self.disable_activity_warnings_command, '2h')
        actual_response = bot_events_commands.check_valid_slash_command_payload(valid_payload, valid_payload["team_id"])
        self.assertTrue(actual_response)
        missing_id_info_payload = {'team_domain': 'team_domain', 'channel_name': 'channel_name',}
        actual_response = bot_events_commands.check_valid_slash_command_payload(missing_id_info_payload, test_team_id)
        self.assertFalse(actual_response)
        wrong_workspace_payload = {'token': "not_workspace_token", 'team_id': 'not_workspace_team_id', 'team_domain': 'team_domain', 
            'channel_id': 'channel_id', 'channel_name': 'channel_name', 'user_id': 'user_id'}
        actual_response = bot_events_commands.check_valid_slash_command_payload(wrong_workspace_payload, test_team_id)
        self.assertFalse(actual_response)
        empty_info_payload = {'token': test_token, 'team_id': test_team_id, 'team_domain': 'team_domain', 
            'channel_id': '', 'channel_name': 'channel_name', 'user_id': ''}
        actual_response = bot_events_commands.check_valid_slash_command_payload(empty_info_payload, test_team_id)
        self.assertFalse(actual_response)

    # mock_handle_vote is a mock version of the handle_vote function, in which 
    # this function does not actually retrieve from and update Firebase, but 
    # the function logic from handle_vote is preserved otherwise. 
    def mock_handle_vote(self, payload, mock_channel_voting_data):
        choice = payload["text"].strip()
        if choice != "Y" and choice != "N":
            return "Vote should be only be \"Y\" for yes, or \"N\" for no." 
        try: 
            end_date = mock_channel_voting_data['channels'][payload["channel_id"]]['end_date']  
            if bot_events_commands.check_date(end_date, "test") == 0: # Message was sent on the set end date. 
                # user_id and channel_id fields are always in the payload at this point 
                # in order to be valid payloads in the first place.
                mock_channel_voting_data['channels'][payload['channel_id']]["users"][payload["user_id"]] = choice
                return mock_channel_voting_data
            # Message was not sent on the end date. 
            if bot_events_commands.check_date(end_date, "test") == -1: 
                return "Sorry! The voting period for voting to archive the channel has passed."
        except:
            # Voting hasn't been recorded in database yet. 
            return "Sorry! The voting period for voting to archive the channel has not started yet."
        return Response(status=200) 

    # test_valid_handle_vote checks for valid voting being registered.
    def test_valid_handle_vote(self):
        payload = self.make_non_defective_payload("/vote_archive", " Y ")
        today_date_str = date.today().strftime("%m-%d-%Y")
        mock_channel_voting_data = {"channels": { # Mock data that would be in Firebase
                payload["channel_id"]: {"end_date": today_date_str, "users":{}}
            }
        }
        actual_response = self.mock_handle_vote(payload, mock_channel_voting_data)
        expected_response = {"channels": {
                payload["channel_id"]: { 
                    "end_date": today_date_str, 
                    "users": {payload["user_id"]: "Y"}
                }
            }
        }
        self.assertTrue(same_responses(actual_response, expected_response))

    # test_invalid_handle_vote accounts for invalid voting being made
    def test_invalid_handle_vote(self):
        payload = self.make_non_defective_payload("/vote_archive", "Not_valid_vote")
        actual_response = self.mock_handle_vote(payload, {})
        self.assertTrue(same_responses(actual_response, self.invalid_vote_choice_response))
        payload = self.make_non_defective_payload("/vote_archive", "Y")
        # Test handling when voting period is too far in the future.
        mock_channel_voting_data = {"channels": {"end_date": "01-20-3000"}}
        actual_response = self.mock_handle_vote(payload, mock_channel_voting_data)
        self.assertTrue(same_responses(actual_response, self.invalid_voting_early_response))
        # Test handling when voting period has passed.
        mock_channel_voting_data = {"channels": {payload["channel_id"]: {"end_date": "01-20-2000"}}} 
        actual_response = self.mock_handle_vote(payload, mock_channel_voting_data)
        self.assertTrue(same_responses(actual_response, self.invalid_voting_past_response))

"""
A test suite for the handle_message_event() function which tests the two 
functions that are used inside: check_valid_event_payload() and parse_payload().
- The first test is going to check whether the check_valid_event_payload() function
determines whether the payload is missing any information
- The second test is going to check whether parse_payload() is able to determine 
whether the subtype of the message event is irrelevant and thus returns an empty dictionary,
whether the user ID is the same as the bot ID (message sent by the bot) and thus returns an empty dictionary,
or if everything is fine and it returns a valid dictionary with the useful information.
"""
class TestCheckingPayload(unittest.TestCase):
    def setUp(self):
        self.payload = {
                        "token": test_token,
                        "team_id": test_team_id,
                        "api_app_id": "A0FFV41KK",
                        "event": {
                            "type": "message",
                            "channel": "C2147483705",
                            "user": "U2147483697",
                            "text": "Hello world",
                            "ts": "1355517523.000005"
                        },
                        "type": "event_callback",
                        "authed_users": [
                            "U061F7AUR"
                        ],
                        "authorizations": [
                            {
                                "enterprise_id": "E12345",
                                "team_id": "T12345",
                                "user_id": "U12345",
                                "is_bot": False
                            }
                        ],
                        "event_id": "Ev9UQ52YNA",
                        "event_context": "EC12345",
                        "event_time": 1234567890
                    }
        self.bad_payload = { #wrong token number and wrong team_id
                        "token": "not_right_token",
                        "team_id": "not_team_id",
                        "api_app_id": "A0FFV41KK",
                        "event": {
                            "type": "message",
                            "channel": "C2147483705",
                            "user": "U2147483697",
                            "text": "Hello world",
                            "ts": "1355517523.000005"
                        },
                        "type": "event_callback",
                        "authed_users": [
                            "U061F7AUR"
                        ],
                        "authorizations": [
                            {
                                "enterprise_id": "E12345",
                                "team_id": "T12345",
                                "user_id": "U12345",
                                "is_bot": False
                            }
                        ],
                        "event_id": "Ev9UQ52YNA",
                        "event_context": "EC12345",
                        "event_time": 1234567890
                    }
        self.bad_payload2 = { #event type is missing
                        "token": test_token,
                        "team_id": test_team_id,
                        "api_app_id": "A0FFV41KK",
                        "event": {
                            "type": "",
                            "channel": "C2147483705",
                            "user": "U2147483697",
                            "text": "Hello world",
                            "ts": "1355517523.000005"
                        },
                        "type": "event_callback",
                        "authed_users": [
                            "U061F7AUR"
                        ],
                        "authorizations": [
                            {
                                "enterprise_id": "E12345",
                                "team_id": "T12345",
                                "user_id": "U12345",
                                "is_bot": False
                            }
                        ],
                        "event_id": "Ev9UQ52YNA",
                        "event_context": "EC12345",
                        "event_time": 1234567890
                    }
        self.bad_payload3 = { #event channel and user missing
                    "token": test_token,
                    "team_id": test_team_id,
                    "api_app_id": "A0FFV41KK",
                    "event": {
                        "type": "message",
                        "channel": "",
                        "user": "",
                        "text": "Hello world",
                        "ts": "1355517523.000005"
                    },
                    "type": "event_callback",
                    "authed_users": [
                        "U061F7AUR"
                    ],
                    "authorizations": [
                        {
                            "enterprise_id": "E12345",
                            "team_id": "T12345",
                            "user_id": "U12345",
                            "is_bot": False
                        }
                    ],
                    "event_id": "Ev9UQ52YNA",
                    "event_context": "EC12345",
                    "event_time": 1234567890
                }

    def test_valid_payload(self):
        print("TESTING THE VALID PAYLOAD\n")
        self.assertTrue(bot_events_commands.check_valid_event_payload(self.payload, test_team_id))
        self.assertFalse(bot_events_commands.check_valid_event_payload(self.bad_payload, test_team_id))
        self.assertFalse(bot_events_commands.check_valid_event_payload(self.bad_payload2, test_team_id))
        self.assertFalse(bot_events_commands.check_valid_event_payload(self.bad_payload3, test_team_id))

    def test_parsing_payload(self):
        print("TESTING PARSING THE PAYLOAD\n")
        payload_subtype = {
                        "token": test_token,
                        "team_id": "T061EG9RZ",
                        "api_app_id": "A0FFV41KK",
                        "event": {
                            "type": "message",
                            "subtype": "channel_join",
                            "text": "<@U023BECGF|bobby> has joined the channel",
                            "ts": "1403051575.000407",
                            "user": "U023BECGF"
                        },
                        "type": "event_callback",
                        "authed_users": [
                            "U061F7AUR"
                        ],
                        "authorizations": [
                            {
                                "enterprise_id": "E12345",
                                "team_id": "T12345",
                                "user_id": "U12345",
                                "is_bot": False
                            }
                        ],
                        "event_id": "Ev9UQ52YNA",
                        "event_context": "EC12345",
                        "event_time": 1234567890
                    }
        expected_output = {
                            "token": test_token,
                            "channel_id": "C2147483705",
                            "user": "U2147483697",
                            "text": "Hello world",
                          }
        self.assertEqual(bot_events_commands.parse_payload(payload_subtype), {})
        self.assertEqual(bot_events_commands.parse_payload(self.payload), expected_output)

# Compared to iteration 1, additional tests were added and the payload 
# information was simplified to include only the relevant portion for testing.
class TestHandlingWorkspace(unittest.TestCase):
    def setUp(self):
        self.bot_id = "bot_id"
        self.not_bot_id = "not_bot_id"
        self.valid_payload_response = Response(status=200)
        self.invalid_payload_response = Response(status=400)

    # Added for iteration 2 a test function version of 
    # mock_handle_workspace_channels that mocks the responses of the API calls
    # made in the actual handle_workspace_channels function. Allows us to test 
    # the general response logic of the function, handling possible responses 
    # that could happen from doing the API calls. Also calls the actual check_id 
    # function, so the function could be tested from here as well. 
    def mock_handle_workspace_channels(self, channel_rv, join_rv, archive_rv):
        if not channel_rv["ok"]:
            return Response(status=400) 
        if (bot_events_commands.check_id(channel_rv, self.bot_id) == False): 
            if (not join_rv["ok"]):
                return Response(status=400) 
            if (not archive_rv["ok"]):
                return Response(status=400) 
        return Response(status=200)

    def test_workspace_handling(self):
        # https://api.slack.com/types/conversation
        # 'is_channel': "Private channels created before March 2021 (with IDs that begin with G) will return false"
        # Based on this information payload should never have 'is_channel' be 
        # private, as the workspace will be created after March 2021.
        bot_channel_rv = {'ok': True, 
            'channel': {
                'creator': self.bot_id, 'id': 'channel_id', 
                'name': 'name', 'is_channel': True, 
                'is_private': False, 'is_archived': False, 
                'is_general': False, 
            }   
        }
        not_bot_id_channel_rv = {'ok': True, 
            'channel': {
                'creator': self.not_bot_id, 
                'id': 'channel_id', 'name': 'name', 
                'is_channel': True, 'is_private': False, 
                'is_archived': False, 'is_general': False, 
            }
        }
        # Bot never creates general channel because general channel is 
        # automatically created when a workspace is created, which is
        # always done by a human.
        general_channel_rv = {'ok': True, 
            'channel': {
                'creator': self.not_bot_id,  
                'id': 'channel_id', 'name': 'name', 
                'is_channel': True, 'is_private': False, 
                'is_archived': False, 'is_general': True, 
            }
        }
        # Testing API call failure in getting necessary channel information.
        failed_channel_rv = {"ok": False, 'error':'error'}
        actual_response = self.mock_handle_workspace_channels(failed_channel_rv, {}, {})
        self.assertTrue(same_responses(actual_response, self.invalid_payload_response))
        # Case where channel archiving is needed to be done, and is done successfully.
        actual_response = self.mock_handle_workspace_channels(not_bot_id_channel_rv, {'ok': True}, {'ok': True})
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
        # Cases where channel archiving is not needed to be done (general channel, 
        # bot made channel), so nothing is done in that case. 
        actual_response = self.mock_handle_workspace_channels(bot_channel_rv, {}, {})
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
        actual_response = self.mock_handle_workspace_channels(general_channel_rv, {}, {})
        self.assertTrue(same_responses(actual_response, self.valid_payload_response))
        # Case where channel archiving is needed to be done, and is not done successfully. 
        # Also testing API call failure response handling for join_rv and archive_rv. 
        actual_response = self.mock_handle_workspace_channels(not_bot_id_channel_rv, {'ok': False}, {'ok': True})
        self.assertTrue(same_responses(actual_response, self.invalid_payload_response))
        actual_response = self.mock_handle_workspace_channels(not_bot_id_channel_rv, {'ok': True}, {'ok': False})
        self.assertTrue(same_responses(actual_response, self.invalid_payload_response))

class TestCheckingDate(unittest.TestCase):
    def setUp(self):
        self.end_date = date.today().strftime("%m-%d-%Y")
        self.day_after = date.today() + timedelta(days=1)
        self.day_after_str = self.day_after.strftime("%m-%d-%Y")
        self.day_before = date.today() - timedelta(days=1)
        self.day_before_str = self.day_before.strftime("%m-%d-%Y")

    # def create_date_after(self, end_date):
    #     date_after = list(end_date)
    #     day = int(end_date[-2]) * 10 + int(end_date[-1])
    #     day_after = str(day + 1)
    #     date_after[-2] = day_after[0]
    #     date_after[-1] = day_after[1]
    #     return "".join(date_after)

    # def create_date_before(self, end_date):
    #     date_before = list(end_date)
    #     day = int(end_date[-2]) * 10 + int(end_date[-1])
    #     day_before = str(day - 1)
    #     date_before[-2] = day_before[0]
    #     date_before[-1] = day_before[1]
    #     return "".join(date_before)

    def testCheckingDate(self):
        print("TESTING CHECKING DATE\n")
        # after = self.create_date_after(self.end_date)
        # before = self.create_date_before(self.end_date)
        self.assertEqual(bot_events_commands.check_date(self.end_date, "test"), 0)
        self.assertEqual(bot_events_commands.check_date(self.day_before_str, "test"), 1)
        self.assertEqual(bot_events_commands.check_date(self.day_after_str, "test"), -1)


if __name__ == '__main__':
    unittest.main()