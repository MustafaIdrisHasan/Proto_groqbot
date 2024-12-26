import os
import pyttsx3
import speech_recognition as sr
import random
import sys
from groq import Groq

# Initialize Groq API Client
client = Groq(
    api_key="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",  # Make sure your API key is set in your environment
)

# Initialize the speech-to-text engine
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
engine.setProperty('rate', 150)  # Set speed of speech
engine.setProperty('volume', 0.9)  # Set volume of speech

# Sample FAQ dictionary
faq_dict = {
    "what is horizon": [
        "Horizon is a research-based group located at MJCET that aims to improve the technical and soft skills of engineers, making them more industry-ready.",
        "We are a team committed to enhancing the quality of engineers through various technical workshops and projects."
    ],
    "what is horizons vision": [
        "Our vision is to enhance the quality of engineers graduating by making innovative projects, improving technical skills, and focusing on networking.",
        "We envision a future where every engineering graduate is well-prepared for the challenges of the industry.",
        "Horizon strives to bridge the gap between theoretical knowledge and practical skills, helping students succeed in their careers."
    ],
    "what is reality check": [
        "Our flagship event is called 'Reality Check,' happening on 11th November.",
        "'Reality Check' is a seminar discussing the challenges facing placements today, such as recession, low skill sets, and overcrowding in the engineering field.",
        "'Reality Check' is Horizon's flagship event aimed at addressing the current placement issues and providing solutions."
    ],
    "when is the reality check event": [
        "The Reality Check event is on 11th November, from 1:30 PM to 4:00 PM.",
        "Join us for Reality Check on 11th November, from 1:30 PM to 4:00 PM at MJCET.",
        "Don't miss Reality Check on 11th November, running from 1:30 PM to 4:00 PM. Mark your calendars!"
    ],
    "why should i attend reality check": [
        "Attend Reality Check to understand why placements are at an all-time low and how you can overcome these challenges.",
        "Reality Check will provide valuable insights into the current job market, recession, and why engineering graduates are often unprepared.",
        "If you're concerned about placements, this seminar is for you. Come get a reality check and gain practical knowledge on how to improve your skills."
    ],
    "how much does reality check cost": [
        "Reality Check is available at a minimal price of Rs 50.",
        "The seminar is priced at Rs 50, making it an affordable way to gain valuable career insights.",
        "Join us for Reality Check for just Rs 50 and get a detailed understanding of the job market."
    ],
    "what will be discussed in reality check": [
        "We will be discussing why placements are at an all-time low, the effects of recession, and the lack of industry-ready skills among engineering graduates.",
        "The seminar will dive deep into issues like overcrowding in the engineering domain and how it affects placement opportunities.",
        "The topics at Reality Check include understanding the placement crisis, recession, and providing solutions for enhancing skills and employability."
    ],
    "how can horizon help improve my skills": [
        "Horizon provides technical workshops that focus on improving both technical and soft skills.",
        "By participating in our workshops, you will gain hands-on experience and improve your skill set, making you more competitive in the job market.",
        "Horizon offers project-based learning and mentorship to help you develop the right skills for a successful engineering career."
    ],
    "where is horizon located": [
        "Horizon is based at MJCET (Muffakham Jah College of Engineering and Technology).",
        "You can find Horizon at MJCET, where we host a variety of events and workshops to enhance student learning.",
        "Horizon is located at MJCET, and we are always welcoming students who are eager to improve their technical and soft skills."
    ],
    "how can i join horizon": [
        "You can join Horizon by participating in our workshops, events, and signing up for club activities.",
        "To be a part of Horizon, attend our events and get involved with the projects we organize.",
        "Joining Horizon is easy—just keep an eye on our upcoming events and workshops and get in touch with us!"
    ]
}


# Function to listen and recognize speech
# Function to listen and recognize speech
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            # Adjust for ambient noise (helps with noise cancellation)
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise before listening
            
            audio = recognizer.listen(source, timeout=5)  # 5 seconds timeout
            
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start.")
            return None
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return None


# Function to get response from the Groq API (using LLaMA 3 model)
def get_groq_response(user_input):
    try:
        # Set the chat completion request with system and user messages
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Horizon , a research-based club at MJCET. Horizon focuses on enhancing engineers' skills through technical workshops, projects, and networking. The club's flagship event, Reality Check, is a seminar on 11th November, from 1:30 PM to 4:00 PM. It will address issues such as low placements, the impact of recession, low skill sets among graduates, and overcrowding in the engineering field. The seminar also offers solutions to these challenges. The event is available at an affordable price of Rs 50.Answer all the questions in a max of 1-2chat\ sentences.Be sarcastic with heckler and roast them a bit. when asked about Ronaldo or messi support the GOAT Ronaldo and when asked about MAX verstapen say he is nothing in comaprison to Lewis hamilton"},
                {"role": "user", "content": user_input}
            ],
            model="llama3-8b-8192",  # Specify the LLaMA 3 model
        )

        # Get the response from Groq's API and return it
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"

# Function to get response from FAQ or Groq API
def get_response(user_input):
    # Normalize the input for matching FAQ
    normalized_input = user_input.strip().lower()
    
    if normalized_input in faq_dict:
        reply = random.choice(faq_dict[normalized_input])  # Choose a random predefined response
    else:
        # If the input is not in FAQ, get a response from Groq API (using LLaMA 3 model)
        reply = get_groq_response(user_input)
    
    print(f"Chatbot: {reply}")
    return reply

# Function to speak the response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Main loop to keep the chatbot running
def main():
    print("Horizon Event Chatbot is ready to chat!")
    while True:
        try:
            user_text = listen()  # Capture the user's voice input
            if user_text:
                normalized_input = user_text.strip().lower()  # Normalize user input
                if normalized_input == "goodbye":  # Check for the dead switch command
                    speak("Goodbye! Have a great day!")  # Respond before shutting down
                    sys.exit(0)
                response = get_response(user_text)  # Get a response from the chatbot model (FAQ or Groq)
                speak(response)  # Speak out the response to the user
        except KeyboardInterrupt:
            print("Chatbot shutting down.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

# Run the chatbot
if __name__ == "__main__":
    main()
