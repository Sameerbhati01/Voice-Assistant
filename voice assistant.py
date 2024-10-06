import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import sys
import time
import requests
listener = sr.Recognizer()
engine = pyttsx3.init()
def talk(text):
    engine.say(text)
    engine.runAndWait()
def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            listener.adjust_for_ambient_noise(source)  
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)  
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except Exception as e:
        print(f"Error: {e}")
        pass
    return command
def get_weather(city):
    API_KEY = 'your_openweathermap_api_key'
    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data['cod'] == 200:
        main = data['main']
        weather = data['weather'][0]['description']
        temp = main['temp']
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    else:
        return "I couldn't fetch the weather information."
def run_alexa():
    global running
    command = take_command()
    print(f"Processing command: {command}")
    if 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            talk('Playing' + song)
            pywhatkit.playonyt(song)
        else:
            talk("I didn't catch the name of the song.")
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('current time is ' + time)
    elif 'open wikipedia' in command:
        topic = command.replace('open wikipedia', '').strip()
        if topic:
            url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
            talk(f'Opening Wikipedia page for {topic}')
            webbrowser.open(url)  # Open the Wikipedia page in the default web browser
        else:
            talk("I didn't catch the topic.")
    elif 'tell me weather' in command:
        city = command.replace('weather in', '').strip()
        if city:
            weather_info = get_weather(city)
            talk(weather_info)
            print(weather_info)
        else:
            talk("I didn't catch the city name.")
    elif 'set reminder' in command:
        try:
            parts = command.split('in')
            if len(parts) == 2:
                reminder_text = parts[0].replace('set reminder', '').strip()
                delay_part = parts[1].strip().split()
                if len(delay_part) > 0:
                    delay_minutes = int(delay_part[0])  # Convert the first part to an integer
                    set_reminder(reminder_text, delay_minutes)
                else:
                    talk("I didn't catch the number of minutes.")
            else:
                talk("I didn't catch the reminder details.")
        except ValueError:
            talk("I didn't understand the number of minutes for the reminder.")
    elif 'stop' in command or 'exit' in command:
        talk('Stopping Alexa')
        running = False
    elif 'date' in command:
        talk('sorry, I have a headache')
    elif 'are you single' in command:
        talk('I am in a relationship with Python')
    else:
        talk('Please say the command again.')
while True:
    run_alexa()
