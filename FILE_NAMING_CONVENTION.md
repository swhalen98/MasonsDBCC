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
| ANN | Annapolis #101 | Annapolis, MD | Open |
| AAV | Atlantic Avenue #122 | Virginia Beach, VA | Open |
| ARL | Arlington #121 | Arlington, VA | Open |
| AUS | Austin | Austin, TX | Open |
| BEL | Belleair Bluffs #129 | Belleair Bluffs, FL | Open |
| BVS | Belvedere Square #103 | Baltimore, MD | Open |
| CHS | Charleston #106 | Charleston, SC | Open |
| CLT | Charlotte #136 | Charlotte, NC | Open |
| COC | Coconut Point #140 | Estero, FL | Coming soon |
| COS | Colorado Springs #137 | Colorado Springs, CO | Open |
| DAL | Dallas #139 | Dallas, TX | Open |
| DEN | Denver #117 | Denver, CO | Open |
| DUP | Dupont #110 | Washington, DC | Open |
| EPR | E Pratt #103 | Baltimore, MD | Open |
| FAL | Falls Church #135 | Falls Church, VA | Open |
| FER | Fernandina #126 | Fernandina Beach, FL | Open |
| FLO | Florence | Florence, Italy | Coming soon |
| FTL | Ft. Lauderdale | Ft. Lauderdale, FL | Open |
| FDC | Ft. Myers/Daniel's Crossing #138 | Ft. Myers, FL | Open |
| FDP | Ft. Myers/Downtown #130 | Ft. Myers, FL | Open |
| GAI | Gaithersburg - Rosé 130 | Gaithersburg, MD | Open |
| LON | Long Branch #126 | Long Branch, NJ | Open |
| MID | Midlothian #131 | Midlothian, VA | Open |
| MIT | Milan - Via Torino | Milan, Italy | Open |
| MIV | Milan - Via Vespucci | Milan, Italy | Open |
| MOA | Mall Of America #113 | Bloomington, MN | Open |
| NAT | National Harbor #104 | National Harbor, MD | Open |
| PAN | Panama City Beach #124 | Panama City Beach, FL | Open |
| REH | Rehoboth #102 | Rehoboth Beach, DE | Open |
| RES | Reston #105 | Reston, VA | Open |
| RID | Ridgewood | Ridgewood, NJ | Open |
| SAU | Saucon Valley | Saucon Valley, PA | Open |
| SCO | Scottsdale #118 | Scottsdale, AZ | Open |
| SDV | Shore Drive #116 | Virginia Beach, VA | Open |
| SPV | Short Pump #137 | Richmond, VA | Open |
| SJF | St. Johns Town Center #133 | Jacksonville, FL | Open |
| WAL | Waldorf | Waldorf, MD | Open |
| WES | Western Market #114 | Washington, DC | Open |
| WHA | Wharf #125 | Washington, DC | Open |

## Region Mapping

- **Mid-Atlantic**: ANN, BVS, DUP, EPR, GAI, NAT, REH, WAL, WES, WHA (Maryland/DC/Delaware area)
- **Virginia**: AAV, ARL, FAL, MID, RES, SDV, SPV
- **Carolinas**: CHS, CLT
- **Southwest Florida**: BEL, FTL, FDC, FDP, COC
- **Northeast Florida**: FER, PAN, SJF
- **Texas**: AUS, DAL
- **Colorado**: COS, DEN
- **Arizona**: SCO
- **Northeast**: LON, RID, SAU
- **Midwest**: MOA
- **International-Europe**: MIT, MIV, FLO

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
