# -*- coding: utf-8 -*-
from datetime import datetime
from time import sleep
from gpiozero import Button
from signal import pause
import subprocess
import requests
import os
from gtts import gTTS
from langs import languages

confFile = "./conf";

# Navigation stuff / Setup #
def showHelp():
    os.system("clear");
    print("-----\n\nHELP MENU\n\n-----\n`help` - Shows this menu\n`lang` - set up the language\n`pin` - set up the GPIO pin\n`done` - exit the setup\n\n");

def langSetup():
    os.system("clear");
    good = False;
    langCode = 'el';

    while not good:
        ipt = input("To list language options write `ls`\nPlease enter your language: ");
        ipt = ipt.lower();

        if (ipt == 'ls'):
            for lang in languages:
                langs = languages[lang];
                print(f"Lang: {lang} || {langs['long']}");
            continue;

        if (len(ipt) > 2 or not languages.get(ipt)):
            print(f"Language {ipt} is not supported yet, please list the laungages if you need a refresher.");
            continue;

        langCode = ipt;
        good = True;

    with open(confFile, 'a') as f:
        f.write(f"lang:{langCode}\n");

def pinSetup():
    os.system("clear");
    good = False;
    pin = 16;

    while not good:
        ipt = input("Please enter the GPIO (BCM) pin you have connected the button to: ");

        if (int(ipt) < 0 or int(ipt) > 27): #TODO: Maybe validate the pin better?
            print("Invalid GPIO pin\n");
            continue;

        good = True;
        pin = int(ipt);

    with open(confFile, 'a') as f:
        f.write(f"pin:{pin}\n");

def mainMenu():
    done = False;

    if (os.path.isfile(confFile)):
        done = True;

    while not done:
        cmd = input("\n\nWelcome to narrateTime setup\n\nFor all the commands type `help`\n\nCommand: ");
        cmd = cmd.lower();

        if (cmd == "help"):
            showHelp();
        elif (cmd == "lang"):
            langSetup();
        elif (cmd == "pin"):
            pinSetup();
        elif (cmd == "done"):
            input("Note: If you change your mind about the settings you can delete the conf file to show this menu again.\nPress enter to actually exit");
            done = True;
        else:
            print(f"Unknown command: {cmd}");

    os.system("clear");

def parseConf():
    try:
        lang = 'el';
        pin = 16;
        with open(confFile, 'r') as f:
            for line in f:
                line = line.strip(); # Remove \n 

                if (line.startswith("lang:")):
                    lang = line.split(":", 1)[1];
                    if (not lang or not languages.get(lang)):
                        lang = "el" # Revert back to default.

                elif (line.startswith("pin:")):
                    pin = int(line.split(":", 1)[1]);
                    if (pin < 0 or pin > 27):
                        pin = 16;

        return {"lang": lang, "pin": pin};
    except FileNotFoundError:
        print("No configuration, reverting back to defaults..");
        return {"lang": 'el', "pin": 16};

# The real thing
def checkInternet():
    try:
        r = requests.get("https://google.com", timeout=5);
        return r.status_code == 200;
    except Exception as e:
        return False;

def speak(text, conf):
    """Calls google translate or espeak to say the text TTS"""
    try:
        internet = checkInternet();
        if (internet):
            tts = gTTS(text=text, lang=conf["lang"]);
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

def speakNum(num, lang='el'):
    """
    Return's the long version of a number
    For example: speakNum(5) -> πέντε || speakNum(12) -> δώδεκα
    """
    try:
        langDict = languages.get(lang);
        if (not langDict):
            raise ValueError(f"{lang} is not supported yet.");

        if (num in langDict):
            return langDict[num]; # Special cases, ex: 10 returns ten

        firstDigit = num // 10 * 10; # Get the tens (20, 10, 30..)
        lastDigit = num % 10; # Get the ones (1, 2, 3..)
        rtn = "";

        if (firstDigit > 0):
            rtn += langDict.get(firstDigit, "") + " ";

        if (lastDigit > 0):
            rtn += langDict.get(lastDigit, "");

        return rtn;
    except Exception as e:
        print(f"Error getting number..\nException: {e}");

def getCurrentTime(conf):
    """Gets the current hour and minutes, formats it and speaks it"""
    print("Pressed");
    hour = datetime.now().hour;
    minute = datetime.now().minute;
    seconds = datetime.now().second;

    text = languages[conf["lang"]].get("timePhrase");
    localized = text.format(
        hour=speakNum(hour, conf["lang"]),
        minute=speakNum(minute, conf["lang"]),
        second=speakNum(seconds, conf["lang"]),
    );

    speak(localized, conf);

def main():
    mainMenu();
    config = parseConf();

    btn = Button(config["pin"], bounce_time=0.1);
    btn.when_pressed = lambda: getCurrentTime(config);
    print("Press the button to speak the current time");
    
    try:
        pause();
    except KeyboardInterrupt:
        print("Exiting..");
        btn.close();

if __name__ == "__main__":
    main();
