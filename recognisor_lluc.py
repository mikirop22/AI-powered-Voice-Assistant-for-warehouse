
import speech_recognition as sr
import pyttsx3

recogniser = sr.Recognizer()

while True:
    with sr.Microphone() as mic:
        print("Say something")
        recogniser.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recogniser.listen(mic)

        try:
            text = recogniser.recognize_google(audio)
            print("You said: {}".format(text))
            if text == "exit":
                break
        except:
            print("Sorry, I could not recognize what you said")
            recogniser = sr.Recognizer()
            continue
