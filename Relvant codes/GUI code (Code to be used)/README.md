# Welcome to the Finished py code

This code essencialy has 3 jobs:
- It talks to the arduino
- It displays data and options to the user through a GUI using pysimplegui
- And finally it allows control and programming of the greenhouse.

You can use this program stanalone or feed it a scenario to automaticly control the greenhouse 24/7


High level explenation of the program:
After setting some variables and most importantly shaping the GUI the program runs in an infinite loop.
The loop waits until it gets an event from the user (button press) or untill timeout and then it interprets the data.
It calls functions when needed and somtimes even opens new windows.