# Testing

In order to run the tests:

1. cd into the slackbot directory 
2. Place the `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` inside the slackbot directory before running the tests
3. Run `pip install -r requirements.txt` to install the necessary requirements
4. Run the tests using the commands below:

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
- `normalize_channel_name(channel_name)`: Converts the name of a class channel (in the format XXXX-#####) to the proper slack format (includes only lowercase letters, numbers, and a hyphen)
- `get_channel_name(channel_id)`: Returns the name of the channel with the given channel ID, or none if the channel doesn't exist.
- `get_channel_id(name_normalized)`: Returns the ID of the channel with the given name.
- `send_im_message(userid, text)`: Sends a direct message to the user with the given user id.

### Onboarding Iteration 2 Plan (4.a)
1. Fix `test_handle_onboarding()`
-We discovered that these tests require a user to be active in the workspace and we plan to find a workaround for this so that the tests for `handle_onboarding()` can run without the active user requirement. We will be creating fake users and passing those users to our tests that don't interact with the API. 

2. Ask for class end date
-We plan to implement part of another feature which will ask for the user to input a class's end date. This will allow the bot to archive and/or delete the channel when the class is over. 

3. Integrate with slash command
-We will have to integrate our code with what the slash command group have written so that when a user inputs a slash command to add/join a class, our functions will be called. 

In this upcoming iteration, we plan on revising our previous tests to ensure they can run under any conditions, and collecting data needed to archive a class channel once the class ends.

### Onboarding Test Changes (4.A)
We added additional tests for helpers that we implemented in the previous iteration, including:
- `normalize_channel_name(string channel_name)`, which ensures that class channels have all lowercase class codes
- `get_channel_name(string channel_id)`, which returns the name of a channel given its id
- `get_channel_id(string name_normalized)`, which returns the id of a channel given its name
- `send_im_message(string userid, string test)`, which sends a direct message to a specific user

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
