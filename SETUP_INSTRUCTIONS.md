# Mason's Famous Lobsters P&L Dashboard - Setup Instructions

## 📋 Overview

This system automatically processes financial statements and displays them in an interactive dashboard. It's designed to be:
- **Free/Low-cost**: Uses free tiers of GitHub and Render.com
- **Automated**: Automatically processes new statements
- **Accessible**: Works from iPad or any device
- **Secure**: Password-protected with 3 user accounts

---

## 🚀 Initial Setup (One-Time)

### Step 1: Set Up GitHub Repository

1. **On your iPad, open GitHub.com in Safari**
2. **Go to this repository**: `swhalen98/MasonsDBCC`
3. **All code is already committed** - ready to use!

### Step 2: Deploy to Render.com

1. **Create Render.com account**
   - Go to https://render.com
   - Sign up with GitHub (it's free!)
   - Click "Authorize Render" to connect to GitHub

2. **Create New Web Service**
   - Click "New +" button → "Web Service"
   - Connect to your GitHub repository: `swhalen98/MasonsDBCC`
   - Click on the repository

3. **Configure Service**
   - **Name**: `masons-lobsters-dashboard`
   - **Region**: Choose closest to you (e.g., Oregon for West Coast)
   - **Branch**: `claude/financial-dashboard-automation-hlcQl` (or `main`)
   - **Runtime**: Python
   - **Build Command**:
     ```
     pip install -r requirements.txt && python database.py
     ```
   - **Start Command**:
     ```
     panel serve dashboard.py --address 0.0.0.0 --port $PORT --allow-websocket-origin=* --num-procs=1
     ```
   - **Instance Type**: Free

4. **Set Environment Variables**
   - Click "Advanced" → "Add Environment Variable"
   - Add these three variables with YOUR chosen passwords:
     ```
     ADMIN_PASSWORD=YourAdminPassword123!
     MANAGER_PASSWORD=YourManagerPassword456!
     VIEWER_PASSWORD=YourViewerPassword789!
     ```
   - ⚠️ **IMPORTANT**: Write these passwords down! You'll need them to login.

5. **Create Web Service**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - You'll see a URL like: `https://masons-lobsters-dashboard.onrender.com`

6. **Test the Dashboard**
   - Click the URL
   - Login with username: `admin` and your ADMIN_PASSWORD
   - You should see the empty dashboard (no data yet!)

### Step 3: Set Up GitHub Codespaces (for file uploads)

Since you're on iPad, you'll use GitHub Codespaces to upload files:

1. **Open GitHub.com** on your iPad
2. **Go to your repository**: `swhalen98/MasonsDBCC`
3. **Click Code (green button) → Codespaces → Create codespace**
4. **Wait for environment to load** (2-3 minutes)
5. **You now have a cloud computer!** 🎉

---

## 📁 How to Upload Financial Statements (Weekly/Monthly)

### Option A: Using GitHub Codespaces (iPad-Friendly)

1. **Open your Codespace**
   - Go to github.com/codespaces
   - Click on `MasonsDBCC` codespace

2. **Upload PDF Files**
   - Click on `financials` folder
   - Click "..." (three dots) → "Upload"
   - Select your PDF files from iPad Files app
   - **Files MUST be named**: `YYYY-MM_LocationCode.pdf`
     - Example: `2026-01_ANN.pdf` (Annapolis, January 2026)
     - Example: `2026-01_DEN.pdf` (Denver, January 2026)
   - See `FILE_NAMING_CONVENTION.md` for all location codes

3. **Process the Files**
   - Open Terminal in Codespace (Terminal menu → New Terminal)
   - Run:
     ```bash
     python process_financials.py
     ```
   - Watch as files are processed!

4. **Commit & Push to GitHub**
   ```bash
   git add financials/*.pdf masons_financials.duckdb*
   git commit -m "Add financial statements for Jan 2026"
   git push
   ```

5. **Render will auto-deploy** (takes 2-3 minutes)
6. **Refresh your dashboard** to see new data!

### Option B: If PDFs Can't Be Parsed (Manual Entry)

If the PDF format is weird and can't be auto-parsed:

1. **Create manual entry template** (in Codespace terminal):
   ```bash
   python -c "from pdf_parser import create_manual_entry_template; create_manual_entry_template('ANN', 2026, 1)"
   ```

2. **Download the CSV file** from Codespace

3. **Edit on iPad**
   - Open in Numbers or Excel
   - Fill in the amounts
   - Save as CSV

4. **Upload back to `financials/` folder**

5. **Process**:
   ```bash
   python process_financials.py
   git add . && git commit -m "Add manual entry" && git push
   ```

---

## 📅 Weekly Routine (15 minutes)

### Every Monday Morning:

1. **Check for new statements**
   - Open Codespace
   - Run:
     ```bash
     python scheduled_check.py
     ```
   - This shows which locations haven't submitted yet

2. **Upload any new PDFs** (see above)

3. **Process & Deploy**
   ```bash
   python process_financials.py
   git add .
   git commit -m "Weekly update - $(date +%Y-%m-%d)"
   git push
   ```

4. **Verify Dashboard**
   - Open dashboard URL
   - Check that new data appears
   - Verify all locations

5. **Send reminder emails** to locations that haven't submitted

---

## 👥 User Accounts

You have 3 user accounts (all same access level currently):

| Username | Password | Who Should Use |
|----------|----------|----------------|
| `admin` | (your ADMIN_PASSWORD) | You |
| `manager` | (your MANAGER_PASSWORD) | Manager #1 |
| `viewer` | (your VIEWER_PASSWORD) | Manager #2 & #3 |

To change passwords:
1. Open Codespace
2. Run:
   ```bash
   python -c "from auth import SimpleAuth; auth = SimpleAuth(); auth.change_password('admin', 'old_password', 'new_password')"
   ```

---

## 📊 Using the Dashboard

### Login
- Go to your Render URL
- Enter username and password
- Click "Login"

### Views

**Consolidated** - All locations combined
- See total revenue, net income for entire company
- Compare trends across all locations

**By Region** - Drill down by region
- Select region from dropdown
- See Mid-Atlantic, Virginia, Florida, etc.

**By Location** - Individual location
- Select specific location
- See that location's P&L only

### Features
- **Date Range Slider**: Filter by date
- **Charts**: Revenue trends, P&L breakdown
- **Data Table**: Detailed numbers, sortable, searchable

---

## 🗂️ File Naming Reference

### Location Codes

| Code | Location | City |
|------|----------|------|
| ANN | Annapolis | Annapolis, MD |
| ARL | Arlington | Arlington, VA |
| AUS | Austin | Austin, TX |
| BEL | Belleair Bluffs | Belleair Bluffs, FL |
| BVS | Belvedere Square | Baltimore, MD |
| CAR | Cary | Cary, NC |
| CHS | Charleston | Charleston, SC |
| CLT | Charlotte | Charlotte, NC |
| COS | Colorado Springs | Colorado Springs, CO |
| DAL | Dallas | Dallas, TX |
| DEN | Denver | Denver, CO |
| DUP | Dupont Circle | Washington, DC |
| FAL | Falls Church | Falls Church, VA |
| FER | Fernandina Beach | Fernandina Beach, FL |
| FMD | Fort Myers Downtown | Fort Myers, FL |
| FMD2 | Fort Myers Daniels | Fort Myers, FL |
| GAI | Gaithersburg | Gaithersburg, MD |
| HAR | Harborplace | Baltimore, MD |
| LON | Long Branch | Long Branch, NJ |
| MOA | Mall of America | Bloomington, MN |
| MAR | Marina Village | Fort Lauderdale, FL |
| MID | Midlothian | Midlothian, VA |
| MIL | Milan | Milan, Italy |
| NAT | National Harbor | National Harbor, MD |
| PAN | Panama City Beach | Panama City Beach, FL |
| REH | Rehoboth Beach | Rehoboth Beach, DE |
| RES | Reston | Reston, VA |
| COC | Coconut Point | Estero, FL |
| FLO | Florence | Florence, Italy |

### File Examples
```
2026-01_ANN.pdf    → Annapolis, January 2026
2026-02_DEN.pdf    → Denver, February 2026
2025-12_MIL.pdf    → Milan, December 2025
```

---

## 🔧 Troubleshooting

### Dashboard won't load
- Check Render.com dashboard for errors
- Look at "Logs" tab
- Common fix: Redeploy (click "Manual Deploy")

### PDF not processing
- Check filename format exactly: `YYYY-MM_CODE.pdf`
- Try manual entry method
- Check Codespace terminal for error messages

### Can't login
- Double-check username and password
- Check environment variables in Render.com
- Passwords are case-sensitive!

### Missing data in dashboard
- Did you run `git push`?
- Wait 2-3 minutes for Render to deploy
- Hard refresh dashboard (Cmd+Shift+R or Ctrl+Shift+R)

---

## 💰 Cost Breakdown

- **GitHub**: Free (for public repos)
- **Codespaces**: 60 hours/month free (way more than you need)
- **Render.com**: Free tier (750 hours/month)
- **DuckDB**: Free (it's just a file)
- **Panel Dashboard**: Free (open source)

**Total Monthly Cost: $0** ✅

---

## 📞 Need Help?

1. Check `TROUBLESHOOTING.md` (in repository)
2. Look at Render logs: Dashboard → Logs tab
3. Check GitHub Issues for this project

---

## ✅ Quick Reference Checklist

**Monthly Upload Process:**
- [ ] Collect all financial PDFs
- [ ] Rename files: `YYYY-MM_CODE.pdf`
- [ ] Open GitHub Codespace
- [ ] Upload to `financials/` folder
- [ ] Run: `python process_financials.py`
- [ ] Run: `git add . && git commit -m "Add financials" && git push`
- [ ] Wait 2-3 minutes
- [ ] Refresh dashboard
- [ ] Verify data looks correct

**Weekly Check:**
- [ ] Run: `python scheduled_check.py`
- [ ] Review missing statements
- [ ] Send reminders to locations
- [ ] Update dashboard with any late submissions

---

## 🎉 You're All Set!

The system is now running 24/7 on Render.com. Access it anytime from your iPad, phone, or computer. Share the URL and login credentials with your team.

**Dashboard URL**: (Your Render URL will be here after setup)

**Next Steps**:
1. Test upload with one sample PDF
2. Verify it appears in dashboard
3. Share credentials with your team
4. Set weekly reminder to check for updates
