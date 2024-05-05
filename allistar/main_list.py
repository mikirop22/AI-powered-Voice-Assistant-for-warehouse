import csv
import os
import tempfile
import speech_recognition as sr
import numpy as np
import librosa
import pandas as pd
import difflib
import json
import pyttsx3
from gtts import gTTS
from pydub.playback import play


from pydub import AudioSegment

def speak(text):
    # Crear el objeto gTTS
    tts = gTTS(text, lang='es')

    # Crear un archivo temporal para almacenar el audio
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
        temp_audio_path = temp_audio.name
        tts.save(temp_audio_path)

        # Cargar el audio como un segmento de audio
        audio_segment = AudioSegment.from_mp3(temp_audio_path)

        # Reproducir el audio
        play(audio_segment)

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

def eliminar_ultimo_producto(output_csv):
    # Leer el archivo CSV de salida y eliminar la última fila
    with open(output_csv, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file, delimiter=';')
        rows = [row for row in reader]

    if rows:
        with open(output_csv, 'w', newline='', encoding='utf-8') as output_file:
            fieldnames = ['id', 'cantidad']
            writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(rows[:-1])
            print("Se ha eliminado el último elemento del archivo '{output_csv}'.")

    else:
        print("No hay elementos para eliminar en el archivo '{output_csv}'.")

    

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


ruta_archivo = "allistar/diccionario.json"
with open(ruta_archivo, "r") as archivo:
    mapeo_palabras = json.load(archivo)




# Añadir más valores a las claves existentes en el diccionario mapeo_palabras
mapeo_palabras["OTINET 125mililitros"].extend(["otinet 125ml", "otinet 125mililitros", "otinet"])
mapeo_palabras["DEPO MODERIN 5mililitros"].extend(["depo modern 5ml", "depo moderin 5ml", "depo modern", "depo moderin", "depo"])
mapeo_palabras["VETREGUL GEL 50mililitros"].extend(["vertegui gel 50ml", "vertegui gel 50", "vertegui", "gel 50ml", "gel 50"])

enviar = False

lista_creada = False
activar = True
while True:
    with sr.Microphone() as mic:
        if activar:
            speak("¿En que puedo ayudarte?")
            activar = False
            recognizer.adjust_for_ambient_noise(mic, duration=0.3)
            audio = recognizer.listen(mic)
        
        else:
            speak("¿Que más quieres hacer?")    
            recognizer.adjust_for_ambient_noise(mic, duration=0.3)
            audio = recognizer.listen(mic)

        try:
            # Reconocer el audio utilizando Google Speech Recognition
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Dijiste: {}".format(text))
            
            # Si se detecta "salir", se rompe el bucle
            if "salir" in text.lower():
                break

            if "crear lista" in text.lower():
                print("Creando lista...")
                speak("Que nombre le quieres poner a la lista?")
                audio = recognizer.listen(mic)
                nombre_lista = recognizer.recognize_google(audio, language="es-ES")
                speak(f"El nombre de la lista es: {nombre_lista}")
                lista_creada = True

            
            if lista_creada:    
                # Si se detecta "añadir", se espera la siguiente palabra
                if "añadir" in text.lower():
                    speak("Escuchando producto")
                    audio = recognizer.listen(mic, timeout=None)
                    text = recognizer.recognize_google(audio, language="es-ES")
                    print("Grabación finalizada")
                    print("Dijiste: {}".format(text))



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
                        else:
                            palabra_tecnica = None   

                    if palabra_tecnica is not None:
                        print(f"Palabra técnica correspondiente a '{text}': {palabra_tecnica}")
                        speak(f"Producto detectado: {palabra_tecnica}")
                        speak("¿Es correcto? ")
                        print("¿Es correcto? (sí/no)")
                        audio = recognizer.listen(mic)
                        response = recognizer.recognize_google(audio, language="es-ES")
                        
                        if "salir" in response.lower():
                            break
                        
                        if "si" in response.lower() or "sí" in response.lower():
                            speak("¿Qué cantidad quieres?")
                            audio = recognizer.listen(mic)
                            cantidad = recognizer.recognize_google(audio, language="es-ES")
                            print(f"La cantidad es: {cantidad}")
                            # ¡Añadir la cantidad también!
                            agregar_producto(palabra_tecnica, cantidad, "products_new.csv", "productos_nuevos.csv")
                            speak("Producto añadido exitosamente.")
                            x = False
                            
                        elif "no" in response.lower():
                            pass

                        
                    else:
                        print(f"No se encontró una palabra técnica para '{text}'")
                        
                if "eliminar ultima" in text.lower():
                    speak("Eliminando el último producto")
                    # Eliminar el último producto de la lista
                    eliminar_ultimo_producto("productos_nuevos.csv")
                
                if "terminar" in text.lower():
                    speak(f"Enviando lista {nombre_lista}")
                    enviar = True
                    break

                
        except sr.UnknownValueError:
            speak("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))




if enviar:
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
