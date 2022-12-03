# Testing 
In order to run the tests for this branch: 
1. cd into the slackbot directory.
2. Place the .env file, `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` and `slackbot-software-firebase-adminsdk-xxfr0-f706556aac.json` files inside the slackbot directory before running the tests.
3. Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt`to install the necessary requirements.
4. Run the tests using the commands below: `python -m unittest discover` or `python3 -m unittest discover`.

# Installation Guide

Use the following link to join our workspace: 
```
https://join.slack.com/t/studyroomuchicago/shared_invite/zt-1kt9yjwxs-Rj_elYqVJ8XPn3qthricnw
```

Once you join the workspace, use the slash commands and acceptance tests outlined below to test the functionality of our bot. The slash commands are broken into 4 functionality categories: onboarding, meetup, activity warnings & mood messages, general & channel archiving. Please refer to each section below to find more details on how to use the slash commands and potential acceptance tests you could run.  

# The complete set of slash commands available in the workspace:![image](https://user-images.githubusercontent.com/93730296/205425766-e6121c18-94e7-4b56-a356-e9899405ab72.png)

## Onboarding:

- `/join_class SUBJ-##### MM-DD-YYYY`

## Meetup:

- `/meetup <time from now>, <location (optional)>`

## Activity warnings, Mood messages & Conversation Summary:

- `/enable_activity_warnings`
- `/disable_activity_warnings <downtime (optional)>` 
- `/set_activity_warning_threshold <number of messages>`
- `/set_activity_warning_content <content (optional)>`
- `/set_mood_message_content <content (optional)>`
- `/enable_mood_messages`
- `/disable_mood_messages <downtime (optional)>`
- `/summarize_conversation`
- `/trigger_activity_warning`

General & Archiving a channel:

- `/vote_archive <Y or N>`
- `/help`
- `/trigger_voting`
- `/trigger_check_vote_results`
	
A more detailed explanation of the commands, as well as examples of potential acceptance tests can be found below. 

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

- `/help` – use this slash command to get information about the bot as well as the available slash commands and functionality

## Archiving a channel:

There are two ways you could test this feature:
1. Follow the “Joining a class” logic outlined in the Onboarding section and set the end date to tomorrow (e.g., if you are testing on 12-3-2022, set it to 12-4-2022). At midnight on the end date, a poll message will be sent asking the users to vote in the channel using the `/vote_archive` slash command. Use examples: `/vote_archive Y` & `/vote_archive N`. At midnight of the next day, the bot will count up the votes and will archive the channel if more than half of the users voted Y.

2. For testing purposes we created a process that doesn’t require you to wait a whole day to test this functionality. Follow the “Joining a class” logic outlined in the Onboarding section and set the end date to today (e.g., if you are testing on 12-3-2022, set it to 12-3-2022). Use the slash command `/trigger_voting` (without any parameters), which will trigger the bot to send a message to the channel asking users to vote for or against archiving the channel. Use `/vote_archive` to vote. Use examples: `/vote_archive Y` & `/vote_archive N`. When all the users in the channel are done voting, use `/trigger_check_vote_results` to trigger the bot to count up the votes and make a decision – it will archive the channel if more than half of the users voted Y.

### Examples to try:
-	Create a channel with 3 people (3 people should join it using the `/join_class` command) and set the end date to the date when you are testing it. Use `/trigger_voting` to send the poll message. Don’t vote and then use `/trigger_check_vote_results` – you should see that nothing happens to the channel.
-	Do the same setup as in the example above, but this time 2 or more people should vote Y using the `/vote_archive` command. If you run `/trigger_check_vote_results` you should find that the bot archived the channel, which you should be notified about by the SlackBot bot. 

### Limitations:
-	If new people are added to the channel after the poll message has been sent, their votes will not be counted 

### Additional acceptance tests:
-	Our bot doesn’t allow users to create public channels. Test it by creating a public channel ("Add Channel" -> "Create new channel" in the workspace) – the bot should archive the channel immediately and you should be notified of it by the SlackBot Bot

### To explore error handling:
-	Try voting something other than Y or N using `/vote_archive`. It should return an error message
-	Using the first scenario outlined above, on the day before the end date try using the command `/vote_archive Y`. It should return an error stating that the voting hasn’t started yet. Note: there’s a minor string mistake – it should say: "Sorry! The voting period for voting to archive the channel has not started yet.", but it says currently “"Sorry! The voting period for voting to archive the channel has passed.".

### Implementation Details:

- `check_valid_event_payload(payload, team_id, token)`
- `check_valid_slash_command_payload(payload, team_id, token)`
- `parse_payload(payload)`
- `handle_message_event(payload)`
- `handle_workspace_channels(payload)`
- `check_id(payload, bot_id)`
- `handle_slash_command()`
- `handle_vote(payload)`
- `handle_disable_activity_warnings_invocation(payload)`
- `handle_set_activity_warning_threshold_invocation(payload)`
- `handle_disable_mood_messages_invocation(payload)`
- `handle_join_class_invocation(payload)`
- `handle_meetup_invocation(payload)`
- `is_time_format_valid`
- `check_date(end_date)`
- `send_poll_msg(channel_id, text)`
- `check_poll_results(channel_id)`
- `archive_channel(channel_id)`
- `check_channels ()`
- `do_channel_check()`

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
