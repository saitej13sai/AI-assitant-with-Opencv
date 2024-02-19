#TEJAI PROJECT
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import datetime
import cv2
import pyautogui
import time
import smtplib

# Configure Google Generative AI API key
genai.configure(api_key="a123456787")
model = genai.GenerativeModel("gemini-pro")

# Initialize the speech recognition recognizer outside the loop
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine outside the loop
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    with sr.Microphone() as source:
        recognizer.pause_threshold = 0.6
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand from Tej A.I.")
            return ""
        except sr.RequestError as e:
            print(f"Request failed; {e}")
            return ""

def writeNotepad(content):
    pyautogui.typewrite(content)

def saveNotepad():
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)
    pyautogui.press('enter')

# Function to greet based on the time of day
def wishme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        say("Good Morning sir")
    elif 12 <= hour < 18:
        say("Good Afternoon sir")
    else:
        say("Good Evening sir")

    say("Hello, I am Tej A.I")

def detect_objects():
    config_file = "C:\\Users\\saite\\Downloads\\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"  #make sure download this file
    frozen_model = "C:\\Users\\saite\\Downloads\\frozen_inference_graph.pb" #make sure download this file
    labels_file = "C:\\Users\\saite\\Downloads\\labels.txt"  #make sure download this file

    net = cv2.dnn_DetectionModel(frozen_model, config_file)

    with open(labels_file, 'rt') as f:
        labels = f.read().rstrip('\n').split('\n')

    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        classes, confidences, boxes = net.detect(frame, confThreshold=0.5)

        for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
            label = f'{labels[classId - 1]}: {confidence:.2f}%'
            cv2.rectangle(frame, box, color=(0, 255, 0), thickness=2)
            cv2.putText(frame, label, (box[0], box[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('Object Detection', frame)

        if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()

def send_mail():
    say("Sure, I will help you send an email. Please provide details.")
    receiver_email = "receivermail@gmail.com" #replace 
    say("Please say the subject of the email.")
    subject = takeCommand()

    # Speech recognition for message
    say("Please say the message of the email.")
    message = takeCommand()

    email = "sendermail@gmail.com"   #replace
    text = f"Subject:{subject}\n\n{message}"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(email, " email password ")  # Replace with your email password

    server.sendmail(email, receiver_email, text)

    say(f"Email has been sent to {receiver_email}")

def play_youtube_video(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)

if __name__ == '__main__':
    print("TEJ AI")
    wishme()  # Greet the user
    while True:
        print("Listening")
        text = takeCommand()
        command_matched = False

        # Add Generative AI response for every user command
        prompt = text
        response = model.generate_content(contents=[prompt])
        answer = response.text

        short_answer = answer[:100]

        print(f"TEJ AI Response: {short_answer}...")
        say(short_answer)
        command_matched = True

        if "open gmail" in text.lower():
            say("Opening Gmail...")
            webbrowser.open("https://mail.google.com/")
            command_matched = True

        elif "open file manager" in text.lower():
            say("Opening File Manager...")
            os.startfile("explorer.exe")
            command_matched = True

        elif "open browser" in text.lower():
            say("Opening Browser...")
            webbrowser.open("https://www.google.com/")
            command_matched = True

        elif "open notepad" in text.lower():
            say("Opening Notepad...")
            os.startfile("notepad.exe")
            command_matched = True
            say("Please provide the important points.")
            points_text = takeCommand()
            writeNotepad(points_text)
            command_matched = True

        elif "save it" in text.lower():
            say("Saving the content in Notepad...")
            saveNotepad()
            command_matched = True

        if "detect object" in text.lower():
            say("Detecting objects through the camera Sir...")
            detect_objects()
            command_matched = True

        if "play youtube video" in text.lower():
            say("Sure, what video would you like to watch?")
            video_query = takeCommand()
            play_youtube_video(video_query)
            command_matched = True

        if "send mail" in text.lower():
            send_mail()
            command_matched = True

        for site in [["youtube", "https://youtube.com"], ["wikipedia", "https://www.wikipedia.org"], ["google", "https://www.google.com"]]:
            if f"open {site[0]}".lower() in text.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
                command_matched = True
                break

        if "open music" in text.lower():
            musicPath = r"C:\Users\saite\perfect-beauty-191271.mp3"
            os.startfile(musicPath)
            command_matched = True

        if "the time" in text.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"sir the time is {strfTime}")
            command_matched = True

        if "open camera" in text.lower():
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Camera', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            command_matched = True

        # Your existing commands
        if "good morning" in text.lower():
            wishme()
            command_matched = True

        if "good afternoon" in text.lower():
            wishme()
            command_matched = True

        if "good evening" in text.lower():
            wishme()
            command_matched = True

        # ... (existing commands)

        if "exit" in text.lower():
            say("Exiting the program. Goodbye!")
            break

        # Windows Commands...
        # ... (existing commands)

        elif not command_matched:
            say("Sorry, I don't understand that command.")

        # Windows Commands ---->   
        if "shutdown" in text:
            say("Okay, shutting down the computer in 5 seconds....")
            os.system("shutdown /s /t 5 /c goodbye")
            command_matched = True

        if "restart" in text:
            say("Okay, restarting the computer in 5 seconds")
            os.system("shutdown /r /t 5")
            command_matched = True

        if "log out" in text:
            say("Okay, logging out....")
            os.system("shutdown /l")
            command_matched = True

        if "close" in text: 
            pyautogui.hotkey('alt', 'f4')
            command_matched = True

        if "disconnect wifi" in text:
            os.system("netsh wlan disconnect")
            say("WiFi disconnected")
            command_matched = True

        elif not command_matched:
            say("Sorry, I don't understand that command.")
