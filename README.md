# Testing

In order to run the tests for this branch:

1. cd into the slackbot directory 
2. Place the `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` inside the slackbot directory before running the tests
3. Run `pip install -r requirements.txt` to install the necessary requirements
4. Run the tests using the commands below:

`python -m unittest discover`

or 

`python3 -m unittest discover`

## Changes from Iteration 1 (Milestone 4A)

Main outlined features were implemented, with the following function changes. 
- Began the process of integrating the project files by setting up or making the function calls outside of bot_events_commands.py, when handling slash commands and message events.
- Modified the current process for bot monitoring of workspace channels, through manually looking for a channel creation event. This served an alternative solution to what we previously designed, due to live testing issues we ran into. 
- Removed compute_time_format function in the bot_events_command file since other files handled that feature's intent.
- Set up the implementation for the feature of archiving a channel at a requested date.

Testing changes:
- Added more tests for test_check_valid_slash_command_payload, test_is_time_format_valid, test_invalid_handle_join_class_invocation, and test_check_valid_slash_command_payload. 
- Modified TestHandlingWorkspace structure by testing a mock version of handle_workspace_channels and check_id.
- Removed compute_time_format tests 
- Wrote testing for the archiving a channel at a requested date feature. 

# Handling Events and Slash Commands Feature (Iteration 1) - Sanzhar and Michael

Compared to the iteration 1 design document, we largely followed the functions outlined in the handling slash command and events feature. We fleshed out the handle_slash_command function more, by having the function branch off into intermediate handling functions, for slash commands that require parameters. The idea is handle_slash_command is the first function called whenever a slash command is invoked. From there is directly handles calling the slash command implementation functions written in the other features, for slash commands that do not have parameters. We also thought that handle_slash_command should also handle defective payload information, since we are relying on Slack to provide us non-malformed data in their POST requests.

For handle_message_event we created 2 helper functions that check if the payload is valid (has all the required fields) and the other one that parses the payload and returns a dictionary with only the useful information, that is later passed on to functions from other features. We test both helper functions in test.py. For handle_workspace_channels we created a helper function that checks if the new channel that was created was created by the bot or by a person user. In the latter case, the bot would delete the channel by making a relevant API call. For now, we just test the functionality of check_id in test.py. 

These tests are unit tests for the "Command Handling" functionality of the Slack Bot. This includes the following functions:
```
- check_valid_event_payload(payload, team_id, token)
- check_valid_slash_command_payload(payload, team_id, token)
- parse_payload(payload)
- check_id(payload, bot_id)
- handle_disable_activity_warnings_invocation(payload)
- handle_set_activity_warning_threshold_invocation(payload)
- handle_disable_mood_messages_invocation(payload)
- handle_join_class_invocation(payload)
- handle_meetup_invocation(payload)
- is_time_format_valid
- handle_slash_command()
```
