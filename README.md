# slackbot

## Running Tests
Run `python unittest -m discover` in the main directory to run all the tests.

## Onboarding
The initial tests revealed better ways to structure the onboarding process, so we restructured our approach to center around three main functions:
- `welcome_new_user()`, which instructs the user on how to join a class
- `handle_onboarding(string class_name)`, which handles the process of creating new channels and adding users
- `check_channels(string class_name)`, a helper to `handle_onboarding()` that checks if a class channel already exists.

We also decided to let the bot automatically handle the creation of classes, rather than prompting the user to do so.
