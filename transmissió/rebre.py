from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload

# Define las credenciales
credentials = Credentials.from_service_account_file('subtle-circlet-422322-b5-50795e26a89a.json')

# Autentica con las credenciales
drive_service = build('drive', 'v3', credentials=credentials)

# Solicita al usuario que ingrese el ID del archivo 'list.csv'
file_id = input("Por favor, ingresa el ID de la lista: ")

# Descarga el archivo 'list.csv' de Google Drive
request = drive_service.files().get_media(fileId=file_id)
fh = open('list.csv', 'wb')
downloader = MediaIoBaseDownload(fh, request)
done = False
while not done:
    status, done = downloader.next_chunk()

print('Archivo "list.csv" descargado correctamente.')

