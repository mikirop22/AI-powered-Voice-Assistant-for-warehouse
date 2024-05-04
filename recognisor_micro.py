import csv
import speech_recognition as sr
import numpy as np
import librosa
from pydub import AudioSegment

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
            
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))

# La llista generada s'ha de guardar i pujar d'alguna manera al núbol, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem