import subprocess
import pandas as panda
from ipaddress import ip_address
from logging.config import listen
import wikipedia

from pyparsing import original_text_for

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy.util import await_only
from pyspark.sql import SparkSession
from webdriver_manager.chrome import ChromeDriverManager
import os
import pyarrow
import socket
import requests
import geocoder
import asyncio
import webbrowser
import pywhatkit
import pyttsx3
import speech_recognition as sr
import pyaudio
import datetime
import time
import pyautogui
from requests import get
from googletrans import Translator
from gtts import gTTS
import playsound
import os
import uuid

from wikipedia import summary

# Initialize the TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Replace with the actual path to the ChromeDriver
CHROMEDRIVER = "E:\APPS\chromedriver-win64"

MOVIE_FOLDER_NAME = "F:\\Movies"

MOVIE_SUPPORTED_EXTENSIONS = ['.mp4','.mkv','.avi','.mov']

VLC_PATH = r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\VideoLAN\\VLC\vlc.exe"

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
recognizer = sr.Recognizer()
translator = Translator()
engine = pyttsx3.init()

def listen_and_detect():

    with sr.Microphone() as source:
        print("Listening.......")
        audio = recognizer.listen(source)
        try:
            print("Recognizing........")
            query = recognizer.recognize_google(audio)
            print("You said", query)
            return query
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio")
        except sr.RequestError:
            print("Could not request results")
        return None
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
# listen and translate
async def listen_and_translate():
    while True:
        print("\n---- Main Menu ----")
        speak("Say something to translate or say 'main menu' to go back")
        query = listen_and_detect()
        if query:
            if "main menu" in query.lower() or "exit" in query.lower() or "go back" in query.lower():
                speak("Returning to the main menu")
                print("Returning to the main menu")
                break
            else:
               await detect_and_translate(query)
# Fetch user Location
def get_user_location():
    try:
        res = requests.get("https://ipinfo.io")
        data = res.json()
        city = data.get("city", "Unknown")
        latitude, longitude = data.get("loc", "0,0").split(",")
        return city, latitude, longitude
    except Exception as e:
        print("Failed to get location:", e)
        speak("I couldn't determine your location.")
        return "Unknown", "0", "0"
#Get weather command
def weather_listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        speak("Please say something...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            speak("Sorry, I couldn't hear you. Please try again.")
        except sr.UnknownValueError:
            print("Could not understand audio.")
            speak("I didn't catch that. Could you repeat?")
        except sr.RequestError as e:
            print(f"Error: {e}")
            speak("There was an error with the voice service.")
        return None
# Get the weather of the location
def get_weather(city):
    api = "b5df6ce959c52f1149f64772a4120899"
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
    try:
        params = {"q":city,"appid":api,"units":"metric"}
        response = requests.get(BASE_URL,params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_report = (f"The current weather in {city} is {weather_description}. "
                              f"The temperature is {temp} degrees Celsius with a humidity of {humidity}% "
                              f"and wind speed of {wind_speed} meters per second.")
            return weather_report
        else:
            return f"Could not fetch the weather report"
    except Exception as e:
        print("Error fetching details ",e)
        return "Sorry, I could not fetch the details"

# Get weather prediction
def weather_detection():
    speak("Do you want to know the today's weather?")
    print("Do you want to know the today's weather?")
    command = weather_listen()
    if command and "yes" in command:
        city,latitude,longitude = get_user_location()
        speak(f"Fetching weather information for {city}.")
        weather_report = get_weather(city)
        print(weather_report)
        speak(weather_report)
    elif "main menu" in command:
        return ""
    else:
        print("Okay let me know if you want something else")
# Translation
async def detect_and_translate(text):
    detected = await translator.detect(text)
    lang_code = detected.lang
    print(f"Detected language:{lang_code}")

    # Translate to Indian english
    translation =await translator.translate(text,src = lang_code,dest='en')
    print(f"Translated:{translation.text}")
    speak(f"{translation.text}")
# Wikipedia
def listen_wikipedia_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Sir, what do you like to search on wikipedia?")
        print("Listening for topic......")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said:{command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I could not understand that")
        return command
    except sr.UnknownValueError:
        print("There was a problem connecting to the speech service")
        return None
# Listen google Command
def listen_google_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("What do you want to search for the day,Sir?")
        print("Listening........")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google()
        print(f"You said:{command}")
        return command
    except sr.UnknownValueError:
        print("Sorry. I didn't understand understand what you said")
        return None
    except sr.RequestError:
        print("Cannot request result")
        return  None


# search in google
def search_google():
    command = listen_google_command()
    if command:
        speak(f"Searching in google")
        pywhatkit.search(command)
# WikiPedia Search Command by Voice Command
def search_wikipedia_info(query):
    try:
        query = query.replace("wikipedia","")
        summary = wikipedia.summary(query)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is too vague. Try one of these: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "Sorry! I couldn't find any results on the query"
    except Exception as e:
        return f"Ann error has occurred: {str(e)}"
EMAIL = "9875441655"
PASSWORD = "Suman@Talukdar"
# open facebook
def login_facebook():
    speak("Opening your facebook and logging into your profile now...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.facebook.com")
    time.sleep(2)
    email_input = driver.find_element(By.ID,"email")
    password_input = driver.find_element(By.ID,"pass")
    login_button = driver.find_element(By.NAME,"login")

    email_input.send_keys(EMAIL)
    password_input.send_keys(PASSWORD)
    login_button.click()
    speak("You are now logged into facebook")
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
        elif "open translator" in query:
            asyncio.run(listen_and_translate())
        elif "open weather" in query:
            weather_detection()
        elif "open ip address" in query:
            try:
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                speak(f"Your Ip address is {ip}")
            except Exception as e:
                print("Error",e)
        elif "open word" in query:
            npath = "C:\\Program Files (x86)\\Microsoft Office\\Office14\\WINWORD.exe"
            os.startfile(npath)
            speak("Writing to Microsoft Word .........Please sir, will you instruct me what to write in the notepad")
            listen_and_type()
        elif "open powerpoint" in query:
            npath = "C:\\Program Files (x86)\\Microsoft Office\\Office14\\POWERPNT.exe"
            os.startfile(npath)
        elif "open excel" in query:
            npath =  "C:\\Program Files (x86)\\Microsoft Office\\Office14\\EXCEL.exe"
            os.startfile(npath)
        elif "open wikipedia" in query:
            topic = listen_wikipedia_command()
            if topic:
                result = search_wikipedia_info(topic)
                speak(f"According to wikipedia, {result}")
        elif "open facebook" in query:
            login_facebook()
        elif "open instagram" in query:
            webbrowser.get("https://www.instagram.com/suman.talukdar53/")
        elif "open linkedin" in query:
            webbrowser.get("https://www.linkedin.com/in/suman-talukdar-29b3352b6")
        elif "open github" in query:
            webbrowser.get("https://github.com/jiraiyasuman")
        elif "open google" in query:
            search_google()
