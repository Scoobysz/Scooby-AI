# Scooby-AI
Scooby is a Python-based AI assistant designed to assist users with a variety of tasks using voice recognition and AI-powered responses. The assistant can perform internet searches, provide weather forecasts, play music, share news, and engage in natural language conversations. The project leverages various APIs and libraries to provide a range of functionalities, aiming to enhance user convenience and interactivity.

Key Features:

Voice Recognition and Wake Word Detection: Scooby listens for a predefined wake word ("Scooby") to activate the assistant. It utilizes the SpeechRecognition library to capture and interpret user voice commands.

Natural Language Processing: The project integrates with OpenAI's GPT-3 engine to generate AI-powered responses and engage in natural language conversations with users.

Internet Search: Scooby can perform internet searches using Google search queries, opening the browser to display search results based on user input.

Weather Forecast: Users can inquire about weather conditions in a specific city. The assistant queries the OpenWeatherMap API to provide weather details, including temperature and humidity.

News Updates: Scooby fetches the latest news articles based on user-specified topics using the NewsAPI. It presents a summary of news articles to users.

Music Playback: The assistant can search for and play music videos from YouTube based on the title and artist provided by the user. It leverages the YouTube Data API to find relevant music videos.

Natural Language Chat: Users can engage in natural conversations with the assistant. Scooby processes user queries, generates AI responses, and provides appropriate answers or actions.

Speech Output: Scooby communicates with users by generating spoken responses using the pyttsx3 library. It can play music and provide information audibly.

Logging and Storage: The assistant logs AI-generated responses and user interactions in text files for future reference and analysis.

Technologies Used:

Python
SpeechRecognition library
OpenAI GPT-3 API
YouTube Data API
NewsAPI
OpenWeatherMap API
pyttsx3 library (text-to-speech)
webbrowser library (opening websites)
datetime module (for time information)
pvporcupine library (for wake word detection)
Usage:

Activate Scooby by saying "Scooby" to trigger the assistant.
Use voice commands or text input to ask questions, perform tasks, or engage in conversations.
Ask about the weather, inquire about news, play music, or perform internet searches.
Interact naturally with the assistant, which provides spoken responses or executes actions based on user input.
