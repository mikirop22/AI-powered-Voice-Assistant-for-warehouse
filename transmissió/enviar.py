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
file_metadata = {'name': 'list.csv'}
media = MediaFileUpload('list.csv', mimetype='text/csv')
file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

print('Archivo "list.csv" cargado correctamente con el ID:', file.get('id'))
