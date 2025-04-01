from google.oauth2 import service_account
from googleapiclient.discovery import build

def archive_google_drive(credentials_file, folder_id, output_dir):
    creds = service_account.Credentials.from_service_account_file(credentials_file)
    service = build('drive', 'v3', credentials=creds)
    os.makedirs(output_dir, exist_ok=True)
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=1000,
        fields="files(id, name, mimeType)"
    ).execute()
    for item in results.get('files', []):
        request = service.files().get_media(fileId=item['id'])
        with open(os.path.join(output_dir, item['name']), 'wb') as f:
            f.write(request.execute())
