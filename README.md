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

### Onboarding Changes (4.B)
1. Fix `test_handle_onboarding()`
-We created a global test_user_id such that in `handle_onboarding()`, the function will detect when the test_user_id is the input and return a custom payload so that no actual call to the API is made. We also added the custom payload that lives in `handle_onboarding()`.

2. Add date input to welcome message
-We added further instruction in the welcome message to accomodate for the change in the slash command where the end date will follow the class name

### Onboarding Test Changes (4.B)
- Added `test_user_id` for testing function that need to make API calls but can't due to Slack's limitations thus acts as a switch for returning custom payloads in the functions instead of making the API calls
- Changed `new_class` and `existing_class` names as they were causing duplicate errors in our workspace  
- Reduced payload complexity in a couple instances

### Acceptance Testing
Within the workspace:
- Execute the command `/join_class cmsc-22002 12-11-22` to be added to an already existing class channel.
- Execute the command `/join_class bios-12345 03-12-24` to be added to a non-existing class channel.

# ITER2 - Activity Warnings, Conversation Summary, and Mood Messages - Matt and Maya G
## Activity Warnings
The iteration finalized the activity warnings feature. 
This encompasses the following<br>
1. Scheduling messages to send
2. Firebase support for multiple channels <br>
Unit tests for both of these features have been added. However, there are 
some practical issues with testing scheduling that make it difficult to test (i.e.
making sure the functions are called at the right times). Thus, we are just 
testing the functionality of the functions called by the scheduler. <br>
## Conversation Summary
Conversation summary is a new feature that is a response to a slash command 
`/summarize_conversation` which summarizes the conversation in the past 6 
hrs. Because the conversation summary will differ each time due to NLP, our two
test cases check if there are 0 msgs in the past 6 hrs, or if there are >0 msgs,
and test the correct behavior for each case<br>
Note that we plan to extend this feature to allow for an aribtrary amount of 
time as opposed to fixed 6 hour conversation history period
## Mood Messages
This iteration finalized the mood messages feature
This encompasses the following<br>
1. Making sure send message is only implemented when the mood is negative
2. Scheduling messages to send
3. Firebase support for multiple channels <br>
Unit tests for all three of these features have been added. However, there are 
some practical issues with testing scheduling that make it difficult to test (i.e.
making sure the functions are called at the right times). Thus, we are just 
testing the functionality of the functions called by the scheduler. <br>
## Testing Notes
### Unit Tests
Unit tests for each function and possible unit interactions are in place
### Acceptance Testing
Acceptance tests for activity & mood have been put in place, which walk through
different possible command calls by users and ensures that variables and command
outputs are correct
## To-fix and Final Implementations for Assgn 5
Minor bug in mood messages test cases<br>
Add support for variable time for convo summary<br>
Finalize scheduling integration
