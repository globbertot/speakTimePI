# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep
import subprocess
import RPi.GPIO as GPIO
from gtts import gTTS

lePin = 16; # Change this if neccesery to your GPIO PIN
internet = True;

def speak(text):
    """Calls espeak (greek) to say the text TTS"""
    try:
        print(internet);
        if (internet == True):
            tts = gTTS(text=text, lang='el');
            tts.save("output.mp3");
            subprocess.run(["mpg123", "output.mp3"], check=True);
        else:
            subprocess.run(["espeak", "-v", "el", "-s", "80", "-p", "30", "-a", "200", "-g", "5", text]);
    except Exception as e:
        print("Error speaking: ", e);
        if (internet):
            print("Are you sure you have an internet connection or have `mpg123` installed?");
        else:
            print("Are you sure you have `espeak` installed?");

def speakNum(num):
    """
    Return's the long version of a number
    For example: speakNum(5) -> πέντε || speakNum(12) -> δώδεκα
    """
    if (num == 20):
        return "είκοσι";
    elif (num == 12):
        return "δώδεκα";
    elif (num == 11):
        return "έντεκα";
    elif (num == 0):
        return "μηδέν";
    elif (num == 60):
        return "εξήντα";
    else:
        firstDigit = num // 10;
        lastDigit = num % 10;
        rtn = "";

        if (firstDigit == 1):
            rtn += "δέκα ";
        elif (firstDigit == 2):
            rtn += "είκοσι ";
        elif (firstDigit == 3):
            rtn += "τριάντα ";
        elif (firstDigit == 4):
            rtn += "σαράντα ";
        elif (firstDigit == 5):
            rtn += "πεενήντα ";

        if (lastDigit == 1 and firstDigit != 1):
            rtn += "εένα";
        elif (lastDigit == 2 and firstDigit != 1):
            rtn += "δύο";
        elif (lastDigit == 3):
            rtn += "τρία";
        elif (lastDigit == 4):
            rtn += "τέσσερα";
        elif (lastDigit == 5):
            rtn += "πέντε";
        elif (lastDigit == 6):
            rtn += "έξι";
        elif (lastDigit == 7):
            rtn += "επτά";
        elif (lastDigit == 8):
            rtn += "οκτώ";
        elif (lastDigit == 9):
            rtn += "εννιά";

        return rtn;

def getCurrentTime(channel):
    """Gets the current hour and minutes, formats it and speaks it"""
    hour = datetime.now().hour;
    minute = datetime.now().minute;
    print(hour);
    print(minute);
    text = "Η ώρα είναι: " + speakNum(hour) + " και " + speakNum(minute);
    print(text);
    speak(text);

def main():
    global internet;
    internet = True if input("Do you have internet (y/N): ").lower() == 'y' else False;

    GPIO.setmode(GPIO.BCM);
    GPIO.setup(lePin, GPIO.IN, pull_up_down=GPIO.PUD_UP);

    flag = True;
    print("Press the button to speak the current time");
    GPIO.add_event_detect(lePin, GPIO.FALLING, callback=getCurrentTime, bouncetime=300);
    
    try:
        while flag:
            sleep(0.1); # Small delay to reduce load while also running continously
    except KeyboardInterrupt:
        GPIO.cleanup();

if __name__ == "__main__":
    main();
