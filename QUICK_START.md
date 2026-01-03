# Quick Start Guide - Mason's Famous Lobsters Dashboard

## ⚡ 5-Minute Setup

### 1. Deploy to Render.com (3 minutes)

1. Go to https://render.com and sign up
2. Click "New +" → "Web Service"
3. Connect GitHub → select `swhalen98/MasonsDBCC`
4. **Name**: `masons-dashboard`
5. **Build Command**:
   ```
   pip install -r requirements.txt && python database.py
   ```
6. **Start Command**:
   ```
   panel serve dashboard.py --address 0.0.0.0 --port $PORT --allow-websocket-origin=*
   ```
7. Add Environment Variables:
   - `ADMIN_PASSWORD` = (your choice)
   - `MANAGER_PASSWORD` = (your choice)
   - `VIEWER_PASSWORD` = (your choice)
8. Click "Create Web Service"
9. Wait for deployment (~5 min)
10. **Save your dashboard URL!** (looks like `https://masons-dashboard.onrender.com`)

### 2. Test Login (1 minute)

1. Open dashboard URL
2. Login:
   - Username: `admin`
   - Password: (your ADMIN_PASSWORD)
3. See empty dashboard? ✅ Success!

### 3. Upload First File (5 minutes)

**On iPad/Computer:**

1. Go to GitHub.com → your repository
2. Click "Code" → "Codespaces" → "Create codespace"
3. Wait for it to load
4. Click `financials` folder
5. Right-click → "Upload files"
6. Select a PDF named like: `2026-01_ANN.pdf`
7. Open Terminal (bottom of screen)
8. Run:
   ```bash
   python process_financials.py
   git add .
   git commit -m "First upload"
   git push
   ```
9. Wait 2 minutes for Render to redeploy
10. Refresh dashboard → See your data! 🎉

---

## 📱 iPad-Optimized Workflow

### Weekly Upload (10 minutes)

1. **Collect PDFs** from email/cloud storage
2. **Rename files** on iPad:
   - Format: `YYYY-MM_CODE.pdf`
   - Example: `2026-01_ANN.pdf` for Annapolis, Jan 2026
3. **Open Codespace** (github.com/codespaces)
4. **Upload** to `financials/` folder
5. **Run in Terminal**:
   ```bash
   python process_financials.py
   git add .
   git commit -m "Weekly update $(date +%Y-%m-%d)"
   git push
   ```
6. **Check dashboard** (auto-deploys in 2 min)

---

## 🗂️ Location Codes Cheat Sheet

| Code | Location | Code | Location |
|------|----------|------|----------|
| ANN | Annapolis, MD | DEN | Denver, CO |
| ARL | Arlington, VA | DUP | Dupont Circle, DC |
| AUS | Austin, TX | FAL | Falls Church, VA |
| BEL | Belleair Bluffs, FL | FER | Fernandina Beach, FL |
| CAR | Cary, NC | FMD | Fort Myers Downtown, FL |
| CHS | Charleston, SC | GAI | Gaithersburg, MD |
| CLT | Charlotte, NC | MIL | Milan, Italy |
| COS | Colorado Springs, CO | ... | (see full list) |

See `FILE_NAMING_CONVENTION.md` for complete list.

---

## ⚙️ Daily Commands

### Check Missing Statements
```bash
python scheduled_check.py
```

### Process New Files
```bash
python process_financials.py
```

### Manual Entry (if PDF won't parse)
```bash
python -c "from pdf_parser import create_manual_entry_template; create_manual_entry_template('ANN', 2026, 1)"
# Edit the CSV, then:
python process_financials.py
```

### Deploy Changes
```bash
git add .
git commit -m "Update"
git push
```

---

## 🎯 Dashboard Features

### 3 View Modes

1. **Consolidated** - All locations combined
2. **By Region** - Mid-Atlantic, Virginia, Florida, etc.
3. **By Location** - Individual store

### What You Can See

- Revenue trends over time
- P&L breakdown by line item
- Profit margins
- Location comparisons
- Detailed data tables

### Filters

- Date range slider
- Location selector
- Region selector

---

## 💰 Costs

- **GitHub**: Free
- **Codespaces**: 60 hours/month free
- **Render.com**: Free tier (750 hours/month)
- **Total**: $0/month 🎉

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't login | Check password in Render env vars |
| No data showing | Did you `git push`? Wait 2 min |
| PDF won't process | Check filename format |
| Dashboard slow | First load takes 60 sec (free tier) |
| Upload failed | Try smaller batch (5 files) |

Full guide: See `TROUBLESHOOTING.md`

---

## 📞 Three User Logins

Share these credentials:

| Who | Username | Password |
|-----|----------|----------|
| You | `admin` | (ADMIN_PASSWORD) |
| Manager 1 | `manager` | (MANAGER_PASSWORD) |
| Managers 2 & 3 | `viewer` | (VIEWER_PASSWORD) |

**Security Note**: All users have same access currently. Passwords are in Render.com environment variables.

---

## ✅ You're Done!

**Dashboard URL**: (paste your Render URL here)

**Next Steps:**
1. ✅ Bookmark dashboard URL
2. ✅ Share with team
3. ✅ Upload financial statements monthly
4. ✅ Run weekly check for missing data

**Need detailed help?** See `SETUP_INSTRUCTIONS.md`

---

## 🚀 Pro Tips

1. **Bookmark Codespace** - creates faster than opening from GitHub
2. **Upload in batches** - process 5-10 files at a time
3. **Use manual entry** for tricky PDFs - faster than debugging parser
4. **Run weekly check** - keep locations accountable
5. **Hard refresh dashboard** (Cmd+Shift+R) if data seems stale

---

That's it! You now have a fully automated, cloud-hosted financial dashboard accessible from any device. 🎉
