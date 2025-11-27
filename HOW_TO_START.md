# How to Start Streamlit - Student Moodmeter 🌊

## Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download NLTK Data
```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Step 3: Start Streamlit

**Option A: Using the start script (Windows)**
```bash
start.bat
```

**Option B: Direct command**
```bash
streamlit run app.py
```

**Option C: If `streamlit` command not found**
```bash
python -m streamlit run app.py
```

**Option D: Using `py` launcher (Windows)**
```bash
py -m streamlit run app.py
```

## What Happens Next?

1. Streamlit will start the server
2. Your browser will automatically open to `http://localhost:8501`
3. If it doesn't open automatically, manually navigate to that URL
4. You'll see the login page
5. Enter your PIN (default: `0000` if you haven't changed it in `.env`)
6. Click "Login"

## Troubleshooting

### "streamlit: command not found"
- Try: `python -m streamlit run app.py`
- Or: `py -m streamlit run app.py` (Windows)
- Make sure Streamlit is installed: `pip install streamlit`

### "Python not found"
- Install Python 3.10+ from https://www.python.org/
- Make sure Python is added to PATH during installation
- Restart your terminal after installing Python

### "Module not found" errors
- Install dependencies: `pip install -r requirements.txt`
- Make sure you're in the project directory

### "NLTK data not found"
- Run: `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"`

### App opens but shows errors
- Check that `.env` file exists in the project root
- Make sure `OPENAI_API_KEY` is set (optional, app works without it)
- Check that you have write permissions for the database file

## First Time Setup

1. **Install Python 3.10+** (if not already installed)
   - Download from https://www.python.org/
   - Make sure to check "Add Python to PATH" during installation

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK data**
   ```bash
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
   ```

4. **Configure `.env` file**
   - The `.env` file should already exist
   - If not, create one with:
     ```
     OPENAI_API_KEY=your-api-key-here
     OPENAI_MODEL=gpt-4o-mini
     DB_URL=sqlite:///moodmeter.db
     APP_AUTH_PIN=0000
     ```

5. **Start the app**
   ```bash
   streamlit run app.py
   ```

## Stopping Streamlit

- Press `Ctrl+C` in the terminal where Streamlit is running
- Or close the terminal window

## Need Help?

- Check the `README.md` for full documentation
- Check the `SETUP.md` for detailed setup instructions
- Make sure all dependencies are installed: `pip install -r requirements.txt`

## Success!

Once Streamlit starts, you should see:
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Then open `http://localhost:8501` in your browser and login with your PIN!


