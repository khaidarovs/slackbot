# Testing 
In order to run the tests for this branch: 
1. cd into the slackbot directory.
2. Place the .env file, `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` and `slackbot-software-firebase-adminsdk-xxfr0-f706556aac.json` files inside the slackbot directory before running the tests.
3. Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt`to install the necessary requirements.
4. Run the tests using the commands below: `python -m unittest discover` or `python3 -m unittest discover`.

# Onboarding (Sabine and Grace)
Every user should get a welcome message upon joining the workspace.
**Important:** When executing commands, enter them in the #general channel. 

## Joining a class
To join a class, do `/join_class SUBJ-##### MM-DD-YYYY`
- `SUBJ` is the four letter code for the class department (e.g. "CMSC", "SPAN")
- `#####` is the 5 digit code for the class (e.g. `22001`, `10100`)
- `MM-DD-YYYY` is the end date for the class in month-day-year format.

### Examples to try:
- `/join_class cmsc-27002 03-12-2022` should add you to the class channel for CMSC 27002, with a success message in #general.
- `/join_class kReY-10300 05-28-2030` should add you to the class channel for KREY 10300.
- `/join_class PHYS-14300 11-01-2059` should add you to the class channel for PHYS 14300.

To explore error handling:
- `/join_class SPAN-20200 12-02-1980` should give you an error message requesting a date in the future.
- Try entering fewer than two parameters to `/join_class` to get an error on how to properly use the command.

## Limitations
- Currently, StudyRoom doesn't support joining channels for classes that have ended (i.e., classes whose channels have been archived). If a class ends and you try to execute the `/join_class` command with its class code, you'll get an error.
- The structure of channels is based on UChicago's class naming system; classes not in this format will not be recognized.

## Implementation Details (onboarding.py):
- `welcome_new_user(payload)`: Instructs the user on how to join a class when they first join the workspace. Returns a Slack API generated success message on success, and False otherwise.
- `handle_onboarding(class_name, user_id)`: Adds the given student to the given class channel, creating the channel if it doesn't already exist. Returns an object with the channel information on success, and a Slack API generated error otherwise.
- `check_channels(class_name)`: Verifies whether a class channel exists within the workspace, returning True if it does and False otherwise.
- `normalize_channel_name(channel_name)`: Converts the name of a class channel (in the format XXXX-#####) to the proper slack format (includes only lowercase letters, numbers, and a hyphen)
- `get_channel_name(channel_id)`: Returns the name of the channel with the given channel ID, or none if the channel doesn't exist.
- `get_channel_id(name_normalized)`: Returns the ID of the channel with the given name.
- `send_im_message(userid, text)`: Sends a direct message to the user with the given user id.

# Handling Events and Slash Commands Feature (Iteration 2) - Sanzhar and Michael 

# Live Testing 
1. Run `python bot_events_commands.py` or `python3 bot_events_commands.py` to run the events file. 
2. After running the command you can find the port number in terminal (ie. "Running on http://127.0.0.1:<port number>"). 
3. Have ngrok in the folder of the program and run the command "ngrok http <port number>" in the ngrok application.
4. Go to the forwarding tab and copy the generated ngrok link. 
5. In the Slack developer workspace console for "StudyRoom UChicago" (which you should have already been added as a collaborator), go to the Event Subscriptions tab and go to the Enable Events section. Input the ngrok link and then add the "/slack/events" endpoint at the end of that ngrok link. The link should be verified and work from there. 
6. For slash commands head to each one of interest under the Slash Commands section of the developer workspace console, and add the "/slash-command" endpoint at the end of the ngrok link as well. Currently though slash commands aren't set up for acceptance tests at the moment, but for future live testing this would apply. 

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
- In the workspace, head to "Add Channel" -> "Create new channel". Name the channel and leave it public. Since the channel was not created by the bot, you should see that the channel was not even created. To verify, go to "unread messages" from SlackBot, which should say that the bot has archived your channel. NOTE: the acceptance test for the slash commands may be currently impacted by this, since there is a chronological process that occurs with channel creation through onboarding onto classes, and eventually deleting said courses. 

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
- Finish integrating the code with the other features
- Fix minor database bugs
- General refactoring with other features (ie. centralizing the time format code under a single file)

# Meetup Feature - Maya Hall and Jason Huang:
- `meetup`, adds a log to the database with the meeting timestamp, location, message. You can enter a time in the form of "XsXmXhXd" where X are different integers. Meetup converts string explaination of a time to seconds.
- `wait_message`, will stores a combination of a location, a message, and a time as a varaible into a database.
- `in_five`, checks whether any events in the database occurs within the next five minutes. If so, a message will be sent after a delay. This command will automatically be called every five minutes while the bot is active. This command is currently no longer needed.

## Meetup Test Changes
- We realized that the previous tests for `in_five` pulled data from the wrong location. The test have been adjusted to pull information from the correct location designated in our code.

## Future Plans
- We plan to change the storage method to Firebase in the near future.
- Additionally, we intend to add alternate formats/features for meet times and include reminders for further versitility.

### Onboarding Test Changes (4.A)
- Firebase implimentation provides a more consistent and secure database. Test cases have been adjusted to match the new storage method.
- Development cycle slightly slowed this iteration due to developer sickness. We have yet to impliment a date-time system consistent throughout the project.

## Future Plans
- We plan to add a function that automatically calls the `in_five` function at set intervals, activated after bot becomes online.
- Create a standard date-time system for the bot.
- If time permits, reactions can bping attendees for each meeting.

## Scheduling Adjustment
- Due to how `in_five` was changed in implimentation, so that reminders are set to a future date instead of being actively updated, the command was rendered obsolete.

### Examples to try:
- `/meetup 5m3s` This will create a reminder in 5 minutes 3 seconds from the current time.
- `/meetup 5m3s, Zoom` This will also create a reminder in the same time, but specify the location as Zoom.

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
1. Making sure send_message is only implemented when the mood is negative. For usability purposes, we are not sending a message when the NLP model classifies a message as positive or neutral. This has a tradeoff: It might be helpful to know what the NLP model is predicting the mood to be in a case where the NLP mood prediction is different from what the user intended it to be. This being said, the Sentiment Analyzer model in python's NLTK package is proven to have a high accuracy (90%+ on testing sets). 
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
