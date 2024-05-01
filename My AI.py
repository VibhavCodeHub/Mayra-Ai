import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import os
import random
import tkinter as tk
from playsound import playsound
import time
import threading

# Variations of the assistant's name
assistant_names = ["mayra", "mera"]

# Sound files
LISTENING_SOUND = "listening.mp3"
SLEEP_SOUND = "sleep.mp3"
BUTTON_PRESS_SOUND = "button_press.mp3"

# Global variable to control program execution
running = False
assistant_thread = None

def execute(command):
    print("Executing command:", command)  # Add this line
    if "dance" in command:
        speak("Sure! Let's dance!")
        # Show dancing GIF
        webbrowser.open("https://media.giphy.com/media/ASd0Ukj0y3qMM/giphy.gif")
        # Play music for 10-12 seconds
        # Replace the music URL with your desired music file or streaming service link
        music_url = "https://soundcloud.com/user-177125779/jawani-gulab-sidhu-1?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing"  # Example music URL
        os.system(f"start {music_url}")
        time.sleep(12)  # Wait for 12 seconds
    elif "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        # Change the path to WhatsApp application on your system
        if os.path.exists("C:\\Path\\To\\WhatsApp.exe"):
            os.system("runas /user:administrator \"C:\\Path\\To\\WhatsApp.exe\"")
        else:
            print("WhatsApp does not exist in this path.")
    elif "which day is it" in command:
        # Implement your logic to tell the day
        pass
    elif "tell me the time" in command:
        # Implement your logic to tell the time
        pass
    elif "bye" in command:
        speak("Goodbye! Take care and call me if you need.")
        exit()
    elif "from wikipedia" in command:
        speak("Checking Wikipedia")
        query = command.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=4)
        speak("According to Wikipedia:")
        speak(result)
    elif "tell me your name" in command:
        speak("I am your virtual assistant. My name is Mira.")
    elif any(greeting in command for greeting in ["hi", "hello", "hey"]):
        speak("Hello! How can I assist you?")
    elif any(apology in command for apology in ["sorry", "apologies"]):
        speak("No problem. How can I assist you?")
    elif any(keyword in command for keyword in ["open", "launch", "run"]):
        # Split the command by spaces and remove the first word (e.g., "open")
        command_words = command.split()
        if len(command_words) > 1:
            name = ' '.join(command_words[1:])  # Join the remaining words as the application name
            speak(f"Opening {name}")
            try:
                # Try to open the application using webbrowser.open()
                webbrowser.open(name)
            except Exception as e:
                print(e)
                speak(f"Sorry, I could not open {name}.")
        else:
            speak("Sorry, I didn't catch the name of the application. Please try again.")
    else:
        # If the query is not recognized as a command, ask the user if they want to perform a web search
        speak("I'm not sure what you mean. Would you like me to search the web?")
        response = takeCommand().lower()
        if "yes" in response:
            speak("Let me search for that.")
            webbrowser.open("https://www.google.com/search?q=" + command)
        else:
            speak("Okay, let me know if there's anything else I can help with.")

def speak(audio):
    engine = pyttsx3.init()
    # Setting the voice to a young female voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Assuming the female voice is at index 1
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        playsound(LISTENING_SOUND)  # Play listening sound
        recognizer.pause_threshold = 0.7
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language='en-in')
            print("User command:", command)
            return command.lower()  # Convert the command to lowercase for comparison
        except Exception as e:
            print(e)
            return None  # Return None when recognition fails

def assistant_function():
    global running
    while running:
        command = takeCommand()
        if command is not None:
            print("Recognized command:", command)  # Add this line
            if any(name in command.lower() for name in assistant_names):
                speak("Yes, how can I assist you?")
                execute(command)
            else:
                print("AI is ON")
        else:
            print("Please say that again.")

first_activation = True

def toggle_assistant():
    global running, assistant_thread, first_activation
    if not running:
        if first_activation:
            speak("Hello, I'm your AI assistant (Mayra). How can I assist you today?")
            first_activation = False
        running = True
        assistant_thread = threading.Thread(target=assistant_function)
        assistant_thread.start()
        button.config(text="Stop Assistant")
    else:
        running = False
        assistant_thread.join()  # Wait for the assistant thread to finish
        speak("Stopping the assistant.")
        print("AI is OFF")
        button.config(text="Start Assistant")

if __name__ == "__main__":
    # Create the GUI window
    root = tk.Tk()
    root.title("AI Assistant")

    # Create a label
    label = tk.Label(root, text="Click the button to toggle the AI Assistant")
    label.pack()

    # Create a button
    button = tk.Button(root, text="Toggle Assistant", command=toggle_assistant)
    button.pack()

    root.mainloop()
