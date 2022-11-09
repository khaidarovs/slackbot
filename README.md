# Testing

In order to run the tests:

1. cd into the slackbot directory 
2. Place the `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca` inside the slackbot directory before running the tests


`python -m unittest discover`

or 

`python3 -m unittest discover`

Each feature is described in more detail below

# Handling Events and Slash Commands Feature - Sanzhar and Michael

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

## Changes from Milestone 3A

Main outlined features were implemented, with the following function changes. 
- Removed handle_set_activity_warning_content_invocation(payload) function since we decided the slash command text didn't need any special parsing.
- check_valid_payload became check_valid_event_payload and check_valid_slash_command_payload(payload) since we found the event and slash command JSON payloads slightly differed in structure. Both functions now require token and team_id as parameters, which are obtained by using auth.test API call. 
- parse_payload. doesn't require a bot_id as an argument anymore
Currently a .env file containing the necessary token information for a given workspace is needed in order to live test the bot, along with the creation of a slack workspace as well. 

Testing changes:
- The message and channel_created payloads were extended to contain all the information an actual payload would


# Meetup Feature - Maya Hall and Jason Huang:
- `meetup`, adds a log to the database with the meeting timestamp, location, message. You can enter a time in the form of "XsXmXhXd" where X are different integers. Meetup converts string explaination of a time to seconds.
- `wait_message`, will stores a combination of a location, a message, and a time as a varaible into a database.
- `in_five`, checks whether any events in the database occurs within the next five minutes. If so, a message will be sent after a delay. This command will automatically be called every five minutes while the bot is active.

## Meetup Test Changes
- We realized that the previous tests for `in_five` pulled data from the wrong location. The test have been adjusted to pull information from the correct location designated in our code.

## Future Plans
- We plan to change the storage method to Firebase in the near future.
- Additionally, we intend to add alternate formats/features for meet times and include reminders for further versitility.

# Onboarding (Sabine and Grace)
Functionality:
- `welcome_new_user(payload)`: Instructs the user on how to join a class when they first join the workspace. Returns a Slack API generated success message on success, and False otherwise.
- `handle_onboarding(class_name, user_id)`: Adds the given student to the given class channel, creating the channel if it doesn't already exist. Returns an object with the channel information on success, and a Slack API generated error otherwise.
- `check_channels(class_name)`: Verifies whether a class channel exists within the workspace, returning True if it does and False otherwise.

### Onboarding Test Changes (3.B)
We realized that the tests utilize events operating in the workspace we created; thus, we had to revamp them a bit to get them to work properly.

`test_welcome_new_user()`:
- We realized that the previous tests for `welcome_new_user()` wouldn't have worked, so we created a helper function to simulate different payloads, and used this to simulate a user joining a non-general and general channel.

`test_handle_onboarding()`:
- Instead of trying to fake a payload for the new and existing channels, we use the Slack API to create channels in the workspace, verify if a channel does/doesn't exist, and test whether or not a user is properly added to a channel. We also make use of the Slack API to remove users from channels prior to running the tests, to avoid unpredictable behavior.

`test_check_channel()`:
- We moved the code for creating the existing channel into the setUp() function, since multiple test make use of that class.

# Activity Warning Branch - Matt and Maya G
### Running the tests
First, run the bot to set up connection to the Firebase DB<br />
    `python bot.py`<br />
To run the tests, use the following command:<br />
    `python -m unittest discover`<br />
*Note:* 
Running the bot requires access to the .env file and Firebase DB, which 
contain sensitive information and cannot be posted on GitHub.
Contact a SlackBot dev if you do not have these files.<br />

### Functions tested
These tests are unit tests for the *"Activity Warnings"* functionality of the 
Slack Bot. This includes the following functions:<br />
 - `enable_activity_warnings()`<br />
 - `disable_activity_warnings()`<br />
 - `set_activity_warnings_threshold()`<br />
 - `set_activity_warnings_content()`<br />
 - `check_activity()`<br />
 - `send_activity_warning()` <br />

## Functions tested
These tests are unit tests for the *"Mood Messages"* functionality of the Slack Bot. This includes the following functions:<br />
 - `enable_mood_messages()`<br />
 - `disable_mood_messages()`<br />
 - `set_mood_messages_content`<br />
 - `check_mood()`<br />
 - `send_mood_message()` <br />
 - 
 ### Notes
 Currently, the Activity Warnings and Mood Messages feature only can be run in one place at a time,
 as the Firebase DB has not been fully configured to handle multiple channels and 
 servers. This will be fixed in a future sprint.<br /><br />
 Currently, Activity Warnings and Mood Messages scheduled sending has not been implemented in iteration
 1 but will be implemented in iteration 2. The code in this iteration is foundational
 for checking activity; i.e. a function that gets the last N messages, and a function
 that actually sends the activity message. Scheduled sending and the simple
 integer comparison between (N_Messages in last 24 hrs) and (Threshold) have yet 
 to be implemented. :)
