import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia 
import os
import requests

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Adjust speaking speed
engine.setProperty('volume', 1.0)  # Set volume level

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user input and return recognized speech as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"User  said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Please repeat.")
            return ""
        except sr.RequestError:
            speak("Speech recognition service is unavailable.")
            return ""

def get_time():
    """Get the current time."""
    return datetime.datetime.now().strftime("%I:%M %p")

def open_website(url):
    """Open a website in the default web browser."""
    webbrowser.open(url)
    speak(f"Opening {url}")

def search_wikipedia(query):
    """Search Wikipedia and return a summary."""
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except wikipedia.exceptions.PageError:
        speak("No information found on Wikipedia.")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")

def get_weather(city):
    """Fetch current weather details from an API (OpenWeatherMap)."""
    api_key = "your_api_key_here"  # Replace with your OpenWeatherMap API key
    if api_key == "your_api_key_here":
        speak("Please set your OpenWeatherMap API key in the code.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") == 200:
        temperature = response["main"]["temp"]
        description = response["weather"][0]["description"]
        speak(f"The weather in {city} is {description} with a temperature of {temperature} degrees Celsius.")
    else:
        speak("City not found. Please try again.")

def execute_command(command):
    """Process user commands and execute tasks."""
    if "time" in command:
        speak(f"The current time is {get_time()}")

    elif "open youtube" in command:
        open_website("https://www.youtube.com")

    elif "open google" in command:
        open_website("https://www.google.com")

    elif "wikipedia" in command:
        speak("What do you want to search on Wikipedia?")
        query = listen()
        if query:
            search_wikipedia(query)

    elif "weather" in command:
        speak("Which city's weather would you like to check?")
        city = listen()
        if city:
            get_weather(city)

    elif "open notepad" in command:
        os.system("notepad")

    elif "who is naveen" in command:
        speak("Yuvaraj wife")

    elif "who is nitish" in command:
        speak("He is a ultra gay")

    elif "where is nitish" in command:
        speak("Avan kaiadikka poyirukkan")

    elif "exit" in command or "quit" in command:
        speak("Good bye! Have a great day.")
        exit()

    else:
        speak("I'm sorry, I can't do that yet. Try another command.")

def main():
    """Main loop for the voice assistant."""
    speak("Hello! How can I assist you today?")
    while True:
        command = listen()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()