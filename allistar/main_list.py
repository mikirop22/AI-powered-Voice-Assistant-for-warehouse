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

# Inicializa el motor TTS
engine = pyttsx3.init()

# Configura la voz en español
voices = engine.getProperty('voices')
for voice in voices:
    if 'spanish' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 150)

def speak(text):
        
    engine.say(text)
    engine.runAndWait()

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
    
    # Ruta completa del archivo dentro de la carpeta "treballador"
    ruta = f"treballador/{output_csv}"
    
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
            if row['cleaned_name'] == name:
                id = row['id']
                if 'stock' in row and int(row['stock']) < cantidad:
                    speak(f"¡Advertencia! La cantidad seleccionada ({cantidad}) supera el stock disponible ({row['stock']}) para el producto '{name}'.")
                    stock_superado = True
                    break

        if not stock_superado:
            row['cantidad'] = cantidad
            output_row = {'id': id, 'cantidad': cantidad}  # Selección de columnas para cada fila
            writer.writerow(output_row)
            print(f"Se ha añadido el elemento con el nombre '{name}' y la cantidad '{cantidad}' en el archivo '{output_csv}'.")


ruta_archivo = "allistar/diccionario.json"
with open(ruta_archivo, "r") as archivo:
    mapeo_palabras = json.load(archivo)




# Añadir más valores a las claves existentes en el diccionario mapeo_palabras
mapeo_palabras["OTINET_125mililitros"].extend(["otinet 125ml", "otinet 125mililitros", "otinet"])
mapeo_palabras["DEPO_MODERIN_5mililitros"].extend(["depo modern 5ml", "depo moderin 5ml", "depo modern", "depo moderin", "depo"])
mapeo_palabras["VETREGUL_GEL_50mililitros"].extend(["vertegui gel 50ml", "vertegui gel 50", "vertegui", "gel 50ml", "gel 50"])

enviar = False

lista_creada = False
activar = True
while True:
    print('Escuchando...')
    with sr.Microphone() as mic:
        if activar:
            speak("¿En que puedo ayudarte?")
            activar = False
            recognizer.adjust_for_ambient_noise(mic, duration=0.4)
            audio = recognizer.listen(mic)
        
        else:
            speak("¿Que más quieres hacer?")    
            recognizer.adjust_for_ambient_noise(mic, duration=0.4)
            audio = recognizer.listen(mic)

        try:
            # Reconocer el audio utilizando Google Speech Recognition
            text = recognizer.recognize_google(audio, language="es-ES")
            print("Dijiste: {}".format(text))
            
            # Si se detecta "salir", se rompe el bucle
            if "salir" in text.lower():
                break

            elif "crear" in text.lower() and "lista" in text.lower():
                print("Creando lista...")
                speak("Que nombre le quieres poner a la lista?")
                audio = recognizer.listen(mic)
                nombre_lista = recognizer.recognize_google(audio, language="es-ES")
                speak(f"El nombre de la lista es: {nombre_lista}")
                ruta = f'{nombre_lista}.csv'
                lista_creada = True

            
            elif lista_creada:    
                # Si se detecta "añadir", se espera la siguiente palabra
                if "añadir" in text.lower():
                    speak("Escuchando producto")
                    audio = recognizer.listen(mic)
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
                        
                    else:
                        print(f"No se encontró una palabra técnica para '{text}'")
                    
                    finish = False
                    while not finish:
                        speak("¿Es correcto? ")
                        print("¿Es correcto? (sí/no)")
                        resposta = False
                        while not resposta:
                            try:    
                                audio = recognizer.listen(mic)
                                response = recognizer.recognize_google(audio, language="es-ES")
                                resposta = True
                            
                            except sr.UnknownValueError:
                                    speak("Lo siento, no te pude entender. ¿Podrías decir: Sí si es correcto o No si no es correcto?")
                            
                        if "salir" in response.lower():
                            finish = True
                            break

                        elif "si" in response.lower() or "sí" in response.lower():
                            cantidad = True
                            while cantidad:
                                speak("¿Qué cantidad quieres? ")
                                audio = recognizer.listen(mic)
                                cantidad = recognizer.recognize_google(audio, language="es-ES")
                                print(cantidad)

                                try:
                                    cantidad_entero = int(cantidad)
                                    speak(f"La cantidad es: {cantidad_entero}")
                                    print(f'La cantidad es: {cantidad_entero}')
                                    # Aquí puedes usar cantidad_entero como un número entero
                                    # Por ejemplo, puedes usarlo para agregar el producto con la cantidad
                                    # Agregar el producto según tu implementación
                                    agregar_producto(palabra_tecnica, cantidad_entero, "products_new.csv", ruta)
                                    print("Producto añadido exitosamente.")
                                    cantidad = False
                                
                                except ValueError:
                                    print("La cantidad ingresada no es un número entero válido. Por favor, intenta de nuevo.")

                        
                            finish = True

                        elif "no" in response.lower():
                            finish = True
                        
                        else:
                            print("No entiendo la respuesta, por favor intenta de nuevo.")
                        
                        
                elif "eliminar ultima" in text.lower():
                    speak("Eliminando el último producto")
                    # Eliminar el último producto de la lista
                    eliminar_ultimo_producto(ruta)
                
                elif "terminar" in text.lower():
                    speak(f"Enviando lista {nombre_lista}")
                    enviar = True
                    break
                
                else:
                    speak(f'Lo siento, esa orden no está disponible')
                
        except sr.UnknownValueError:
            speak("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))




if enviar:
    # ENVIAR LA LLISTA A GOOGLE DIRVE, per tal que es pugui accedir de forma fàcil desde la terminal del treballador del magatzem
    from googleapiclient.discovery import build
    from google.oauth2.service_account import Credentials
    from googleapiclient.http import MediaFileUpload
    import os
    import json
    
    # Accede al secreto desde la variable de entorno
    service_account_info = os.getenv("GOOGLE_CLOUD_KEY")
    
    # Cargar el secreto como un JSON
    if service_account_info:
        credentials_dict = json.loads(service_account_info)
        credentials = Credentials.from_service_account_info(credentials_dict)
    else:
        raise Exception("Service account credentials not found.")

    # Autentica con las credenciales
    drive_service = build('drive', 'v3', credentials=credentials)
    
    # Carga el archivo 'list.csv' a Google Drive
    file_metadata = {'name': ruta}
    media = MediaFileUpload(ruta, mimetype='text/csv')
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

    print(f'Archivo "{nombre_lista}.csv" cargado correctamente con el ID:', file.get('id'))
