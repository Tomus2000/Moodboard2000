# GitHub Secrets Configuration

When deploying to Streamlit Cloud, you'll need to add these secrets in the Streamlit Cloud dashboard.

## Required Secrets (for full functionality)

Add these in Streamlit Cloud → Your App → Settings → Secrets:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
OPENAI_MODEL = "gpt-4o-mini"
APP_AUTH_PIN = "0000"
```

## Optional Secrets

```toml
# HuggingFace (alternative sentiment analysis)
HUGGINGFACE_API_KEY = "your-huggingface-api-key-here"
SENTIMENT_PROVIDER = "hf"
SENTIMENT_MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"

# App customization
APP_TITLE = "Student Moodmeter 🌊"
APP_FOOTER = "Built with ❤️ using Streamlit"
DB_URL = "sqlite:///moodmeter.db"
```

## How to Add Secrets in Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Select your app
3. Click "⚙️ Settings" or "Manage app"
4. Click "Secrets" in the sidebar
5. Paste the secrets in TOML format (as shown above)
6. Click "Save"
7. Your app will automatically redeploy

## Security Notes

- ✅ Never commit secrets to Git
- ✅ Use Streamlit Cloud secrets for all sensitive values
- ✅ Rotate API keys if accidentally exposed
- ✅ The `.env` file is already in `.gitignore`

## Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add it to Streamlit Cloud secrets as `OPENAI_API_KEY`

**Note:** The app works without an API key, but AI analysis features will be disabled.

