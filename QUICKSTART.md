# Quick Start Guide - Student Moodmeter

## Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

## Step 2: Download NLTK Data

Run this command to download required NLTK data:

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

## Step 3: Create .env File

Create a `.env` file in the project root with the following content:

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4o-mini
DB_URL=sqlite:///moodmeter.db
APP_AUTH_PIN=0000
```

**Note:** You can get an OpenAI API key from https://platform.openai.com/api-keys
If you don't have an API key, the app will still work but won't provide AI analysis.

## Step 4: Start Streamlit

Run this command:

```bash
streamlit run app.py
```

Or on Windows if `streamlit` is not found:

```bash
py -m streamlit run app.py
```

Or:

```bash
python -m streamlit run app.py
```

## Step 5: Open in Browser

Streamlit will automatically open your browser to `http://localhost:8501`

If it doesn't open automatically, navigate to that URL in your browser.

## Step 6: Login

- **PIN:** Enter the PIN from your `.env` file (default: `0000`)
- Click "Login"

## That's it! 🎉

You should now see the Student Moodmeter app with the beach theme.

## Troubleshooting

### "streamlit: command not found"
- Try: `py -m streamlit run app.py` (Windows)
- Or: `python -m streamlit run app.py`
- Make sure Streamlit is installed: `pip install streamlit`

### "Module not found" errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`

### "NLTK data not found"
- Run: `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"`

### App opens but shows errors
- Check that your `.env` file exists and has the correct format
- Make sure the database file can be created (check file permissions)

## Next Steps

1. Add a beach image to `assets/beach.jpg` for the full theme experience (optional)
2. Start checking in with your mood!
3. Explore the Analytics dashboard
4. Export your data from Settings


