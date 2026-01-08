# Google Drive Integration Setup

This guide shows you how to automatically sync financial PDFs from Google Drive.

## 📋 One-Time Setup (15 minutes)

### Step 1: Create Google Cloud Project

1. **Go to**: https://console.cloud.google.com/
2. **Sign in** with your Google account (the one with access to the financials)
3. **Click** "Create Project" (top left)
4. **Name it**: "Masons Financial Sync"
5. **Click** "Create"

### Step 2: Enable Google Drive API

1. **In the project**, click "Enable APIs and Services"
2. **Search** for "Google Drive API"
3. **Click** "Google Drive API"
4. **Click** "Enable"

### Step 3: Create OAuth Credentials

1. **Go to**: APIs & Services → Credentials (left sidebar)
2. **Click** "Create Credentials" → "OAuth client ID"
3. **Configure consent screen** (if prompted):
   - User Type: **External**
   - App name: **Masons Financial Sync**
   - User support email: *your email*
   - Developer email: *your email*
   - Click **Save and Continue**
   - Scopes: Skip (click Save and Continue)
   - Test users: Add your email
   - Click **Save and Continue**
4. **Back to Credentials**:
   - Click "Create Credentials" → "OAuth client ID"
   - Application type: **Desktop app**
   - Name: **Masons Sync Client**
   - Click **Create**
5. **Download** the JSON file (click Download icon)
6. **Rename** it to `credentials.json`

### Step 4: Upload credentials.json to Codespaces

1. **Open GitHub Codespaces**
2. **Navigate to** `/workspaces/MasonsDBCC/`
3. **Upload** the `credentials.json` file
4. **IMPORTANT**: Don't commit this to git (it's already in .gitignore)

### Step 5: Get Your Google Drive Folder ID

1. **Open Google Drive** in your browser
2. **Navigate to** your "Masons Financials" folder (or create one)
3. **Look at the URL** - it looks like:
   ```
   https://drive.google.com/drive/folders/1a2b3c4d5e6f7g8h9i0j
                                          ^^^^^^^^^^^^^^^^^^^
                                          This is your Folder ID
   ```
4. **Copy** the Folder ID

### Step 6: Set Folder ID in Codespaces

In Codespaces terminal:

```bash
export GOOGLE_DRIVE_FOLDER_ID='your_folder_id_here'
```

Or edit `sync_from_google_drive.py` line 18:
```python
DRIVE_FOLDER_ID = 'your_folder_id_here'
```

---

## 🚀 Monthly Usage (2 minutes)

### Option 1: From iPad

1. **Upload PDFs** to your Google Drive folder from iPad
2. **Open Codespaces** on iPad
3. **Run** in terminal:
   ```bash
   python sync_from_google_drive.py
   ```
4. **First time only**: Authorize the app (click the link, allow access)
5. **Watch** as PDFs download and process automatically
6. **Commit** changes:
   ```bash
   git add .
   git commit -m "Sync from Google Drive - $(date +%Y-%m-%d)"
   git push
   ```

### Option 2: Scheduled Automation

Set up a GitHub Action to run monthly (see `AUTOMATION.md`)

---

## 📁 Folder Structure in Google Drive

Organize your Google Drive folder like this:

```
Mason's Financials/
├── 2026-01_ANN.pdf
├── 2026-01_SCO.pdf
├── 2026-01_DEN.pdf
├── 2026-02_ANN.pdf
└── ...
```

**File Naming**: Must follow `YYYY-MM_LocationCode.pdf` format!

---

## 🔧 Troubleshooting

### "credentials.json not found"
- Make sure you uploaded `credentials.json` to the root directory
- Check it's named exactly `credentials.json` (not `credentials (1).json`)

### "Google Drive folder ID not configured"
- Set the environment variable or edit the script
- Make sure the folder ID is correct (copy from URL)

### "Access denied" or "Permission denied"
- Make sure you added your email as a test user in OAuth consent screen
- Try deleting `token.pickle` and re-authenticating

### PDFs not downloading
- Check the PDFs are actually in the specified Google Drive folder
- Make sure they're not in a subfolder
- Check they're named correctly (`YYYY-MM_CODE.pdf`)

---

## 🔒 Security Notes

- `credentials.json` - Contains API keys, NOT in git (in .gitignore)
- `token.pickle` - Contains your auth token, NOT in git (in .gitignore)
- PDFs themselves are NOT committed to git (for privacy)
- Only the aggregated database is stored in git

---

## 💡 Alternative: Manual Upload

If Google Drive setup is too complex, you can still manually:

1. Download PDFs from Google Drive on iPad
2. Upload to Codespaces `financials/` folder
3. Run `python process_financials.py`
4. Commit and push

The sync script is just for convenience!
