# Troubleshooting Guide

## Common Issues and Solutions

### 🔐 Login Issues

#### Problem: "Invalid username or password"
**Solutions:**
1. Double-check username (lowercase): `admin`, `manager`, or `viewer`
2. Verify password in Render.com:
   - Go to Render.com dashboard
   - Click on your web service
   - Go to "Environment" tab
   - Check `ADMIN_PASSWORD`, `MANAGER_PASSWORD`, `VIEWER_PASSWORD`
3. Passwords are case-sensitive - check caps lock
4. Try resetting password in Codespace:
   ```bash
   python -c "from auth import SimpleAuth; auth = SimpleAuth(); auth.add_user('admin', 'newpassword123')"
   ```

#### Problem: Login button doesn't work
**Solutions:**
1. Hard refresh the page (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear browser cache
3. Try different browser (Safari, Chrome)
4. Check Render logs for errors

---

### 📄 PDF Processing Issues

#### Problem: "Invalid filename format"
**Issue:** File named incorrectly

**Solution:** Rename to exact format: `YYYY-MM_CODE.pdf`
- ✅ Correct: `2026-01_ANN.pdf`
- ❌ Wrong: `2026-1-ANN.pdf` (month must be 2 digits)
- ❌ Wrong: `Jan-2026-ANN.pdf` (wrong format)
- ❌ Wrong: `2026-01-ANN.pdf` (use underscore, not dash)

#### Problem: "Unknown location code"
**Issue:** Location code not recognized

**Solution:**
1. Check `FILE_NAMING_CONVENTION.md` for correct codes
2. Make sure code is uppercase
3. Verify location code exists in system

#### Problem: PDF processes but no data extracted
**Issue:** PDF format incompatible with parser

**Solutions:**
1. Check if PDF is scanned image vs. text-based:
   - Try to select text in PDF
   - If you can't, it's a scanned image

2. Use manual entry instead:
   ```bash
   python -c "from pdf_parser import create_manual_entry_template; create_manual_entry_template('ANN', 2026, 1)"
   ```

3. Open PDF and verify it contains P&L data

4. Check for standard line items:
   - Total Revenue
   - Cost of Goods Sold
   - Gross Profit
   - Net Income
   etc.

---

### 🖥️ Dashboard Issues

#### Problem: Dashboard shows "No data available"
**Causes & Solutions:**

1. **No files processed yet**
   - Upload financial PDFs
   - Run `python process_financials.py`
   - Commit and push to GitHub

2. **Database not deployed**
   - Make sure you committed `masons_financials.duckdb*` files
   - Check `.gitignore` - remove `*.duckdb` if present
   - Push again

3. **Date filter excludes all data**
   - Adjust date range slider to include your data dates

#### Problem: Dashboard is slow to load
**Solutions:**
1. Render free tier can be slow on first load (60 seconds)
2. Wait patiently for "cold start"
3. Once loaded, subsequent loads are faster
4. Consider upgrading Render plan if needed ($7/month)

#### Problem: Charts not displaying
**Causes & Solutions:**

1. **Not enough data**
   - Need at least 2 months for trends
   - Need multiple line items for breakdown charts

2. **JavaScript error**
   - Check browser console (F12)
   - Hard refresh (Ctrl+Shift+R)

3. **Wrong data format**
   - Verify amounts are numbers, not text
   - Check database with:
     ```bash
     python -c "from database import FinancialDatabase; db = FinancialDatabase(); print(db.get_summary_stats())"
     ```

---

### 📤 Upload Issues (Codespaces/GitHub)

#### Problem: Can't upload files to Codespace
**Solutions:**
1. Refresh the Codespace page
2. Stop and restart Codespace:
   - Go to github.com/codespaces
   - Click "..." → "Stop codespace"
   - Wait 30 seconds
   - Click to restart

3. Try uploading smaller batches (5 PDFs at a time)

4. Alternative: Use git command line:
   ```bash
   # In Codespace terminal
   git add financials/2026-01_ANN.pdf
   git commit -m "Add Annapolis Jan 2026"
   git push
   ```

#### Problem: "Permission denied" in Codespace
**Solutions:**
1. Make sure you're in the correct directory:
   ```bash
   cd /workspaces/MasonsDBCC
   pwd  # Should show /workspaces/MasonsDBCC
   ```

2. Check file permissions:
   ```bash
   ls -la financials/
   ```

3. Fix permissions if needed:
   ```bash
   chmod 644 financials/*.pdf
   ```

---

### 🚀 Render.com Deployment Issues

#### Problem: "Deploy failed" or "Build failed"
**Solutions:**

1. **Check the logs:**
   - Render Dashboard → Your Service → "Logs" tab
   - Look for specific error messages

2. **Common build errors:**

   **"No module named 'X'"**
   - Missing dependency in `requirements.txt`
   - Add it and push:
     ```bash
     echo "missing-package==1.0.0" >> requirements.txt
     git add requirements.txt
     git commit -m "Add missing dependency"
     git push
     ```

   **"Python version not found"**
   - Check `runtime.txt` has correct Python version
   - Render supports Python 3.8 - 3.11

3. **Manual redeploy:**
   - Render Dashboard → Your Service
   - Click "Manual Deploy" → "Deploy latest commit"

#### Problem: Dashboard URL shows "Not Found" or "502 Bad Gateway"
**Solutions:**

1. **Service starting up**
   - Wait 2-3 minutes after deploy
   - Refresh page

2. **Service crashed**
   - Check Render logs
   - Look for Python errors
   - Common issue: Missing environment variables

3. **Wrong port**
   - Verify start command uses `$PORT`:
     ```
     panel serve dashboard.py --address 0.0.0.0 --port $PORT
     ```

#### Problem: Environment variables not working
**Solutions:**

1. **Set in Render dashboard:**
   - Dashboard → Your Service → "Environment"
   - Click "Add Environment Variable"
   - Add key and value
   - Click "Save Changes"
   - **Important:** Redeploy after changing env vars!

2. **Check they're loaded:**
   - Look at logs during startup
   - Should see environment variable values (not passwords though!)

---

### 🗄️ Database Issues

#### Problem: Data disappeared after update
**Causes:**

1. **Database file not committed**
   - The database is stored in `masons_financials.duckdb`
   - Must be committed to Git
   - Check with: `git status`

2. **Gitignore excluding database**
   - Open `.gitignore`
   - Remove `*.duckdb` or `*.db` if present
   - Commit and push

**Solution:**
```bash
# Force add database
git add -f masons_financials.duckdb*
git commit -m "Add database file"
git push
```

#### Problem: "Database is locked" error
**Cause:** Multiple processes accessing database

**Solution:**
1. Stop any running processes
2. In Codespace:
   ```bash
   pkill -f python
   ```
3. Wait 10 seconds
4. Try again

#### Problem: Duplicate data after reprocessing
**Cause:** Database constraint not working

**Solution:**
```bash
# Delete old database and start fresh
rm masons_financials.duckdb*
python database.py
python process_financials.py
```

---

### 📱 iPad-Specific Issues

#### Problem: Can't upload files from iPad Files app
**Solutions:**

1. **Use iCloud Drive:**
   - Save PDFs to iCloud Drive
   - Access from Codespace browser
   - Download to Codespace
   - Move to `financials/` folder

2. **Email method:**
   - Email PDFs to yourself
   - Download from webmail in Codespace browser
   - Save to `financials/` folder

3. **Alternative: GitHub web interface:**
   - Go to repository on GitHub.com
   - Navigate to `financials/` folder
   - Click "Add file" → "Upload files"
   - Drag PDFs from Files app
   - Commit directly

#### Problem: Codespace won't load on iPad
**Solutions:**
1. Use Safari (works best)
2. Enable "Desktop Website" mode
3. Clear Safari cache
4. Try on laptop/desktop if available

---

### 📊 Data Accuracy Issues

#### Problem: Numbers look wrong in dashboard
**Solutions:**

1. **Check source PDF:**
   - Open original PDF
   - Verify numbers match

2. **Check database:**
   ```bash
   python -c "from database import FinancialDatabase; db = FinancialDatabase(); print(db.get_all_data())"
   ```

3. **Reprocess specific file:**
   ```bash
   python process_financials.py financials/2026-01_ANN.pdf
   ```

4. **If still wrong, use manual entry:**
   - Create CSV template
   - Enter numbers manually
   - Process CSV

#### Problem: Missing line items
**Cause:** PDF format doesn't match expected line items

**Solution:**
1. Edit `config.py` → `PNL_LINE_ITEMS` list
2. Add your specific line items
3. Reprocess files:
   ```bash
   rm masons_financials.duckdb*
   python database.py
   python process_financials.py
   ```

---

## 🆘 Emergency Recovery

### Complete System Reset

If everything is broken, start fresh:

```bash
# 1. Back up any custom changes
cp config.py config.py.backup

# 2. Delete database
rm masons_financials.duckdb*
rm .users

# 3. Reinitialize
python database.py

# 4. Reprocess all files
python process_financials.py

# 5. Commit
git add .
git commit -m "Reset system"
git push

# 6. Redeploy on Render
# Go to Render dashboard → Manual Deploy
```

---

## 📞 Getting Help

1. **Check this guide first**
2. **Check Render logs** (most issues show up there)
3. **Try on a different device/browser**
4. **Look at GitHub Issues** for similar problems
5. **Ask for help** with specific error messages

---

## 🔍 Debugging Commands

Useful commands to diagnose issues:

```bash
# Check database contents
python -c "from database import FinancialDatabase; db = FinancialDatabase(); print(db.get_summary_stats())"

# List all processed files
python -c "from database import FinancialDatabase; db = FinancialDatabase(); print(db.conn.execute('SELECT * FROM financial_statements').df())"

# Test PDF parsing
python pdf_parser.py

# Check for missing statements
python scheduled_check.py 6

# Verify authentication
python -c "from auth import SimpleAuth; auth = SimpleAuth(); print(auth.authenticate('admin', 'your_password'))"

# Test database connection
python -c "import duckdb; print(duckdb.connect('masons_financials.duckdb').execute('SELECT COUNT(*) FROM locations').fetchone())"
```

---

## ✅ Checklist: Is Everything Set Up Correctly?

- [ ] Repository exists on GitHub
- [ ] Render.com service created and deployed
- [ ] Environment variables set (ADMIN_PASSWORD, etc.)
- [ ] Dashboard URL loads (even if no data)
- [ ] Can login with admin credentials
- [ ] `financials/` folder exists
- [ ] Can upload files to Codespace
- [ ] `python process_financials.py` runs without errors
- [ ] Database file exists (`masons_financials.duckdb`)
- [ ] Dashboard shows data after upload
- [ ] All 3 views work (Consolidated, Region, Location)

If all checked ✅, system is working! 🎉
