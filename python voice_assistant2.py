import speech_recognition as sr
import pyttsx3
import datetime
import time

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 = Male, 1 = Female

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def get_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.WaitTimeoutError:
            print("No speech detected within timeout.")
            speak("No speech detected. Please try again.")
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that.")
        except sr.RequestError:
            print("API unavailable or network error.")
            speak("Network error.")
        return ""


def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def tell_date():
    today = datetime.datetime.now()
    speak(f"Today's date is {today.strftime('%B %d, %Y')}")

def calculate(expression):
    expression = expression.replace("plus", "+")
    expression = expression.replace("minus", "-")
    expression = expression.replace("into", "*")
    expression = expression.replace("multiplied by", "*")
    expression = expression.replace("divided by", "/")
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def respond(text):
    if "time" in text:
        tell_time()
    elif "date" in text:
        tell_date()
    elif "hello" in text or "hi" in text:
        speak("Hello, how can I help you?")
    elif "how are you" in text:
        speak("I'm doing great, thank you!")
    elif "exit" in text or "quit" in text or "stop" in text:
        speak("Goodbye!")
        exit()
    elif any(op in text for op in ["plus", "minus", "into", "divided by", "+", "-", "*", "/"]):
        calculate(text)
    else:
        speak("Sorry, I don't understand that.")

# Run assistant
speak("Hi, I'm your assistant. What can I do for you?")
while True:
    command = get_audio()
    if command:
        respond(command)
