"""
Google Drive Sync Script
Automatically downloads financial PDFs from Google Drive
"""

import os
import io
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import pickle
from config import FINANCIALS_DIR
from database import FinancialDatabase
from process_financials import process_pdf

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Google Drive folder ID (set this to your folder's ID)
DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID', None)


def get_google_drive_service():
    """Authenticate and return Google Drive service"""
    creds = None
    token_file = Path(__file__).parent / 'token.pickle'

    # Load existing credentials
    if token_file.exists():
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If credentials don't exist or are invalid, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Look for credentials.json file
            credentials_file = Path(__file__).parent / 'credentials.json'
            if not credentials_file.exists():
                print("❌ ERROR: credentials.json not found!")
                print("Please follow setup instructions in GOOGLE_DRIVE_SETUP.md")
                return None

            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_file), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def list_pdfs_in_folder(service, folder_id):
    """List all PDF files in the specified Google Drive folder"""
    if not folder_id:
        print("❌ ERROR: Google Drive folder ID not set!")
        print("Set GOOGLE_DRIVE_FOLDER_ID environment variable or edit this script.")
        return []

    query = f"'{folder_id}' in parents and mimeType='application/pdf' and trashed=false"

    try:
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, modifiedTime)',
            orderBy='modifiedTime desc'
        ).execute()

        files = results.get('files', [])
        return files
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return []


def download_file(service, file_id, file_name, destination_folder):
    """Download a file from Google Drive"""
    try:
        request = service.files().get_media(fileId=file_id)
        file_path = destination_folder / file_name

        fh = io.FileIO(file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"  Downloading... {progress}%", end='\r')

        print(f"  ✓ Downloaded: {file_name}")
        return file_path
    except Exception as e:
        print(f"  ✗ Error downloading {file_name}: {e}")
        return None


def sync_from_google_drive():
    """Main sync function"""
    print("=" * 70)
    print("Google Drive Sync - Mason's Famous Lobsters Financial Statements")
    print("=" * 70)

    # Get Google Drive service
    service = get_google_drive_service()
    if not service:
        return

    # Get folder ID
    folder_id = DRIVE_FOLDER_ID
    if not folder_id:
        print("\n❌ Google Drive folder ID not configured!")
        print("To configure:")
        print("1. Open your Google Drive folder in a browser")
        print("2. Copy the folder ID from the URL:")
        print("   https://drive.google.com/drive/folders/YOUR_FOLDER_ID_HERE")
        print("3. Set environment variable: export GOOGLE_DRIVE_FOLDER_ID='your_folder_id'")
        print("   Or edit this script and set DRIVE_FOLDER_ID")
        return

    print(f"\nScanning Google Drive folder: {folder_id}")

    # List PDFs in folder
    files = list_pdfs_in_folder(service, folder_id)

    if not files:
        print("\n✓ No new PDF files found in Google Drive folder")
        return

    print(f"\nFound {len(files)} PDF file(s) in Google Drive:")
    for f in files:
        print(f"  - {f['name']}")

    # Check which files already exist locally
    existing_files = set(f.name for f in FINANCIALS_DIR.glob("*.pdf"))

    # Download new files
    new_files = []
    for file in files:
        if file['name'] in existing_files:
            print(f"\n⏭  Skipping {file['name']} (already exists)")
        else:
            print(f"\n📥 Downloading {file['name']}...")
            downloaded_path = download_file(service, file['id'], file['name'], FINANCIALS_DIR)
            if downloaded_path:
                new_files.append(downloaded_path)

    # Process new files
    if new_files:
        print("\n" + "=" * 70)
        print(f"Processing {len(new_files)} new file(s)...")
        print("=" * 70)

        db = FinancialDatabase()
        processed = 0
        failed = 0

        for pdf_path in new_files:
            print(f"\nProcessing: {pdf_path.name}")
            if process_pdf(pdf_path, db):
                processed += 1
            else:
                failed += 1

        db.close()

        print("\n" + "=" * 70)
        print(f"Sync Complete!")
        print(f"  Downloaded: {len(new_files)}")
        print(f"  Processed: {processed}")
        print(f"  Failed: {failed}")
        print("=" * 70)
    else:
        print("\n✓ All files up to date - no new downloads needed")


if __name__ == "__main__":
    sync_from_google_drive()
