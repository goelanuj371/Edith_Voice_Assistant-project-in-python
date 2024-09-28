import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import sys
from googletrans import Translator

# Language dictionary for translation
dic = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Basque': 'eu',
    'Belarusian': 'be',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Bulgarian': 'bg',
    'Catalan': 'ca',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'English': 'en',
    'Estonian': 'et',
    'Finnish': 'fi',
    'French': 'fr',
    'Galician': 'gl',
    'Georgian': 'ka',
    'German': 'de',
    'Greek': 'el',
    'Gujarati': 'gu',
    'Haitian Creole': 'ht',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Irish': 'ga',
    'Italian': 'it',
    'Japanese': 'ja',
    'Kazakh': 'kk',
    'Korean': 'ko',
    'Kurdish (Kurmanji)': 'ku',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Macedonian': 'mk',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Punjabi': 'pa',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Spanish': 'es',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Xhosa': 'xh',
    'Zulu': 'zu',
}

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # You can change the index to select a different voice

# Function to make the assistant speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Function to greet based on the time of day
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")
    speak("I am Edith. How can I assist you today?")

# Function to take user commands through the microphone
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Could not understand, please repeat...")
        return "none"
    return query.lower()

# Function to translate speech into a target language
def translateSpeech(query, target_lang='es'):
    translator = Translator()
    try:
        translated = translator.translate(query, dest=target_lang)
        language_name = [lang for lang, code in dic.items() if code == target_lang][0]  # Get the language name
        speak(f"Translating to {language_name}")  # Announce the target language
        print(f"Translated: {translated.text}")
        speak(translated.text)  # Ensure that the translated text is spoken
    except Exception as e:
        print("Translation error:", e)
        speak("Sorry, I couldn't complete the translation.")

# Function to dynamically open websites
def openWebsite(query):
    # Extract the website name (anything after 'open')
    try:
        website = query.split("open ")[1]
        if "." not in website:
            website += ".com"  # Default to .com if not mentioned
        url = f"http://{website}"
        speak(f"Opening {website}")
        webbrowser.open(url)
    except IndexError:
        speak("I couldn't understand the website you want to open.")

# Function to handle searches on Google
def searchGoogle(query):
    try:
        search_term = query.split("search ")[1]
        speak(f"Searching {search_term} on Google")
        webbrowser.open(f"https://www.google.com/search?q={'+'.join(search_term.split())}")
    except IndexError:
        speak("I couldn't understand the search query.")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        if 'wikipedia' in query:
            speak('Searching on Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                print(e)
                speak("Sorry, no results found on Wikipedia.")

        elif 'open' in query:
            openWebsite(query)

        elif 'search' in query:
            searchGoogle(query)

        elif 'translate' in query:
            speak("Which language should I translate to?")
            target_lang_query = takeCommand()
            # Normalize the target language query
            target_lang_normalized = target_lang_query.strip().lower()
            # Match the spoken language to the language codes
            target_lang = None
            for lang, code in dic.items():
                if lang.lower() == target_lang_normalized:
                    target_lang = code
                    break
            if target_lang:  # Check if we found a matching language code
                speak("Please speak the sentence you want to translate.")
                sentence = takeCommand()
                translateSpeech(sentence, target_lang)
            else:
                speak("Sorry, I don't support that language.")

        elif "stop" in query or "quit" in query or "exit" in query:
            speak("Goodbye!")
            sys.exit()
