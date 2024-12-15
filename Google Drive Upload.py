#pip install google-auth google-auth-oauthlib google-auth-httplib2
#pip install google-api-python-client
#pip install pydrive

import os
import io
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.service_account import Credentials

# Pfad zur JSON-Datei mit den Anmeldeinformationen
credentials_path = r'C:\Users\bienendaten.json'

# Google Drive API initialisieren
credentials = Credentials.from_service_account_file(credentials_path)
drive_service = build('drive', 'v3', credentials=credentials)

def upload_image_to_drive(image_path, folder_id):
    # Dateiname extrahieren
    file_name = os.path.basename(image_path)

    # Bild als Dateiobjekt öffnen
    image_file = open(image_path, 'rb')

    # Medien-Upload vorbereiten
    media = MediaIoBaseUpload(image_file, mimetype='image/jpeg')

    # Datei-Metadaten erstellen
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    # Medien-Upload durchführen
    response = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Dateiobjekt schließen
    image_file.close()

    print(f'Die Datei {file_name} wurde erfolgreich hochgeladen. Datei-ID: {response["id"]}')

# Beispielaufruf der Funktion Bilder Hochladen
image_path = r'C:\.jpg'  # Pfad zu Ihrem Bild
folder_id = '1vgjhvcg'  # ID des Zielordners auf Google Drive
upload_image_to_drive(image_path, folder_id)


