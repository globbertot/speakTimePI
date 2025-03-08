# speakTimePI
A simple python script that uses TTS to speak out the current time in greek.

# Requirements
- `espeak` or `mpg123 and an internet connection`
- `python 3.X`

# Installation
1) Clone this repository
2) Set up the raspberry pi so that you have one jumper wire connected from GND to one leg of your button and one to GPIO pin 16 and the other end to the other leg of the button

You are ready to run the script using `python3 timerPI.py`

# Roadmap (sort of)
- ~~Configuration files~~ Mostly done, more settings could be added in the future
- ~~Tell seconds as well~~ DONE
- ~~Any language~~ Sort of done, more languages may be added in the `langs.py` file
- Connect a screen to also display the time
