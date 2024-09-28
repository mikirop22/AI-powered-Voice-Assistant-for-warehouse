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

# Solicita al usuario que ingrese el nombre e ID del archivo
list_name = input("Por favor, ingresa el nombre de la lista: ")
list_id = input("Por favor, ingresa el ID de la lista: ")

# Directorio donde deseas guardar el archivo
directory = 'transmissió/'

# Ruta completa del archivo con el nombre proporcionado por el usuario
file_path = os.path.join(directory, f'{list_name}.csv')

# Descarga el archivo con el nombre proporcionado por el usuario desde Google Drive
request = drive_service.files().get_media(fileId=list_id)
with open(file_path, 'wb') as fh:
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()

print(f'Archivo "{list_name}.csv" descargado correctamente.')

