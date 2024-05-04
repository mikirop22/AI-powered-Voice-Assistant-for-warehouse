import speech_recognition as sr

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

# Función para reconocer la siguiente palabra con el modelo entrenado
def recognize_custom(audio):


    print("Palabra reconocida con el modelo entrenado: {}".format(audio))



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
            if text.lower() == "salir":
                break
                
            # Si se detecta "añadir", se espera la siguiente palabra
            if text.lower() == "añadir":
                print("Escuchando siguiente palabra...")
                audio = recognizer.listen(mic)
                recognize_custom(audio)
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")
        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))
