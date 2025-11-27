# Quick Deploy Check - What to Verify

## Files That MUST Be in GitHub:

✅ `app.py` - Main file (MUST be in root)
✅ `requirements.txt` - Dependencies (MUST be in root)
✅ `core/` folder - With all Python files
✅ `core/__init__.py` - MUST exist (can be empty)
✅ `pages/` folder - With all page files
✅ `.streamlit/config.toml` - Optional but helpful

## Streamlit Cloud Settings:

- **Repository:** Your GitHub repo (e.g., `Tomus2000/Moodboard2000`)
- **Branch:** `main` (or `master` if that's your default)
- **Main file path:** `app.py` (exactly this, no path)

## Common Issues:

1. **"Error installing requirements"**
   - Check `requirements.txt` is in root
   - Make sure no syntax errors
   - Current version has no version pins (should work)

2. **"No module named 'core'"**
   - Make sure `core/__init__.py` exists
   - Make sure `core/` folder is in root (not in a subfolder)
   - Check that `app.py` is in root

3. **Still failing?**
   - Go to Streamlit Cloud → Your App → "Manage App" → "Terminal"
   - Copy the EXACT error message
   - Share it so I can fix it

## What I Just Fixed:

- Updated `app.py` to use absolute paths
- Added `os.chdir()` to ensure correct working directory
- Simplified `requirements.txt` (no version pins)
- Updated `.streamlit/config.toml`

## Next Steps:

1. Push everything to GitHub
2. Deploy on Streamlit Cloud with:
   - Branch: `main`
   - Main file: `app.py`
3. If it fails, check the terminal logs and share the error

