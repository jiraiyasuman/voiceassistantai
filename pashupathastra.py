from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
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

# Replace with the actual path to the ChromeDriver
CHROMEDRIVER = "E:\APPS\chromedriver-win64"

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Text-to-speech function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to play the song
def play_song_on_youtube(song_name):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.youtube.com")

    # Wait for the page to load
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "search_query")
    search_box.send_keys(song_name)
    search_box.submit()

    try:
        # Wait and play first video
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "video-title"))
            )
            first_video = driver.find_elements(By.ID, "video-title")[0]
            first_video.click()

    except Exception as e:
            print(" Error playing video:", e)

# Function to take voice input
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("What song do you like to play, Sir?")
        print(" Say the song name to play on YouTube...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f" You said: {command}")
        return command
    except sr.UnknownValueError:
        print(" Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f" Could not request results; {e}")
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

        return "none"
    except Exception as e:
        print(f"Microphone error: {e}")

        return "none"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:

        return "none"
    except sr.RequestError:

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
                elif "change line" in command:
                    pyautogui.typewrite(command + '\n')
                elif "space" in command:
                    pyautogui.typewrite(" ")
                elif "main menu" in command:
                    return
                else:
                    pyautogui.typewrite(command + ' ')
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
        elif "cmd" in query:
            os.system("start cmd")
        elif "open spotify" in query:
            npath = "C:\\Users\\SUMAN\\AppData\\Roaming\\Spotify\\Spotify.exe"
            os.startfile(npath)
        elif "open youtube" in query:
            command = listen_command()
            if command:
                play_song_on_youtube(command)
         