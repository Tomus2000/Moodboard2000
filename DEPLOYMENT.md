# Deployment Guide - Student Moodmeter

This guide will help you deploy the Student Moodmeter app to Streamlit Cloud.

## Prerequisites

1. A GitHub account
2. Your repository pushed to GitHub
3. A Streamlit Cloud account (free at https://streamlit.io/cloud)
4. OpenAI API key (optional, for AI features)

## Step 1: Prepare Your Repository

### ✅ Already Done:
- ✅ All API keys are removed from code (using environment variables)
- ✅ `.gitignore` is configured to exclude `.env` files
- ✅ Code uses `os.getenv()` for all sensitive values

### What to Check:
1. Make sure your `.env` file is **NOT** committed to Git
2. Verify `requirements.txt` includes all dependencies
3. Ensure `app.py` is the main entry point

## Step 2: Push to GitHub

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

## Step 3: Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub account if not already connected
4. Select your repository
5. Set the main file path: `app.py`
6. Click "Deploy"

## Step 4: Configure Secrets in Streamlit Cloud

After deployment, you need to add your secrets:

1. In your Streamlit Cloud app dashboard, click "⚙️ Settings" (or "Manage app")
2. Click "Secrets" in the sidebar
3. Add the following secrets (one per line):

```toml
OPENAI_API_KEY = "your-actual-openai-api-key-here"
OPENAI_MODEL = "gpt-4o-mini"
APP_AUTH_PIN = "0000"
APP_TITLE = "Student Moodmeter 🌊"
APP_FOOTER = "Built with ❤️ using Streamlit"
DB_URL = "sqlite:///moodmeter.db"
```

**Optional secrets:**
```toml
HUGGINGFACE_API_KEY = "your-huggingface-api-key-here"
SENTIMENT_PROVIDER = "hf"
SENTIMENT_MODEL_ID = "cardiffnlp/twitter-roberta-base-sentiment-latest"
```

4. Click "Save"
5. Your app will automatically redeploy with the new secrets

## Step 5: Verify Deployment

1. Wait for the deployment to complete (usually 1-2 minutes)
2. Visit your app URL (e.g., `https://your-app-name.streamlit.app`)
3. Test the login with your PIN
4. Verify AI features work (if API key is set)

## Environment Variables Reference

All environment variables used by the app:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | No* | `""` | OpenAI API key for AI analysis |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | OpenAI model to use |
| `HUGGINGFACE_API_KEY` | No | `""` | HuggingFace API key (alternative) |
| `SENTIMENT_PROVIDER` | No | `hf` | Sentiment provider: `hf` or `openai` |
| `SENTIMENT_MODEL_ID` | No | `cardiffnlp/...` | HuggingFace model ID |
| `APP_AUTH_PIN` | No | `0000` | Authentication PIN |
| `APP_TITLE` | No | `Student Moodmeter 🌊` | App title |
| `APP_FOOTER` | No | `Built with ❤️ using Streamlit` | Footer text |
| `DB_URL` | No | `sqlite:///moodmeter.db` | Database URL |

*Required if you want AI analysis features

## Troubleshooting

### App fails to deploy
- Check that `app.py` exists in the root directory
- Verify `requirements.txt` is present and complete
- Check the deployment logs in Streamlit Cloud dashboard

### API errors after deployment
- Verify secrets are set correctly in Streamlit Cloud
- Check that API keys are valid and have credits
- Review error logs in the Streamlit Cloud dashboard

### Database issues
- Streamlit Cloud uses ephemeral storage - data may be lost on redeploy
- Consider using a persistent database (PostgreSQL, etc.) for production

### Import errors
- Make sure all dependencies are in `requirements.txt`
- Check that all Python files are in the correct directories
- Verify `core/__init__.py` exists

## Security Notes

✅ **Good practices already implemented:**
- No API keys in code
- `.env` files are gitignored
- Secrets are managed through Streamlit Cloud secrets
- API keys are only used via environment variables

⚠️ **Important:**
- Never commit `.env` files
- Never hardcode API keys
- Use Streamlit Cloud secrets for all sensitive values
- Rotate API keys if accidentally exposed

## Next Steps

After successful deployment:
1. Test all features (check-in, journal, analytics)
2. Share your app URL with users
3. Monitor usage and costs (if using OpenAI API)
4. Set up custom domain (optional, paid feature)

## Support

For issues with:
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **This app**: Check the README.md or open an issue

