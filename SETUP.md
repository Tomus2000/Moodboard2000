# Student Moodmeter - Setup Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download NLTK Data**
   ```bash
   python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
   ```

3. **Configure Environment**
   - Copy `.env.example` to `.env`
   - Set your `OPENAI_API_KEY` in `.env`
   - Configure `APP_AUTH_PIN` (default: 0000)

4. **Add Beach Image (Optional)**
   - Add a beach-themed image to `assets/beach.jpg`
   - The app will use a gradient fallback if not found

5. **Run the App**
   ```bash
   streamlit run app.py
   ```

6. **Access the App**
   - Open your browser to `http://localhost:8501`
   - Login with your PIN (default: 0000)

## Project Structure

```
feelings-app/
├── app.py                  # Main entry point
├── pages/                  # Streamlit multipage pages
│   ├── 1_Check_in.py      # Mood check-in page
│   ├── 2_Journal.py       # Journal viewing page
│   ├── 3_Analytics.py     # Analytics dashboard
│   ├── 4_Cohort_Compare.py # Cohort comparison (teacher mode)
│   └── 5_Settings.py      # Settings page
├── core/                   # Core modules
│   ├── __init__.py
│   ├── ai.py              # OpenAI integration
│   ├── auth.py            # Authentication
│   ├── charts.py          # Chart utilities
│   ├── config.py          # Configuration
│   ├── db.py              # Database models and CRUD
│   ├── export_import.py   # Export/import functionality
│   ├── nlp_utils.py       # NLP utilities
│   └── styles.py          # Shared styles
├── prompts/               # AI prompts
│   └── system.txt         # System prompt for OpenAI
├── assets/                # Static assets
│   ├── beach.jpg          # Beach background image (optional)
│   └── README.md          # Assets documentation
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── README.md             # Main documentation
└── SETUP.md              # This file
```

## Features

### ✅ Implemented

- **Mood Check-in**: AI-powered sentiment and emotion analysis
- **Journal**: View and search entries with filters
- **Analytics**: Comprehensive mood insights and visualizations
- **Cohort Comparison**: Teacher mode for comparing cohorts
- **Export/Import**: CSV and JSON export/import
- **Privacy**: PII scrubbing option, local storage
- **Beach Theme**: Calm, beach-themed UI with glassmorphism
- **Authentication**: PIN-based or username/password
- **Streaks**: Daily streak tracking with shell awards
- **Word Cloud**: Word cloud generation from journal text
- **Charts**: Time series, radar, heatmaps, calendar views

### 🔧 Configuration

- **OpenAI API**: Set `OPENAI_API_KEY` in `.env`
- **Database**: SQLite database (default: `moodmeter.db`)
- **Authentication**: Set `APP_AUTH_PIN` in `.env`
- **Theme**: Add `assets/beach.jpg` for beach theme

## Database Schema

### Tables

- **users**: User accounts (id, username, role, created_at)
- **entries**: Mood entries (id, user_id, created_at, text, summary, sentiment, mood_score, emotions_json, tags, source, timezone, model_used, tokens)
- **cohorts**: Student cohorts (id, name, created_at)
- **cohort_members**: Cohort membership (id, user_id, cohort_id)

## AI Analysis

The app uses OpenAI's Chat Completions API to:
- Detect overall sentiment (-1 to +1)
- Identify emotion distribution (8 emotions)
- Generate a 2-3 sentence summary
- Provide two gentle suggestions

If OpenAI API is unavailable, the app degrades gracefully by storing text only.

## Privacy

- All data is stored locally in SQLite
- PII scrubbing option available
- Teacher mode shows only aggregated data
- No external services beyond OpenAI (optional)

## Troubleshooting

### Issue: Python not found
- Install Python 3.10+ from python.org
- Or use `py` command on Windows: `py -m streamlit run app.py`

### Issue: OpenAI API errors
- Check your API key in `.env`
- Verify you have credits in your OpenAI account
- The app will work without OpenAI (text storage only)

### Issue: NLTK data not found
- Run: `python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"`

### Issue: Beach image not showing
- Add `assets/beach.jpg` or the app will use a gradient fallback
- Image should be JPG format, 1920x1080 or larger

## Next Steps

1. Add your OpenAI API key to `.env`
2. Add a beach image to `assets/beach.jpg` (optional)
3. Run `streamlit run app.py`
4. Login with your PIN
5. Start checking in with your mood!

## Support

For issues or questions, please check the README.md or open an issue on GitHub.


