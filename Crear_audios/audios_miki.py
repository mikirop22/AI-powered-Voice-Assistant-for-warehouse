import os
from keras.models import load_model
import pickle
import librosa
import numpy as np
import pandas as pd
import tempfile


# Cargar el modelo
with open('modelo_entrenado.pkl', 'rb') as f:
    loaded_model = pickle.load(f)

df = pd.read_csv('products_with_audios_oficial.csv')
for i, _ in enumerate(df['id']):
    df.at[i, 'id'] = i

import csv
import speech_recognition as sr
import numpy as np
import librosa
from pydub import AudioSegment


ruta_audios = "audios_depo_moderin_5ml"

# Si la carpeta no existe, créala
if not os.path.exists(ruta_audios):
    os.makedirs(ruta_audios)

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

i = 1
while True:
    with sr.Microphone() as mic:
        print("Di algo...")
        recognizer.adjust_for_ambient_noise(mic, duration=0.5)
        audio = recognizer.listen(mic)

        try:
            # Reconocer el audio utilizando Google Speech Recognition
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Dijiste: {}".format(text))
            
            # Si se detecta "salir", se rompe el bucle
            if "salir" in text.lower():
                break
                
            # Si se detecta "añadir", se espera la siguiente palabra
            if "añadir" in text.lower():
                print("Escuchando siguiente palabra...")
                audio = recognizer.listen(mic)
                print("Grabación finalizada.")

                # Guardar el audio en formato WAV
                with open("audio_temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Convertir el audio a formato MP3
                sound = AudioSegment.from_wav("audio_temp.wav")
                sound.export("audio_temp.mp3", format="mp3")
                output_file = f"{i}.mp3"
                i += 1
                # Exporta el archivo de audio en formato mp3 en la ruta especificada
                sound.export(os.path.join(ruta_audios, output_file), format="mp3")
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))