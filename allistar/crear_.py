import speech_recognition as sr
from pydub import AudioSegment
import os
import json

# Cargar el archivo MP3
def reconocer_audio(mp3_file, producto, mapeo_palabras):
    audio = AudioSegment.from_mp3(mp3_file)

    # Convertir el audio a formato WAV (u otro formato compatible)
    wav_file = "audio_converted.wav"
    audio.export(wav_file, format="wav")

    # Inicializar el reconocedor de voz
    recognizer = sr.Recognizer()

    # Leer el archivo WAV
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)

        try:
            # Reconocer el texto utilizando Google Speech Recognition
            texto = recognizer.recognize_google(audio_data, language="es-ES")
            mapeo_palabras[producto].append(texto)
        except sr.UnknownValueError:
            print("Google Speech Recognition no pudo entender el audio")
        except sr.RequestError as e:
            print("Error al solicitar resultados de Google Speech Recognition:", e)

import pandas as pd

# Crear mapeo inicial con productos y palabras asociadas
mapeo_palabras_inicial = {
    "OTINET 125mililitros": ["otinet 125 ml"],
    "DEPO MODERIN 5mililitros": ["de pomo 5 ml", "depo modern 5 ml", "pepo modern 5 ml", "Depo modeling 5 ml", "Depo mothering 5 ml"],
    "VETREGUL GEL 50mililitros": ["vertegui gel 50 ml"]
}

# Leer el archivo CSV
df = pd.read_csv('products_with_audio.csv')

# Inicializar mapeo_palabras con todas las palabras de la columna name
mapeo_palabras = {producto.replace(' ', '_').replace('.', ''): [] for producto in df["cleaned_name"]}

print(mapeo_palabras)

# Fusionar los dos mapeos
for producto, palabras in mapeo_palabras_inicial.items():
    if producto in mapeo_palabras:
        mapeo_palabras[producto].extend(palabras)
    else:
        mapeo_palabras[producto] = palabras

directorio = "audios/"
for audio in os.listdir(directorio):
    print(f"Procesando archivo: {audio}")
    producto = audio.split(".")[0]
    reconocer_audio(directorio + audio, producto, mapeo_palabras)

print("Mapeo de palabras:")
for producto, palabras in mapeo_palabras.items():
    print(f"{producto}: {palabras}")
    
# Ruta del archivo donde se guardará el diccionario
ruta_archivo = "diccionario.json"

# Guardar el diccionario en el archivo
with open(ruta_archivo, "w") as archivo:
    json.dump(mapeo_palabras, archivo)