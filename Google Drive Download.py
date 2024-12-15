import io
from googleapiclient.discovery import build #"pip3 install google-api-python-client"
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
#"https://console.cloud.google.com/?pli=1" "Webseite für die Json Datei"

# Datei-ID und Zielpfad angeben
file_id = 'bghhbg'  # ID der Datei auf Google Drive
destination_path = r'C:jpg'  # Zielpfad zum Speichern der heruntergeladenen Datei

# Google Drive API-Verbindung erstellen
credentials = service_account.Credentials.from_service_account_file(r'C:Bienendaten.json')
drive_service = build('drive', 'v3', credentials=credentials)

# Funktion zum Herunterladen der Datei von Google Drive
def download_image_from_drive(file_id, destination_path):
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download {int(status.progress() * 100)}% abgeschlossen.")

    print(f'Die Datei wurde erfolgreich heruntergeladen und gespeichert unter: {destination_path}')

# Datei von Google Drive herunterladen
download_image_from_drive(file_id, destination_path)


