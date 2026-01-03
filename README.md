# Mason's Famous Lobsters P&L Dashboard

> Automated financial reporting dashboard for Mason's Famous Lobster Rolls locations

## 🎯 What This Does

Automatically processes monthly financial statements (PDFs) from 29 locations and displays them in an interactive, password-protected dashboard with:
- Consolidated view across all locations
- Drill-down by region or individual location
- Revenue trends and P&L breakdowns
- Missing statement tracking
- 100% free hosting

## ✨ Features

- **📊 Interactive Dashboard** - Built with Panel, hosted on Render.com
- **🔐 Secure Login** - 3 user accounts with password authentication
- **📱 iPad-Friendly** - Upload and manage from iPad using GitHub Codespaces
- **🤖 Automated Processing** - PDF parsing with fallback to manual entry
- **💾 DuckDB Database** - Fast, embedded analytics database
- **📍 29 Locations** - US (27) + International (2)
- **🌍 Regional Grouping** - Mid-Atlantic, Virginia, Carolinas, Florida, Texas, Colorado, etc.
- **💰 Free Hosting** - GitHub + Render.com free tiers

## 🚀 Quick Start

### 1-Minute Overview

1. **Deploy to Render.com** (see `QUICK_START.md`)
2. **Set 3 passwords** (admin, manager, viewer)
3. **Upload PDFs** via GitHub Codespaces
4. **View Dashboard** - instant analytics

### Detailed Setup

📖 See **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** for complete step-by-step guide

## 📁 File Structure

```
MasonsDBCC/
├── dashboard.py              # Panel dashboard application
├── database.py               # DuckDB database management
├── pdf_parser.py             # PDF financial statement parser
├── process_financials.py     # Process and load PDFs
├── auto_process.py           # Automatic file monitoring
├── scheduled_check.py        # Weekly missing statement check
├── auth.py                   # Authentication system
├── config.py                 # Configuration and location codes
├── requirements.txt          # Python dependencies
├── render.yaml               # Render.com deployment config
├── financials/               # Upload PDFs here (YYYY-MM_CODE.pdf)
├── logs/                     # Processing logs
├── masons_financials.duckdb  # Database file
├── SETUP_INSTRUCTIONS.md     # Detailed setup guide
├── QUICK_START.md            # Quick start guide
├── TROUBLESHOOTING.md        # Common issues and solutions
└── FILE_NAMING_CONVENTION.md # Location codes and naming
```

## 📋 File Naming Convention

Format: `YYYY-MM_LocationCode.pdf`

Examples:
- `2026-01_ANN.pdf` - Annapolis, January 2026
- `2026-02_DEN.pdf` - Denver, February 2026
- `2025-12_MIL.pdf` - Milan, December 2025

### Location Codes

| Region | Codes |
|--------|-------|
| **Mid-Atlantic** | ANN, BVS, DUP, GAI, HAR, NAT |
| **Virginia** | ARL, FAL, MID, RES |
| **Carolinas** | CAR, CHS, CLT |
| **Florida** | BEL, FER, FMD, FMD2, MAR, PAN, COC |
| **Texas** | AUS, DAL |
| **Colorado** | COS, DEN |
| **Northeast** | LON, REH |
| **Midwest** | MOA |
| **International** | MIL, FLO |

See `FILE_NAMING_CONVENTION.md` for complete list with city names.

## 🔧 Usage

### Monthly Workflow

1. **Collect PDFs** from all locations
2. **Rename** to format: `YYYY-MM_CODE.pdf`
3. **Upload** to `financials/` folder via Codespace
4. **Process**:
   ```bash
   python process_financials.py
   ```
5. **Commit & Push**:
   ```bash
   git add .
   git commit -m "Add financials for [Month Year]"
   git push
   ```
6. **Auto-deploys** to Render.com in 2-3 minutes
7. **View** updated dashboard

### Weekly Check

Run missing statement report:
```bash
python scheduled_check.py
```

Outputs:
- Which locations haven't submitted
- Missing count by region
- CSV report for follow-up

### Manual Entry (for non-standard PDFs)

If PDF can't be parsed:
```bash
python -c "from pdf_parser import create_manual_entry_template; create_manual_entry_template('ANN', 2026, 1)"
```

Edit CSV → Upload → Process

## 👥 User Accounts

3 accounts (set passwords in Render.com environment variables):

- `admin` - Full access
- `manager` - Full access
- `viewer` - Full access

(Currently same permissions; can be customized later)

## 📊 Dashboard Views

### Consolidated View
- All locations combined
- Company-wide metrics
- Total revenue, net income, profit margin

### By Region View
- Mid-Atlantic, Virginia, Florida, etc.
- Regional performance comparison

### By Location View
- Individual store P&L
- Location-specific trends

## 🗄️ Database Schema

**DuckDB Tables:**

1. **locations** - Location master data (code, name, city, region, status)
2. **financial_statements** - Statement metadata (location, date, file)
3. **pnl_data** - P&L line items and amounts

**Standard P&L Line Items:**
- Total Revenue
- Food Sales
- Beverage Sales
- Cost of Goods Sold
- Gross Profit
- Labor
- Rent
- Utilities
- Marketing
- Net Income
- etc.

## 💻 Local Development

```bash
# Clone repository
git clone https://github.com/swhalen98/MasonsDBCC.git
cd MasonsDBCC

# Install dependencies
pip install -r requirements.txt

# Initialize database
python database.py

# Run dashboard locally
python dashboard.py
# Opens at http://localhost:5000
```

## 🌐 Deployment

**Render.com (Free Tier)**

1. Connect GitHub repository
2. Use `render.yaml` config
3. Set environment variables:
   - `ADMIN_PASSWORD`
   - `MANAGER_PASSWORD`
   - `VIEWER_PASSWORD`
4. Deploy!

Auto-deploys on every `git push` to main branch.

## 📱 iPad Workflow

Perfect for iPad-only users:

1. **GitHub.com** - Access repository
2. **Codespaces** - Cloud development environment
3. **Upload files** - Drag & drop PDFs
4. **Run commands** - Terminal in browser
5. **View dashboard** - Any browser

No desktop required! ✅

## 🛠️ Tech Stack

- **Frontend**: Panel (Python), HoloViews, hvPlot
- **Backend**: Python 3.11
- **Database**: DuckDB (embedded)
- **PDF Parsing**: pdfplumber, PyPDF2
- **Auth**: bcrypt
- **Hosting**: Render.com (free tier)
- **CI/CD**: GitHub + Render auto-deploy
- **Development**: GitHub Codespaces

## 💰 Cost Breakdown

- GitHub: **Free**
- Codespaces: **Free** (60 hrs/month)
- Render.com: **Free** (750 hrs/month)
- DuckDB: **Free** (open source)
- Panel: **Free** (open source)

**Total: $0/month** 🎉

Optional upgrades:
- Render Starter: $7/month (faster, always-on)
- GitHub Pro: $4/month (more Codespaces hours)

## 📚 Documentation

- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Complete setup guide
- **[QUICK_START.md](QUICK_START.md)** - 5-minute quick start
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues
- **[FILE_NAMING_CONVENTION.md](FILE_NAMING_CONVENTION.md)** - Location codes

## 🆘 Troubleshooting

Common issues:

- **Can't login** - Check environment variables in Render
- **No data** - Did you `git push`? Wait 2-3 min
- **PDF won't process** - Use manual entry template
- **Dashboard slow** - First load takes 60s (free tier cold start)

See `TROUBLESHOOTING.md` for detailed solutions.

## 🔄 Automation

**File Monitoring** (optional):
```bash
python auto_process.py
```
Watches `financials/` folder and auto-processes new files.

**Weekly Report** (cron/scheduled):
```bash
python scheduled_check.py
```
Emails missing statement report to management.

## 🔐 Security

- Password authentication with bcrypt hashing
- Environment variable passwords (not in code)
- HTTPS via Render.com
- No public data exposure
- Passwords stored hashed in `.users` file

**⚠️ Change default passwords!** Set in Render environment variables.

## 📈 Roadmap

- [ ] Email notifications for missing statements
- [ ] Role-based permissions (admin vs. viewer)
- [ ] Budget vs. actual comparisons
- [ ] Year-over-year trend analysis
- [ ] Export to Excel
- [ ] Mobile app (iOS/Android)
- [ ] Forecasting/predictions

## 🤝 Contributing

This is a private dashboard for Mason's Famous Lobster Rolls. If you'd like to suggest improvements:

1. Open an issue
2. Submit a pull request
3. Contact the administrator

## 📄 License

Proprietary - Mason's Famous Lobster Rolls

## 👨‍💻 Support

Questions or issues?

1. Check `TROUBLESHOOTING.md`
2. Review Render logs
3. Check GitHub Issues
4. Contact system administrator

---

## ✅ Status

**All 29 Locations:**

✅ Open (23):
Annapolis, Arlington, Austin, Belleair Bluffs, Belvedere Square, Cary, Charleston, Charlotte, Colorado Springs, Denver, Dupont Circle, Falls Church, Fernandina Beach, Fort Myers Downtown, Gaithersburg, Harborplace, Long Branch, Mall of America, Marina Village, Midlothian, Milan, National Harbor, Panama City Beach, Rehoboth Beach, Reston

🔜 Coming Soon (6):
Dallas, Fort Myers Daniels, Coconut Point, Florence

**Dashboard**: ✅ Deployed
**Database**: ✅ Initialized
**Authentication**: ✅ Configured
**Automation**: ✅ Ready

---

Made with ❤️ for Mason's Famous Lobster Rolls
