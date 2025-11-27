# Requirements Fix for Streamlit Cloud

## Issue: "Error installing requirements"

### Problem
Streamlit Cloud was failing to install dependencies, likely due to:
- YAKE package compatibility issues
- Version conflicts
- Missing dependencies

### Solution
1. **Removed YAKE from requirements.txt** - It's only used in `feelings_app_streamlit.py`, not in the main `app.py` that's being deployed
2. **Simplified requirements** - Removed optional dependencies that aren't needed for the main app

### What Changed
- Removed `yake>=0.4.8` (not used in main app)
- Removed `pyphen>=0.14.0` (dependency of YAKE)

### If You Need YAKE Later
If you want to use `feelings_app_streamlit.py` which requires YAKE, you can:
1. Install it manually: `pip install yake`
2. Or add it back to requirements.txt if Streamlit Cloud supports it

### Next Steps
1. Commit and push the updated `requirements.txt`:
   ```bash
   git add requirements.txt
   git commit -m "Fix requirements.txt for Streamlit Cloud"
   git push origin main
   ```
2. Streamlit Cloud will automatically redeploy
3. The installation should now succeed

