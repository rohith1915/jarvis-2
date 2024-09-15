
import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime

# Initialize the recognizer and the text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice commands."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return ""

def set_reminder():
    """Set a simple reminder."""
    speak("What would you like to be reminded about?")
    task = listen()
    
    if task:
        speak("When should I remind you? Please provide the time in the format HH:MM.")
        reminder_time = listen()
        
        try:
            # Parse the time
            reminder_time_obj = datetime.datetime.strptime(reminder_time, "%H:%M").time()
            speak(f"Reminder set for {reminder_time}. I will remind you to {task}.")
            
            # Check the time periodically (this part needs to be improved for real-time reminders)
            while True:
                now = datetime.datetime.now().time()
                if now >= reminder_time_obj:
                    speak(f"Reminder: {task}")
                    break
                
        except ValueError:
            speak("Sorry, I didn't get the time format. Please try again.")
    
def create_todo_list():
    """Create a to-do list."""
    todo_list = []
    speak("Tell me the tasks you want to add to your to-do list. Say 'stop' when you are done.")
    
    while True:
        task = listen()
        if task == "stop":
            break
        todo_list.append(task)
        speak(f"Added {task} to your to-do list.")
    
    speak(f"Your to-do list contains: {', '.join(todo_list)}.")

def search_web():
    """Search the web."""
    speak("What do you want to search for?")
    query = listen()
    
    if query:
        url = f"https://www.google.com/search?q={query}"
        speak(f"Searching for {query} on the web.")
        webbrowser.open(url)

def voice_assistant():
    """Main function for voice assistant."""
    speak("Hello! How can I help you today?")
    
    while True:
        command = listen()
        
        if "reminder" in command:
            set_reminder()
        elif "to-do list" in command:
            create_todo_list()
        elif "search" in command:
            search_web()
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't catch that. Can you repeat?")

if __name__ == "__main__":
    voice_assistant()
