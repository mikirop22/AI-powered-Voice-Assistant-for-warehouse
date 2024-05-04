import csv
import speech_recognition as sr
import numpy as np
import librosa

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


<<<<<<< HEAD

=======
    print("Palabra reconocida con el modelo entrenado: {}".format(audio))
>>>>>>> af6b57d00b4a9ca3f9f2a4f5522039a38b290efa


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
<<<<<<< HEAD
                recognize_custom(audio)
                print("Palabra añadida.")
            
=======
                product = recognize_custom(audio)
>>>>>>> af6b57d00b4a9ca3f9f2a4f5522039a38b290efa
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))

# La llista generada s'ha de guardar i pujar d'alguna manera al núbol, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem