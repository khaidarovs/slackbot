# Testing 
In order to run the unit tests for our bot: 
1. git clone the repo. 
2. cd into the slackbot directory.
3. Place the `.env` file, `slackbot-v1-firebase-adminsdk-n7ggn-fcdad3e5ca.json` and `slackbot-software-firebase-adminsdk-xxfr0-f706556aac.json` files inside the slackbot directory before running the tests.
4. Run `pip install -r requirements.txt` or `pip3 install -r requirements.txt` to install the necessary requirements.
5. Run the tests using the commands below: `python -m unittest discover` or `python3 -m unittest discover`.

# Installation Guide

Use the following link to join our workspace: 
```
https://join.slack.com/t/studyroomuchicago/shared_invite/zt-1kt9yjwxs-Rj_elYqVJ8XPn3qthricnw
```

Once you join the workspace, use the slash commands and acceptance tests outlined below to test the functionality of our bot. The slash commands are broken into 4 functionality categories: onboarding, meetup, activity warnings & mood messages, general & channel archiving. Please refer to each section below to find more details on how to use the slash commands and potential acceptance tests you could run.  

# The complete set of slash commands available in the workspace:
Note that many of these slash commands use Slack API calls, which have rate limiting in place to prevent too many calls being made in a short amount of time. As a result, try not to spam inputting the slash command all at once, as it may temporarily crash the bot (this would be seen via operation dispatch errors). In the case that happens, you would need to wait for a few minutes for the commands to be working again.  

## Onboarding:

- `/join_class <four letter department code>-<five digit course code> <MM-DD-YYYY>`

## Meetup:

- `/meetup <time from now>, <location (optional)>`

## Activity warnings, Mood messages & Conversation Summary:

- `/enable_activity_warnings`
- `/disable_activity_warnings <downtime (optional)>` 
- `/set_activity_warning_threshold <threshold (optional)>`
- `/set_activity_warning_content <content (optional)>`
- `/set_mood_message_content <content (optional)>`
- `/enable_mood_messages`
- `/disable_mood_messages <downtime (optional)>`
- `/summarize_conversation`
- `/trigger_activity_warning`

## General & Archiving a channel:

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
- If you run in a joining an archived channel error text, that means the requested class has already been archived. Try to type another class name instead.

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

# General & Archiving a Channel (Handling Events and Slash Commands Feature) - Sanzhar and Michael 

- `/help` – use this slash command to get information about the bot as well as the available slash commands and functionality

## Archiving a channel:

There are two ways you could test this feature:
1. Follow the “Joining a class” logic outlined in the Onboarding section and set the end date to tomorrow (e.g., if you are testing on 12-3-2022, set it to 12-4-2022). At midnight on the end date, a poll message will be sent asking the users to vote in the channel using the `/vote_archive` slash command. Use examples: `/vote_archive Y` & `/vote_archive N`. At midnight of the next day, the bot will count up the votes and will archive the channel if more than half of the users voted Y.

2. For testing purposes we created a process that doesn’t require you to wait a whole day to test this functionality. Follow the “Joining a class” logic outlined in the Onboarding section and set the end date to today (e.g., if you are testing on 12-3-2022, set it to 12-3-2022). Use the slash command `/trigger_voting` (without any parameters), which will trigger the bot to send a message to the channel asking users to vote for or against archiving the channel. Use `/vote_archive` to vote. Use examples: `/vote_archive Y` & `/vote_archive N`. When all the users in the channel are done voting, use `/trigger_check_vote_results` to trigger the bot to count up the votes and make a decision – it will archive the channel if more than half of the users voted Y.

### Examples to try:
-	Create a channel with 3 people (3 people should join it using the `/join_class` command) and set the end date to the date when you are testing it. Use `/trigger_voting` to send the poll message. Don’t vote and then use `/trigger_check_vote_results` – you should see that nothing happens to the channel.
-	Do the same setup as in the example above, but this time 2 or more people should vote Y using the `/vote_archive` command. If you run `/trigger_check_vote_results` you should find that the bot archived the channel, which you should be notified about by the SlackBot bot. 

### Limitations:
-	If new people are added to the channel after the poll message has been sent, their votes will not be counted.

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

## Creating a meetup
To create a meetup, do `/meetup #s#m#h#d, <location (optional)>`. This will create a reminder after a specified amount of time. The "s" "m" "h" and "d" are acceptable modifiers for second, minute, hour, and day respectively. If no specific letter is used, minutes is assumed by default. Location adds an optional tag, that will be included in the reminder message.

## Examples to try:
- `/meetup 5m3s` This will create a reminder in 5 minutes 3 seconds from the current time.
- `/meetup 5m3s, Zoom` This will also create a reminder in the same time, but specify the location as Zoom.
- `/meetup 10m, https://uchicago.zoom.us/j/20816624750?pwd=ZzNjZllJZkMwclBVZHpZNW8ycThrUT09` - this will create a meetup at the specified Zoom link in 10 minutes.

## Implementation Details
- `meetup(payload)`- Adds a log to the database with the meeting timestamp, location, message. You can enter a time in the form of "XsXmXhXd" where X are different integers. Meetup converts string explaination of a time to seconds.
- `handle_message_scheduling(message, channel_id, location, ts)` - This is an internal function that takes in a message, destination channel, location string, and a timestamp and sends the reminder message at the destination channel at a specified time. Additionally, the data of the reminder is stored in a Firebase database.
- `in_five` - This is an internal function that checks whether any events in the database occurs within the next five minutes. If so, a message will be sent after a delay. This command will automatically be called every five minutes while the bot is active. This command is currently no longer needed due to a change in how messages are scheduled.

## Limitations
- Currently there is no method to edit a set meetup after it has been made, although data for all meetups is recorded in Firebase. Additionally, once a meetup's information has been added to Firebase, there isn't a method for removing it. In the long run, this may cause storage issues, but given the scope and size of the bot, this should not be an issue.

# Activity warnings, Mood messages & Conversation Summary (Matt & Maya G.): 

The activity warnings and mood messages warnings features (done by Matt and Maya G.), have similar commands and functionality but serve different purposes. Specifically, both have enable and disable commands, and the disable commands can be specified for indefinite or definite timeframes. Both features can set message content, and can reset them to default. Activity warnings additionally have a feature which sets the threshold, determining whether an activity warning should be sent.

At midnight, a function checks whether an activity message should be sent or not. Further, we can force-trigger this with a slash command.

On the other hand, mood messages need not be force-triggered with a slash command as they are instantaneous. Once mood messages are enabled in a certain channel using the slash command, the mood of every message sent to the channel thereafter is analyzed using the Sentiment Analyzer model from the NLTK python package. In the case where the mood is negative, a message is sent to the channel encouraging positive chat. But in the case where the mood is either positive or neutral, no message is sent for usability purposes. Note: The only tradeoff here is that it might be useful for the user to know what the model is predicting the mood as in the case where the user’s intended mood doesn’t match the predicted mood, but given the high accuracy of the model, this scenario is unlikely.

The functions are as follows:
- `/enable_activity_warnings` - enables activity warnings indefinitely
- `/disable_activity_warnings <downtime (optional)>` - disables activity warnings for a specified downtime, if none, then indefinite
- `/set_activity_warning_threshold <threshold (optional)>` - sets threshold, if none, then reverts to default
- `/set_activity_warning_content <content (optional)>` - sets content, if none, then reverts to default
- `/set_mood_message_content <content (optional)>` - sets content, if none, then reverts to default
- `/enable_mood_messages` - enables mood messages
- `/disable_mood_messages <downtime (optional)>`- disables mood messages for a specified downtime, if none, then indefinite
- `/trigger_activity_warning` - manually triggers the usual-daily activity warning

Note: manually triggering activity warnings when they are disabled for a definite specified period of time decrements the downtime by 1 day. This is because, conventionally, activity warnings only are triggered daily. However for debugging purposes this is too long to wait.

Finally, all of the variables mentioned above for activity warnings and mood messages are stored in firebase. Specifically, firebase has a separate entry for each channel that stores bool activity_warnings_enabled, int activity_warning_threshold, etc, allowing for multi-channel support. These variables are updated in real time and fetched from the database when needed.

## Convo Summary

Conversation summary feature (done by Matt and Maya G.): Conversation summary is a triggered slash command that uses the NLTK python package and tokenization to process given messages in the past 6 hours and summarize them. Since this function assigns a value to each sentence, there may be a case where there is no significant value associated with specific messages, in which case, the function would return every message from the past 6 hours. 

The function is:
- `/summarize_conversation` - summarizes a conversation

## Use Examples

(ACTIVITY)
- `/enable_activity_warnings` - enables activity warnings indefinitely. User will be informed of current threshold
- `/set_activity_warning_threshold 10` - sets threshold to 10 and informs user
- `/trigger_activity_warning` - if number of messages in channel is less than 10 in the last 24hr, then send activity warning
- `/disable_activity_warnings 1d` - disables activity warnings for 1d
- `/trigger_activity_warning` - will decrement downtime
- `/trigger_activity_warning` - will notice that downtime is 0d, reenabling activity warnings, and sending the activity warning message if number of messages in channel is less than 10 in the last 24hr
- `/disable_activity_warnings` - disables activity warnings indefinitely

(MOOD)
- `/enable_mood_messages` - enables mood messages indefinitely. 
> user sends message to the channel, and if it is negative, the bot will send a message encouraging positive chat. 
- `/enable_mood_messages` - disables mood messages indefinitely. 

(CONVO)
> user uploads their notes on class today
- `/summarize_conversation` - summarizes the notes in fewer sentences
