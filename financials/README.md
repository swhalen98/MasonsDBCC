# Financials Folder

This folder stores monthly financial statement PDFs.

## File Naming Convention

**Format**: `YYYY-MM_LocationCode.pdf`

**Examples**:
- `2026-01_ANN.pdf` - Annapolis, January 2026
- `2026-01_SCO.pdf` - Scottsdale, January 2026
- `2025-12_DEN.pdf` - Denver, December 2025

## Location Codes

See `FILE_NAMING_CONVENTION.md` in the root directory for all location codes.

## Upload Methods

### Method 1: Direct Upload (Codespaces)
1. Open GitHub Codespaces
2. Navigate to this `financials/` folder
3. Right-click → Upload files
4. Select your PDFs from iPad Files or Google Drive

### Method 2: Google Drive Sync (Automated)
Run the sync script:
```bash
python sync_from_google_drive.py
```

This will automatically download new PDFs from your Google Drive folder.

## Privacy Note

**PDF files are NOT committed to git** for privacy/security. Only the database with aggregated financial data is stored in the repository.
