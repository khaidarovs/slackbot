# Handling Events and Slash Commands Feature - Sanzhar and Michael

Compared to the iteration 1 design document, we largely followed the functions outlined in the handling slash command and events feature. We fleshed out the handle_slash_command function more, by having the function branch off into intermediate handling functions, for slash commands that require parameters. The idea is handle_slash_command is the first function called whenever a slash command is invoked. From there is directly handles calling the slash command implementation functions written in the other features, for slash commands that do not have parameters. We also thought that handle_slash_command should also handle defective payload information, since we are relying on Slack to provide us non-malformed data in their POST requests.

For handle_message_event we created 2 helper functions that check if the payload is valid (has all the required fields) and the other one that parses the payload and returns a dictionary with only the useful information, that is later passed on to functions from other features. We test both helper functions in test.py. For handle_workspace_channels we created a helper function that checks if the new channel that was created was created by the bot or by a person user. In the latter case, the bot would delete the channel by making a relevant API call. For now, we just test the functionality of check_id in test.py. 

These tests are unit tests for the "Command Handling" functionality of the Slack Bot. This includes the following functions:
```
- check_valid_event_payload(payload)
- check_valid_slash_command_payload(payload)
- parse_payload(payload, bot_id)
- check_id(payload, bot_id)
- handle_disable_activity_warnings_invocation(payload)
- handle_set_activity_warning_threshold_invocation(payload)
- handle_disable_mood_messages_invocation(payload)
- handle_join_class_invocation(payload)
- handle_meetup_invocation(payload)
- is_time_format_valid
- handle_slash_command()
```

## Changes from Milestone 3A

Main outlined features were implemented, with the following function changes. 
- Removed handle_set_activity_warning_content_invocation(payload) function since we decided the slash command text didn't need any special parsing.
- check_valid_payload became check_valid_event_payload and check_valid_slash_command_payload(payload) since we found the event and slash command JSON payloads slightly differed in structure.
Currently a .env file containing the necessary token information for a given workspace is needed in order to live test the bot, along with the creation of a slack workspace as well. 