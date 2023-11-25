import os.path
import random
import win32com.client
from AppOpener import open as op
import speech_recognition as sr
import webbrowser
import openai
from config import apikey

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Nabeel: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    speaker.speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    with open('openai/textfile.txt', 'w') as f:
        f.write(text)

    # if not os.path.exists("Openai"):
    #     os.mkdir("Openai")
    #
    # # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    # with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
    #     f.write(text)
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio,language="en-in")
            print(f"User said:{query}")
            return query
        except Exception as e:
            return "Some error occured. Sorry form jarvis"

while 1:
    # print("Enter the word you speak")
    print("Listening..")

    query = takeCommand()
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
             ["google", "https://www.google.com"], ]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            speaker.Speak(f"Opening {site[0]} Nabeel...")
            webbrowser.open(site[1])

    if "open music".lower() in query:
        speaker.speak("opening your music player")
        op("Media Player")
    elif "open insta".lower() in query:
        op("Instagram")
    elif "whatsapp".lower() in query:
        op("WhatsApp")

    if "using ai".lower() in query.lower():
        ai(prompt=query)

    elif "reset chat".lower() in query.lower():
        chatStr = ""

    else:
        print("Chatting...")
        chat(query)




    # speaker.Speak(text)
