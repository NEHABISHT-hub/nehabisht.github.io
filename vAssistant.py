import speech_recognition as sr
import pyttsx3
import webbrowser
import requests
import musiclibrary
from openai import OpenAI, completions

# Initialize speech recognition and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "260f9618674d45bcb17b80292ffd9908"

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()
    
def AIprocess(Command):
    
  client = OpenAI( api_key="<Your Key Here>",
  )

  completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named Alex skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "command"}
  ]
)

  return completion.choices[0].message.content


# Function to process commands
def processCommand(c):
    c = c.lower()
    print(f"Processing command: {c}") 
    if "open google" in c:
        print("Opening Google...")
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        print("Opening Facebook...")
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        print("Opening YouTube...")
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        print("Opening LinkedIn...")
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[-1]
        if song in musiclibrary.music:
            link = musiclibrary.music[song]
            webbrowser.open(link)
            speak(f"Playing {song}")
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "news" in c:
        try:
            print(f"Fetching news for command: {c}")
            r = requests.get(f"https://newsapi.org/v2/everything?q=world&apiKey={newsapi}")

            print(f"Status code: {r.status_code}")
            print(f"Response: {r.text}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])
                if articles:
                    speak("Here are the top news headlines:")
                    for article in articles[:3]:
                        speak(article['title'])
                else:
                    speak("No news articles found.")
            else:
                speak("Failed to fetch news.")
        except Exception as e:
            speak(f"An error occurred while fetching news: {e}")
    else:
        output = AIprocess(c)
        speak(output)

# Main Program
if __name__ == "__main__":
    speak("Hello, I am your virtual assistant 'Alex'. How can I help you today?")
    
    while True:
        with sr.Microphone() as source:
            print("Listening for 'Alex'...")
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")

                # Check for Alex trigger
                if "alex" in command.lower():
                    speak("Yes, Alex here! What can I do for you?")
                    
                    # Listen for the actual command after Alex trigger
                    print("Listening for your command...")
                    audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    user_command = recognizer.recognize_google(audio)
                    print(f"Command received: {user_command}")
                    
                    processCommand(user_command)
                    
                else:
                    print("No trigger word detected.")
            
            except sr.WaitTimeoutError:
                print("Listening timed out. Please speak again.")
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Request failed: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")




