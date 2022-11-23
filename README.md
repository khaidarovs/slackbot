# Testing

In order to run the tests for this branch:

1. cd into the slackbot directory 
2. Place the `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` inside the slackbot directory before running the tests
3. Run `pip install -r requirements.txt` to install the necessary requirements
4. Run the tests using the commands below:

`python -m unittest discover`

or 

`python3 -m unittest discover`

# Handling Events and Slash Commands Feature (Iteration 2) - Sanzhar and Michael

## Functionality:
```
- check_valid_event_payload(payload, team_id, token)
- check_valid_slash_command_payload(payload, team_id, token)
- parse_payload(payload)
- handle_message_event(payload)
- handle_workspace_channels(payload)
- check_id(payload, bot_id)
- handle_disable_activity_warnings_invocation(payload)
- handle_set_activity_warning_threshold_invocation(payload)
- handle_disable_mood_messages_invocation(payload)
- handle_join_class_invocation(payload)
- handle_meetup_invocation(payload)
- is_time_format_valid
- handle_slash_command()
New Functionality (4.B)
- check_date(end_date)
- send_poll_msg(channel_id, text)
- check_poll_results(channel_id)
- archive_channel(channel_id)
- check_channels_end_dates()
```

## Handle Events Changes (4.B)
Added the functionality for storing the class end date in Firebase, and then checking if today is that date every 24h. In case today is that date, we send out a poll into the channel where users vote "Y" or "N" in favor of archiving the channel. The next day we make a decision based on the number of votes. 

## Handle Events Test Changes (4.B)
We updated the tests for check_date as well as a few minor updates to other tests. You can find more details about other changes below.

## Acceptance Testing
- In the workspace, head to "Add Channel" -> "Create new channel". Name the channel and leave it public. Since the channel was not created by the bot, you should see that the channel was not even created. To verify, go to "unread messages" from SlackBot, which should say that the bot has archived your channel.

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

## Things to do
- Fix potential bugs related to parsing different types of payloads
- Finish integrating the code 
- Fix minor database bugs
