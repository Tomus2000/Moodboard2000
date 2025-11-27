# How to Add API Key to Streamlit Cloud

**IMPORTANT:** GitHub Actions secrets and Streamlit Cloud secrets are **different systems**. 
You have the key in GitHub Actions secrets, but you also need to add it to Streamlit Cloud.

## Quick Steps:

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io/
   - Log in with your GitHub account
   - Select your app (Moodboard2000)

2. **Open Secrets:**
   - Click "⚙️ Settings" (gear icon) or "Manage app"
   - Click "Secrets" in the sidebar

3. **Add Your API Key:**
   - Copy your API key from GitHub (or get it from OpenAI)
   - Paste this into the secrets field:
   
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   OPENAI_MODEL = "gpt-4o-mini"
   APP_AUTH_PIN = "0000"
   ```

4. **Save:**
   - Click "Save"
   - Your app will automatically redeploy (takes ~1-2 minutes)

5. **Verify:**
   - Go to your app's Settings page
   - Check that "API Key Status" shows ✅ Configured

## Why Both?

- **GitHub Actions Secrets**: Used for GitHub Actions workflows (CI/CD)
- **Streamlit Cloud Secrets**: Used by your Streamlit app when it runs

They're separate systems, so you need the key in both places if you use both.

## Need Help?

If the key still doesn't work after adding to Streamlit Cloud:
1. Check the app logs in Streamlit Cloud dashboard
2. Verify the key starts with "sk-"
3. Make sure there are no extra spaces or quotes
4. Wait 1-2 minutes for redeploy to complete

