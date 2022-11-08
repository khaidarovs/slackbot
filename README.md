# slackbot

## Running Tests
Run `python unittest -m discover` in the main directory to run all the tests.
To run specific tests, run `python -m unittest -k test_name` (e.g. `python -m unittest -k test_welcome_new_user`).

## Onboarding (3.A)
The initial tests revealed better ways to structure the onboarding process, so we restructured our approach to center around three main functions:
- `welcome_new_user()`, which instructs the user on how to join a class
- `handle_onboarding(string class_name)`, which handles the process of creating new channels and adding users
- `check_channels(string class_name)`, a helper to `handle_onboarding()` that checks if a class channel already exists.

We also decided to let the bot automatically handle the creation of classes, rather than prompting the user to do so.

## Onboarding Test Changes (3.B)
We realized that the tests utilize events operating in the workspace we created; thus, we had to revamp them a bit to get them to work properly.
`test_welcome_new_user()`:
- We realized that the previous tests for `welcome_new_user()` wouldn't have worked, so we created a helper function to simulate different payloads, and used this to simulate a user joining a non-general and general channel.

`test_handle_onboarding()`:
- Instead of trying to fake a payload for the new and existing channels, we use the Slack API to create channels in the workspace, verify if a channel does/doesn't exist, and test whether or not a user is properly added to a channel. We also make use of the Slack API to remove users from channels prior to running the tests, to avoid unpredictable behavior.

`test_check_channel()`:
- We moved the code for creating the existing channel into the setUp() function, since multiple test make use of that class.
