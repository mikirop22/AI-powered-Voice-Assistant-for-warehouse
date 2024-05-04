
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment

import speech_recognition as sr
from pydub import AudioSegment

# Load the MP3 file
mp3_file = "tu_archivo.mp3"
audio = AudioSegment.from_mp3(mp3_file)

# Export the audio to WAV format
wav_file = "converted_audio.wav"
audio.export(wav_file, format="wav")

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

# Procesar el archivo de audio WAV
with sr.AudioFile(wav_file) as source:
    # Ajustar para el ruido ambiental
    recognizer.adjust_for_ambient_noise(source, duration=0.7)
    
    # Escuchar el archivo de audio
    audio = recognizer.record(source)
    
    try:
        # Reconocer el audio utilizando Google Speech Recognition
        text = recognizer.recognize_google(audio)
        print("Dijiste: {}".format(text))
    except sr.UnknownValueError:
        print("Lo siento, no pude entender el audio.")
    except sr.RequestError as e:
        print("Error ocurrido; {0}".format(e))
