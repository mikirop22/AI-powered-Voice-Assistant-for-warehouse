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

df = pd.read_csv('products_with_audio_updated.csv')
for i, _ in enumerate(df['id']):
    df.at[i, 'id'] = i

import speech_recognition as sr

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()


def recognize_custom(audio):
    
    def pad_mfcc(mfcc, max_length):
        # Si la longitud de la secuencia es menor que la longitud máxima, rellenar con ceros
        if mfcc.shape[1] < max_length:
            pad_width = max_length - mfcc.shape[1]
            mfcc = np.pad(mfcc, ((0, 0), (0, pad_width)), mode='constant', constant_values=(0,))
        # Si la longitud de la secuencia es mayor que la longitud máxima, trunca la secuencia
        elif mfcc.shape[1] > max_length:
            mfcc = mfcc[:, :max_length]
        return mfcc
    
    # Guardar el audio en un archivo temporal en formato WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_audio:
        tmp_audio.write(audio.get_wav_data())
        tmp_audio_name = tmp_audio.name

    # Cargar el archivo de audio con librosa
    audio, sr = librosa.load(tmp_audio_name, sr=None)

    # Ahora puedes utilizar `audio` y `sr` para extraer características de audio como los MFCCs
    mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

    max_length = mfccs.shape[1]

    # Aplicar la función de relleno/truncado a las características MFCCs
    input_padded = pad_mfcc(mfccs, max_length)

    input_array = np.expand_dims(input_padded, axis=0)  # Añadir dimensión de lote
    
    # Realizar la predicción con el modelo cargado
    predictions = loaded_model.predict(input_array)

    # Obtener la clase predicha (índice de la clase con probabilidad más alta)
    predicted_class = np.argmax(predictions)

    # Obtener el nombre de la clase predicha usando el índice
    name_value = df.loc[df['id'] == predicted_class, 'name'].values[0]

    print(f"Palabra reconocida con el modelo entrenado: {name_value}")
    
    return mfccs




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
            if text.lower() == "salir":
                break
                
            # Si se detecta "añadir", se espera la siguiente palabra
            if "añadir" in text.lower():
                print("Escuchando siguiente palabra...")
                audio = recognizer.listen(mic)
                recognize_custom(audio)
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")
        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))
