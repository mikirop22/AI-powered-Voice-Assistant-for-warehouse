import csv
import os
import tempfile

from gtts import gTTS
import pygame
from magatzem import Warehouse
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import pyttsx3
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload
import os
import json

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()

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

#DESCARREGAR LA LLISTA
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


trobat = False
while not trobat:
    speak("Por favor, comuníqueme el nombre de la lista: ")
    with sr.Microphone() as mic:
        try:
            recognizer.adjust_for_ambient_noise(mic, duration=0.3)
            audio = recognizer.listen(mic)
            
            list_name = recognizer.recognize_google(audio, language="es-ES")
            print("Dijiste: {}".format(list_name))

            if "salir" in list_name.lower():
                break
            
            else:
                # Directorio donde deseas guardar el archivo
                directory = 'treballador/'

                # Ruta completa del archivo con el nombre proporcionado por el usuario
                file_path = os.path.join(directory, f'{list_name}.csv')
                
                trobat = True
                
        except sr.UnknownValueError:
            speak("Lo siento, no pude entender el audio.")

        except sr.RequestError as e:
            print("Error ocurrido; {0}".format(e))


speak("Por favor, ingresa el ID de la lista: ")
list_id = input("Por favor, ingresa el ID de la lista: ")

# Descarga el archivo con el nombre proporcionado por el usuario desde Google Drive
request = drive_service.files().get_media(fileId=list_id)
with open(file_path, 'wb') as fh:
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

#speak(f'Archivo "{list_name}.csv" descargado correctamente.')

magatzem = [[[0, None, 0] for _ in range(10)] for _ in range(10)]
for fila in magatzem:
    fila.append([None, None, None])

for fila in magatzem:
    fila.insert(0, [None, None, None])
    
with open('products_new.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Salta la primera fila (encapçalament)
    for row in reader:
        product_id = row[0]
        fila = int(row[3])-1  # Les files comencen des de 1, però l'índex de la llista comença des de 0
        columna = int(row[4])  # Les columnes comencen des de 1, però l'índex de la llista comença des de 0
        if row[5] == 'L':
            costat = 0
        elif row[5] == 'R':
            costat = 2
        magatzem[fila][columna][costat] = product_id  # Reemplaza el valor en la posición 2 de la lista

warehouse = Warehouse(12, 10, magatzem)

# Llegeix les dades del document products_new.csv i guarda les ubicacions dels productes
product_locations = {}
noms = {}
with open('products_new.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    next(reader)  # Salta la primera fila (encapçalament)
    for row in reader:
        product_id = row[0]
        fila = int(row[3]) 
        columna = int(row[4]) 
        product_locations[product_id] = (fila, columna)
        nom = row[1]
        noms[product_id] = nom

# Selecciona els productes de la llista a recollir
product_ids = []
nom_quantitas_pos = {}
with open(f'treballador/{list_name}.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        product_id = row[0]
        product_ids.append(product_id)
        quantitat = row[1]
        pos = product_locations[product_id]
        nom_quantitas_pos[product_id] = [noms[product_id], quantitat, (pos[0], pos[1])]

print("Productes seleccionats:")
for product_id in product_ids:
    print("- ID:", product_id)

# Allista els productes seleccionats
for product_id in product_ids:
    
    (x,y) = product_locations[product_id]
    warehouse.add_pick_location(x,y)
    warehouse.add_pick_location_id((x,y),product_id)

# Busca i visualitza el camí mínim per recollir els productes seleccionats al magatzem
print("\nCamí mínim per recollir els productes:")
start_x, start_y = 0, 0
final_x, final_y = 11, 11
path = warehouse.find_min_path(start_x, start_y, final_x, final_y)

if path is not None:
    warehouse.visualize_path(path, nom_quantitas_pos)
else:
    speak("No se encontró un camino válido.")
