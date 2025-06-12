import os
import webbrowser
import pywhatkit
import pyttsx3
import speech_recognition as sr
import pyaudio
import datetime
import time
import pyautogui
from requests import get
# Initialize the TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Text-to-speech function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to play the song
def play_on_youtube(song_name):
    speak(f"Playing {song_name} on YouTube")
    pywhatkit.playonyt(song_name)

# Control YouTube using keyboard
def youtube_control(action):
    key_map = {
        "pause": "space",
        "resume": "space",
        "stop": "w",  # no native 'stop', but you can close tab if you want
        "mute": "m",
        "fullscreen": "f"
    }
    key = key_map.get(action)
    if key:
        pyautogui.press(key)
        speak(f"{action.capitalize()} command executed.")
    elif action == "exit":
        speak("Exiting the assistant.")
    else:
        speak("Unknown command.")

# Function to take voice input
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening for a song name...")
        speak("Which song would you like to play on YouTube?")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print(f" You said: {command}")
            return command
        except sr.UnknownValueError:
            print(" Sorry, I couldn't understand.")
            speak("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            print(" Could not request results.")
            speak("Network error.")
            return None

# Voice command capture
def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            #print("Listening from mic 10...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
    except sr.WaitTimeoutError:
        print("Listening timed out.")
        speak("Sorry, I didn't hear anything.")
        return "none"
    except Exception as e:
        print(f"Microphone error: {e}")
        speak("Microphone is not working correctly.")
        return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        speak("Sorry, I could not understand that.")
        return "none"
    except sr.RequestError:
        speak("Sorry, the speech service is unavailable.")
        return "none"
#date-time module
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0  and hour<=12:
        speak("Good Morning Sir!")
    elif hour>=12 and hour<16:
        speak("Good Afternoon Sir!")
    elif hour>=16 and hour<20:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir!")

# write to notepad
def listen_and_type():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Say 'stop typing' to exit.")
        while True:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")

                if "stop typing" in command:
                    print("Stopping typing.")
                    break
                else:
                    pyautogui.typewrite(command + '\n')
            except sr.WaitTimeoutError:
                print("No speech detected. Retrying...")
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                break
# Main program
if __name__ == "__main__":
    wish()
    speak("This is your personal voice assistant AI, Pashupathasthra. How can I help you?")
    while True:

        query = takeCommand().lower()
        # logic building for tasks
        if "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)
            speak("Writing to notepad.....Please sir, will you instruct me what to write in the notepad")
            listen_and_type()
        elif "open spring" in query:
            npath = "E:\\APPS\\sts-4.27.0.RELEASE\\SpringToolSuite4.exe"
            os.startfile(npath)
        elif "open command prompt" in query:
            os.system("start cmd")
        elif "open spotify" in query:
            npath = "C:\\Users\\SUMAN\\AppData\\Roaming\\Spotify\\Spotify.exe"
            os.startfile(npath)
        elif "open youtube" in query:
            #webbrowser.open("https://www.youtube.com")
            speak("What song do you like to play, Sir?")
            song = listen_command()
            if song:
                play_on_youtube(song)
                while True:
                    command = listen_command("You can say pause, resume, mute, fullscreen or exit.")
                    if "pause" in command:
                        youtube_control("pause")
                    elif "resume" in command:
                        youtube_control("resume")
                    elif "mute" in command:
                        youtube_control("mute")
                    elif "fullscreen" in command:
                        youtube_control("fullscreen")
                    elif "exit" in command or "stop" in command:
                        speak("Stopping YouTube control. Goodbye!")
                        break