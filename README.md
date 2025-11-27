# Student Moodmeter 🌊

A calm, beach-themed web app where students check in their mood, journal briefly, and get AI sentiment + emotion analysis, trend insights, and gentle suggestions.

## Features

- **Mood Check-in**: Type a short note and get AI-powered sentiment and emotion analysis
- **Journal**: View and search your entries with filters by date, tags, and sentiment
- **Analytics Dashboard**: Comprehensive mood insights with charts and visualizations
- **Cohort Comparison**: Teacher mode for comparing anonymized class sections
- **Export/Import**: Export your data as CSV or JSON, import for migration
- **Privacy-Focused**: Local SQLite storage, PII scrubbing option, no external services beyond OpenAI

## Tech Stack

- **Frontend**: Streamlit
- **Language**: Python 3.10+
- **AI**: OpenAI Chat Completions (configurable model)
- **Database**: SQLite with SQLModel/SQLAlchemy
- **Charts**: Plotly Express + Altair
- **NLP**: NLTK, WordCloud, YAKE
- **Authentication**: Simple PIN-based or username/password

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd feelings-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data:
```python
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

4. Create a `.env` file from `.env.example`:
```bash
cp .env.example .env
```

5. Configure your `.env` file:
```env
OPENAI_API_KEY=sk-xxxxx
OPENAI_MODEL=gpt-4o-mini
DB_URL=sqlite:///moodmeter.db
APP_AUTH_PIN=0000
```

6. Add a beach image to `assets/beach.jpg` (optional, but recommended for the full experience)

## Usage

1. Run the app:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Login with the PIN configured in your `.env` file (default: 0000)

4. Start checking in with your mood!

## Pages

- **Home / Check-in**: Default page for mood check-in
- **Journal**: View and search entries
- **Analytics**: Comprehensive mood analytics dashboard
- **Cohort Compare**: Teacher mode for comparing cohorts (off by default)
- **Settings**: Configuration, export/import, privacy settings

## Data Model

### Tables

- **users**: User accounts (id, username, role, created_at)
- **entries**: Mood entries (id, user_id, created_at, text, summary, sentiment, mood_score, emotions_json, tags, source, timezone, model_used, tokens)
- **cohorts**: Student cohorts (id, name, created_at)
- **cohort_members**: Cohort membership (id, user_id, cohort_id)

## Analytics

- **Mood Index**: Rescaled sentiment to 0-100
- **Time-series**: Daily average mood score
- **Calendar Heatmap**: Month view of mood scores
- **Emotion Radar**: Radar chart of average emotion weights
- **Word Cloud**: From journal text (stopwords removed)
- **Tag Frequency**: Bar chart of tag frequencies
- **Hour-of-day Heatmap**: Mood by hour and day of week
- **Insight Call-outs**: Most positive day, top stress tag, etc.

## AI Behavior

The app uses OpenAI's Chat Completions API to:
- Detect overall sentiment (-1 to +1)
- Identify emotion distribution (joy, sad, anger, fear, anticipation, trust, surprise, disgust)
- Generate a 2-3 sentence summary
- Provide two gentle suggestions

If OpenAI API is unavailable, the app degrades gracefully by storing text only and skipping AI analysis.

## Privacy

- Everything is stored locally in SQLite
- No external services beyond OpenAI (optional)
- PII scrubbing option (emails, phone numbers)
- Teacher mode shows only aggregated data, no raw text

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key (required for AI analysis)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `DB_URL`: Database URL (default: sqlite:///moodmeter.db)
- `APP_AUTH_PIN`: Authentication PIN (default: 0000)
- `APP_USERNAME`: Username for authentication (optional)
- `APP_PASSWORD`: Password for authentication (optional)
- `APP_TITLE`: App title (default: Student Moodmeter 🌊)
- `APP_FOOTER`: App footer text (default: Built with ❤️ using Streamlit)

## Requirements

- Python 3.10+
- Streamlit
- OpenAI API key (optional, for AI analysis)
- SQLite (included with Python)

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on GitHub.

## Acknowledgments

- Built with Streamlit
- AI powered by OpenAI
- Charts by Plotly and Altair
- Beach theme inspired by calm, soothing designs


