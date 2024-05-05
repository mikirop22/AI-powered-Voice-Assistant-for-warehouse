import csv
import os
import speech_recognition as sr
import numpy as np
import librosa
import pandas as pd
import difflib

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

def recognize_custom(audio):
    pass

def agregar_producto(name, cantidad, input_csv, output_csv):
    # Determinar si el archivo de salida existe y está vacío
    output_exists_and_empty = os.path.isfile(output_csv) and os.stat(output_csv).st_size == 0

    # Leer el archivo CSV de entrada y escribir las filas en el archivo de salida
    with open(input_csv, 'r', newline='', encoding='utf-8') as input_file, \
         open(output_csv, 'a', newline='', encoding='utf-8') as output_file:
        
        reader = csv.DictReader(input_file, delimiter=';')
        fieldnames = ['id', 'cantidad']  # Selección de columnas para el archivo de salida
        writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=';')

        # Escribir el encabezado solo si el archivo de salida no existe o está vacío
        if output_exists_and_empty:
            writer.writeheader()

        # Verificar si la cantidad seleccionada no supera el stock
        stock_superado = False
        for row in reader:
            if row['name'] == name:
                if 'stock' in row and int(row['stock']) < cantidad:
                    print(f"¡Advertencia! La cantidad seleccionada ({cantidad}) supera el stock disponible ({row['stock']}) para el producto '{name}'.")
                    stock_superado = True
                    break

        if not stock_superado:
            row['cantidad'] = cantidad
            output_row = {'id': row['id'], 'cantidad': cantidad}  # Selección de columnas para cada fila
            writer.writerow(output_row)
            print(f"Se ha añadido el elemento con el nombre '{name}' y la cantidad '{cantidad}' en el archivo '{output_csv}'.")




# Definir el mapeo entre palabras técnicas y palabras reconocidas por Google
mapeo_palabras = {
    "OTINET 125mililitros": ["otinet 125 ml"],
    "DEPO MODERIN 5mililitros": ["de pomo 5 ml", "depo modern 5 ml", "pepo modern 5 ml", "Depo modeling 5 ml", "Depo mothering 5 ml"],
    "VETREGUL GEL 50mililitros": ["vertegui gel 50 ml"]
}


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

            if "crear lista" in text.lower():
                print("Pon un nombre a la lista. Te escucho")
                audio = recognizer.listen(mic)
                list_name = recognizer.recognize_google(audio, language="es-ES")
                print(f"Tu lista se llama: {list_name}. Ahora puedes añadir productos con la palabra AÑADIR")


                # Dentro del bloque try:
                # Buscar la palabra reconocida en el diccionario
                done = False
                for tecnica, reconocidas in mapeo_palabras.items():
                    if text in reconocidas:
                        palabra_tecnica = tecnica
                        done = True
                        break
                # Si no se encuentra una coincidencia exacta, buscar la palabra más cercana
                if done == False:
                    closest_match = difflib.get_close_matches(text, [word for sublist in mapeo_palabras.values() for word in sublist], n=1)
                    if closest_match:
                        palabra_tecnica = closest_match[0]
                        # Convertir la palabra técnica en la palabra original
                        for tecnica, reconocidas in mapeo_palabras.items():
                            if palabra_tecnica in reconocidas:
                                palabra_tecnica = tecnica
                                break   
                        print(f"No se encontró una coincidencia exacta para '{text}'. La palabra más cercana es '{palabra_tecnica}'")
                        

                # Si se detecta "añadir", se espera la siguiente palabra
                if "añadir" in text.lower():
                    print("Escuchando siguiente palabra...")
                    audio = recognizer.listen(mic, timeout=None)
                    text = recognizer.recognize_google(audio, language="es-ES")
                    print("Grabación finalizada.")
                    print("Dijiste: {}".format(text))

                    # Buscar la palabra reconocida en el diccionario
                    for tecnica, reconocidas in mapeo_palabras.items():
                        if text in reconocidas:
                            palabra_tecnica = tecnica
                            break

                    if palabra_tecnica is not None:
                        print(f"Palabra técnica correspondiente a '{text}': {palabra_tecnica}")
                        print(f"Producto detectado: {palabra_tecnica}")
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
                                agregar_producto(palabra_tecnica, "products_new.csv", "list.csv")
                                print("Producto añadido exitosamente.")
                                x = False

                            elif "no" in response.lower():
                                pass
                        
                    else:
                        print(f"No se encontró una palabra técnica para '{text}'")
                    
                    # Comprobar si el producto es correcto
                    print(f"Producto detectado: {product_name}")
                    print("¿Es correcto? (sí/no)")
                    audio = recognizer.listen(mic)
                    response = recognizer.recognize_google(audio, language="es-ES")
                    x  =  True
                    while x:
                        if "salir" in response.lower():
                            break
                        if "sí" or "Sí" in response.lower():
                            print("Que cantidad quieres?")
                            audio = recognizer.listen(mic)
                            cantidad = recognizer.recognize_google(audio, language="es-ES")
                            print(f"La cantidad es: {cantidad}")
                            # Añadir la cantidad tambieeen!!!
                            agregar_producto(product_name, cantidad, "products.csv", "list.csv")
                            agregar_producto(palabra_tecnica, cantidad, "products_new.csv", "productos_nuevos.csv")
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
                
                if "enviar"
                
        except sr.UnknownValueError:
            print("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))



# ENVIAR LA LLISTA A GOOGLE DIRVE, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

# Define las credenciales
credentials = Credentials.from_service_account_file('subtle-circlet-422322-b5-50795e26a89a.json')

# Autentica con las credenciales
drive_service = build('drive', 'v3', credentials=credentials)

# Carga el archivo 'list.csv' a Google Drive
file_metadata = {'name': 'productos_nuevos.csv'}
media = MediaFileUpload('productos_nuevos.csv', mimetype='text/csv')
file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

print('Archivo "productos_nuevos.csv" cargado correctamente con el ID:', file.get('id'))
print('Archivo "list.csv" cargado correctamente con el ID:', file.get('id'))
