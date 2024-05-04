import csv
import speech_recognition as sr
import numpy as np
import librosa
<<<<<<< HEAD
from pydub import AudioSegment
=======
import pandas as pd
>>>>>>> 08bdc8fb1da43d3a85cad077b497424ef80b085d

model = 
# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

# Función para reconocer la palabra con el modelo entrenado i relacionar-la con los datos del producto de la base de datos
def recognize_custom(audio):
    # Convertir el audio capturado por el micrófono en características (MFCC)
    mfccs = extract_features(audio)

    # Predecir utilizando tu modelo entrenado
    prediction = model.predict_classes(mfccs)
    
    # Imprimir la palabra predicha (o hacer lo que desees con la predicción)
    print("Palabra predicha con el modelo entrenado:", prediction)

def extract_features(audio_path):
    # Aquí puedes usar librosa para extraer características de audio, como los coeficientes cepstrales en frecuencia (MFCC)
    audio, sr = librosa.load(audio_path, sr=None)
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    return mfccs

def agregar_producto(name, input_csv, output_csv):
    # Lista para almacenar las filas completas
    filas_completas = []

<<<<<<< HEAD
=======
    # Leer el archivo CSV de entrada y añadir los parámetros completos a la lista
    with open(input_csv, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            if row['name'] == name:
                filas_completas.append(row)

    # Si no se encontró ningún producto con el nombre dado, salir de la función
    if not filas_completas:
        print(f"No se encontró ningún producto con el nombre '{name}' en el archivo CSV.")
        return

    # Escribir los parámetros completos en un nuevo archivo CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=filas_completas[0].keys(), delimiter=';')
        writer.writeheader()
        for row in filas_completas:
            writer.writerow(row)

    print(f"Se ha añadido el elementos con el nombre '{name}' en el archivo '{output_csv}'.")

>>>>>>> 08bdc8fb1da43d3a85cad077b497424ef80b085d

while True:
    with sr.Microphone() as mic:
        print("Di algo...")
        recognizer.adjust_for_ambient_noise(mic, duration=0.7)
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
<<<<<<< HEAD
                audio = recognizer.listen(mic, timeout=None)
                print("Grabación finalizada.")

                # Guardar el audio en formato WAV
                with open("audio_temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Convertir el audio a formato MP3
                sound = AudioSegment.from_wav("audio_temp.wav")
                sound.export("audio_temp.mp3", format="mp3")
                
                # Llamar a la función recognize_custom con el audio en formato MP3
                recognize_custom("audio_temp.mp3")
            
=======
                audio = recognizer.listen(mic)
                product = recognize_custom(audio)
                agregar_producto(product, products_new, )
>>>>>>> 08bdc8fb1da43d3a85cad077b497424ef80b085d
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))

# La llista generada s'ha de guardar i pujar d'alguna manera al núbol, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem