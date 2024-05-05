from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

# Define las credenciales
credentials = Credentials.from_service_account_file('subtle-circlet-422322-b5-50795e26a89a.json')

# Autentica con las credenciales
drive_service = build('drive', 'v3', credentials=credentials)

# Carga el archivo 'list.csv' a Google Drive
file_metadata = {'name': 'list.csv'}
media = MediaFileUpload('list.csv', mimetype='text/csv')
file = drive_service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()

print('Archivo "list.csv" cargado correctamente con el ID:', file.get('id'))