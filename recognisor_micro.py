import csv
import speech_recognition as sr
import numpy as np
import librosa
import pandas as pd

# Cargar el modelo entrenado
from tensorflow.keras.models import load_model

model = load_model("model.h5")
# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

# Función para reconocer la palabra con el modelo entrenado i relacionar-la con los datos del producto de la base de datos
def recognize_custom(audio):
    # Convertir el audio capturado por el micrófono en características (MFCC)
    mfccs = extract_features_from_audio(audio)
    
    
    # Predecir utilizando tu modelo entrenado
    prediction = model.predict_classes(mfccs)
    
    # Imprimir la palabra predicha (o hacer lo que desees con la predicción)
    print("Palabra predicha con el modelo entrenado:", prediction)

# Función para extraer características (MFCC) del audio
def extract_features_from_audio(audio):
    # Convertir el audio a matriz numérica
    audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)
    
    # Extraer características (MFCC) del audio
    mfccs = librosa.feature.mfcc(y=audio_data, sr=audio.sample_rate, n_mfcc=13)
    return mfccs

def agregar_producto(name, input_csv, output_csv):
    # Lista para almacenar las filas completas
    filas_completas = []

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
                audio = recognizer.listen(mic)
                product = recognize_custom(audio)
                agregar_producto(product, products_new, )
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))

# La llista generada s'ha de guardar i pujar d'alguna manera al núbol, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem