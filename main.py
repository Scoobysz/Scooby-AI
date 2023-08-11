import speech_recognition as sr
import os
import webbrowser
import datetime
import openai
import pyttsx3
import requests
from config import apikey, weather_api_key, news_api_key, youtube_api_key, access_key, wake_word_model_path
from googleapiclient.discovery import build
import pvporcupine
#import pyaudio

AI_NAME = "Scooby"
is_speaking = False
porcupine = pvporcupine.create(access_key=access_key, keyword_paths=[wake_word_model_path])


def play_music(title, artist):
    search_query = f"{title} {artist} music video"

    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    search_response = youtube.search().list(
        q=search_query,
        part="id",
        maxResults=1,
        type="video"
    ).execute()

    video_id = search_response["items"][0]["id"]["videoId"]

    webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")


def say(text):
    global is_speaking
    is_speaking = True
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    is_speaking = False


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt} \n*******************\n\n"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
    )

    generated_text = response.choices[0].text.strip()
    print(generated_text)
    text += generated_text

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('AI')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def chat(query, chatStr):
    openai.api_key = apikey
    chatStr += f"Abhay: {query}\n Scooby:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=100,
        n=1,
        stop=None,
    )

    generated_text = response.choices[0].text.strip()

    if "open" in query.lower() and ("youtube" in query.lower() or any(
            site in query.lower() for site in ["instagram", "wikipedia", "google", "twitter", "gmail"])):
        # Extract the site name from the query
        site_name = next((site for site in ["YouTube", "Instagram", "Wikipedia", "Google", "Twitter", "Gmail"] if
                          site.lower() in query.lower()), "")
        if site_name:
            say(f"Opening {site_name}....")
            webbrowser.open(f"https://www.{site_name.lower()}.com")
    else:
        say(generated_text)

    chatStr += f"{generated_text}\n"

    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(query.split('AI')[1:]).strip()}.txt", "w") as f:
        f.write(chatStr)

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        return f"The weather in {city} is {weather_desc}. The temperature is {temp:.1f}°C and humidity is {humidity}%."
    else:
        return "Sorry, I couldn't fetch the weather data."


def get_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}"
    response = requests.get(url)
    data = response.json()
    if data["status"] == "ok" and data["totalResults"] > 0:
        articles = data["articles"]
        news = ""
        for i, article in enumerate(articles[:5]):
            title = article["title"]
            description = article["description"]
            news += f"{i + 1}. {title}\n{description}\n\n"
        return news
    else:
        return "Sorry, I couldn't find any news on that topic."

def takeActualCommand():
    global is_speaking
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Listening for user's query...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")

            if "open youtube" in query.lower():

                video_title = query.lower().replace("open youtube", "").strip()

                if video_title:
                    openYouTubeVideo(video_title)
                else:
                    say("Please specify the title of the YouTube video.")

            if "stop" in query.lower() and is_speaking:
                say("Okay, stopping.")
                is_speaking = False

            return query
        except Exception as e:
            return "Some error occurred. Sorry."


def do_internet_search(query):
    
    search_query = query.lower().replace("do internet search", "").strip()
    if search_query:
        say(f"Searching the internet for {search_query}...")
        webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
    else:
        say("Please specify the search query after 'do internet search'.")

def takeCommand():
    global is_speaking
    r = sr.Recognizer()
    wake_word_detected = False

    while not wake_word_detected:
        with sr.Microphone() as source:
            r.pause_threshold = 1
            audio = r.listen(source)
            try:
                print("Listening for wake word...")
                query = r.recognize_google(audio, language="en-in")
                print(f"User said: {query}")

                if "scooby" in query.lower():
                    wake_word_detected = True
                    say("How can I assist you?")
                    return takeActualCommand()

                if "do internet search" in query.lower():
                    wake_word_detected = True
                    do_internet_search(query)
            except Exception as e:
                pass


def openYouTubeVideo(title):
    search_query = title + " YouTube"
    url = f"https://www.youtube.com/results?search_query={search_query}"
    webbrowser.open(url)


say(f"Hello, I am your personal AI assistant {AI_NAME}")
chatStr = ""

while True:
    query = takeCommand()

    if query:
        print("Processing your request...")
        say("Processing your request...")

    sites = [
        # ["YouTube", "https://www.youtube.com"],
        ["Wikipedia", "https://www.wikipedia.com"],
        ["Google", "https://www.google.com"],
        ["Instagram", "https://www.instagram.com"],
        ["Twitter", "https://www.twitter.com"],
        ["Gmail", "https://mail.google.com/mail/u/0/#inbox"],
    ]

    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]}....")
            webbrowser.open(site[1])

    if "The time" in query:
        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"The time is {strfTime}")

    if "weather forecast" in query.lower():
        say("Sure, for which city would you like to know the weather?")
        city = takeCommand()
        weather_info = get_weather(city)
        say(weather_info)

    if "Using AI".lower() in query.lower():
        ai(prompt=query)
    elif "open YouTube" in query.lower():

        if len(query.split("open YouTube ")) > 1:
            video_title = query.split("open YouTube ")[1]
            openYouTubeVideo(video_title)
        else:
            say("Sure, opening YouTube...")
            webbrowser.open("https://www.youtube.com")
    elif "news" in query.lower():
        say("Sure, what topic are you interested in?")
        topic = takeCommand()
        news = get_news(topic)
        say(news)
    elif "play music" in query.lower():
        say("Sure, what is the title of the music?")
        title = takeCommand()

        say("Great! And what is the name of the artist?")
        artist = takeCommand()

        play_music(title, artist)
    elif "do internet search" in query.lower():
        do_internet_search(query)
    else:
        chat(query, chatStr)