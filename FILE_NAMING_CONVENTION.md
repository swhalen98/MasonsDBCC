# Financial Statement File Naming Convention

## Format

### Option 1: Single File (All Statements Combined)
```
YYYY-MM_LocationCode.pdf
```
or
```
YYYY-MM_LocationCode_ALL.pdf
```

### Option 2: Separate Files by Statement Type
```
YYYY-MM_LocationCode_IS.pdf  (Income Statement)
YYYY-MM_LocationCode_BS.pdf  (Balance Sheet)
YYYY-MM_LocationCode_CF.pdf  (Cash Flow Statement)
```

### Statement Type Codes
- **IS** = Income Statement (Profit & Loss)
- **BS** = Balance Sheet
- **CF** = Cash Flow Statement
- **ALL** = All statements (same as no suffix)

## Examples

### Single File (All Statements)
- `2026-01_ANN.pdf` - Annapolis, January 2026 (all statements)
- `2026-02_ARL.pdf` - Arlington, February 2026 (all statements)
- `2026-12_MIL_ALL.pdf` - Milan, December 2026 (all statements, explicit)

### Multiple Files (Separate Statements)
- `2026-01_ANN_IS.pdf` - Annapolis Income Statement, January 2026
- `2026-01_ANN_BS.pdf` - Annapolis Balance Sheet, January 2026
- `2026-01_ANN_CF.pdf` - Annapolis Cash Flow, January 2026

### Mixed (Some Locations Have Different Formats)
- Location A: `2026-01_ANN.pdf` (all in one)
- Location B: `2026-01_ARL_IS.pdf` + `2026-01_ARL_BS.pdf` (only two statements)
- Location C: `2026-01_AUS_IS.pdf` + `2026-01_AUS_BS.pdf` + `2026-01_AUS_CF.pdf` (all three separate)

**This is completely flexible!** Each location can submit in whatever format works best for them.

## Location Codes

| Location Code | Location Name | City, State/Country | Status |
|--------------|---------------|---------------------|--------|
| ANN | Annapolis | Annapolis, MD | Open |
| ARL | Arlington – Village at Shirlington | Arlington, VA | Open |
| AUS | Austin | Austin, TX | Open |
| BEL | Belleair Bluffs | Belleair Bluffs, FL | Open |
| BVS | Belvedere Square | Baltimore, MD | Open |
| CAR | Cary – Waverly Place | Cary, NC | Open |
| CHS | Charleston | Charleston, SC | Open |
| CLT | Charlotte | Charlotte, NC | Open |
| COS | Colorado Springs | Colorado Springs, CO | Open |
| DAL | Dallas | Dallas, TX | Coming soon |
| DEN | Denver | Denver, CO | Open |
| DUP | Dupont Circle | Washington, DC | Open |
| FAL | Falls Church | Falls Church, VA | Open |
| FER | Fernandina Beach | Fernandina Beach, FL | Open |
| FMD | Fort Myers – Downtown | Fort Myers, FL | Open |
| FMD2 | Fort Myers – Daniels Parkway | Fort Myers, FL | Coming soon |
| GAI | Gaithersburg – Rio Lakefront | Gaithersburg, MD | Open |
| HAR | Harborplace | Baltimore, MD | Open |
| LON | Long Branch | Long Branch, NJ | Open |
| MOA | Mall of America | Bloomington, MN | Open |
| MAR | Marina Village | Fort Lauderdale, FL | Open |
| MID | Midlothian | Midlothian, VA | Open |
| MIL | Milan | Milan, Italy | Open |
| NAT | National Harbor | National Harbor, MD | Open |
| PAN | Panama City Beach | Panama City Beach, FL | Open |
| REH | Rehoboth Beach | Rehoboth Beach, DE | Open |
| RES | Reston | Reston, VA | Open |
| SCO | Scottsdale | Scottsdale, AZ | Open |
| COC | Coconut Point | Estero, FL | Coming soon |
| FLO | Florence | Florence, Italy | Coming soon |

## Region Mapping

- **Mid-Atlantic**: ANN, BVS, DUP, GAI, HAR, NAT (Maryland/DC area)
- **Virginia**: ARL, FAL, MID, RES
- **Carolinas**: CAR, CHS, CLT
- **Florida**: BEL, FER, FMD, FMD2, MAR, PAN, COC
- **Southwest Florida**: FMD, FMD2, BEL, COC
- **Texas**: AUS, DAL
- **Colorado**: COS, DEN
- **Arizona**: SCO
- **Northeast**: LON
- **Midwest**: MOA
- **International**: MIL, FLO

## Instructions for Uploading

1. **Save your financial statement(s) as PDF**
   - If all three statements (Income Statement, Balance Sheet, Cash Flow) are in one PDF, that's fine!
   - If they're in separate PDFs, that's also fine!
   - You can even send just the Income Statement if that's all you have

2. **Rename using the appropriate format:**
   - **All-in-one file**: `YYYY-MM_LocationCode.pdf`
   - **Separate files**: `YYYY-MM_LocationCode_IS.pdf`, `YYYY-MM_LocationCode_BS.pdf`, `YYYY-MM_LocationCode_CF.pdf`

3. **Upload to the `financials/` folder**
   - Via GitHub Codespaces (drag & drop)
   - Or via Google Drive sync (automatic)

4. **Process the statements:**
   ```bash
   python process_financials.py
   ```

The system will automatically:
- Detect which statement types are in each file
- Extract the relevant financial data
- Store everything in the database
- Update the dashboard

## Missing Statements

If a location doesn't submit a statement for a month, simply don't upload a file. The system will handle missing data appropriately and show "No Data" in the dashboard for that location/month.
