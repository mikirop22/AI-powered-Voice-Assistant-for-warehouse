import csv
import speech_recognition as sr
import numpy as np
import librosa
import pandas as pd

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

def recognize_custom(audio):
    pass



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
                audio = recognizer.listen(mic, timeout=None)
                print("Grabación finalizada.")

                # Guardar el audio en formato WAV
                with open("audio_temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                
                # Convertir el audio a formato MP3
                sound = AudioSegment.from_wav("audio_temp.wav")
                sound.export("audio_temp.mp3", format="mp3")
                
                # Llamar a la función recognize_custom con el audio en formato MP3
                product_name = recognize_custom("audio_temp.mp3")

                # Comprobar si el producto es correcto
                print(f"Producto detectado: {product_name}")
                print("¿Es correcto? (sí/no)")
                audio = recognizer.listen(mic)
                response = recognizer.recognize_google(audio, language="es-ES")
                x  =  True
                while x:
                    if "salir" in response.lower():
                        break
                    if "sí" in response.lower():
                        print("Que cantidad quieres?")
                        audio = recognizer.listen(mic)
                        cantidad = recognizer.recognize_google(audio, language="es-ES")
                        print(f"La cantidad es: {cantidad}")
                        # Añadir la cantidad tambieeen!!!
                        agregar_producto(product_name, "productos.csv", "productos_nuevos.csv")
                        print("Producto añadido exitosamente.")
                        x = False

                    elif "no" in response.lower():
                        print("Por favor, repita el nombre del producto.")
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
                        product_name = recognize_custom("audio_temp.mp3")





            
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))

# La llista generada s'ha de guardar i pujar d'alguna manera al núbol, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem