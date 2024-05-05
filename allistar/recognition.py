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

max_length = 1463

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

# Función para reconocer la palabra con el modelo entrenado i relacionar-la con los datos del producto de la base de datos
def recognize_custom(audio):
    
    # Función para extraer características (MFCC) del audio
    def extract_features(audio_path):
        # Cargar el archivo de audio y extraer características
        audio, sr = librosa.load(audio_path, sr=None)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        return mfccs
    
    # Convertir el audio capturado por el micrófono en características (MFCC)
    mfccs = extract_features(audio)
    
    def pad_mfcc(mfcc, max_length):
        # Si la longitud de la secuencia es menor que la longitud máxima, rellenar con ceros
        if mfcc.shape[1] < max_length:
            pad_width = max_length - mfcc.shape[1]
            mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant', constant_values=(0,))
        # Si la longitud de la secuencia es mayor que la longitud máxima, trunca la secuencia
        elif mfcc.shape[1] > max_length:
            mfcc = mfcc[:, :max_length]
        return mfcc

    # Aplicar la función de relleno/truncado a cada secuencia de MFCCs
    mfccs_padded = np.array([pad_mfcc(mfccs, max_length)])

    mfccs_array = np.array(mfccs_padded)
    
    mfccs_array_flat = mfccs_array.reshape(mfccs_array.shape[0], -1)

    # Predecir utilizando tu modelo entrenado
    prediction = loaded_model.predict(mfccs_array_flat)
    
    # Obtener la clase predicha (índice de la probabilidad más alta)
    predicted_class_index = np.argmax(prediction)

    # Imprimir la palabra predicha (o hacer lo que desees con la predicción)
    print("Palabra predicha con el modelo entrenado:", predicted_class_index)




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
                recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = recognizer.listen(mic)
                print("Grabación finalizada.")

                # Guardar el audio en formato WAV
                with open("audio_temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Convertir el audio a formato MP3
                sound = AudioSegment.from_wav("audio_temp.wav")
                sound.export("audio_temp.mp3", format="mp3")
                
                # Llamar a la función recognize_custom con el audio en formato MP3
                recognize_custom("audio_temp.mp3")
            
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))

# La llista generada s'ha de guardar i pujar d'alguna manera al núbol, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem