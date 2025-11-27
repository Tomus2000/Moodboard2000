"""Diagnostic script to check if everything is set up correctly."""
import sys
import os

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

print("=" * 50)
print("Student Moodmeter - Diagnostic Script")
print("=" * 50)
print()

# Check Python version
print(f"Python version: {sys.version}")
print()

# Check if required modules can be imported
print("Checking imports...")
try:
    import streamlit
    print(f"[OK] Streamlit {streamlit.__version__}")
except ImportError as e:
    print(f"[ERROR] Streamlit: {e}")
    sys.exit(1)

try:
    import openai
    print(f"[OK] OpenAI {openai.__version__}")
except ImportError as e:
    print(f"[ERROR] OpenAI: {e}")

try:
    import pandas
    print(f"[OK] Pandas {pandas.__version__}")
except ImportError as e:
    print(f"[ERROR] Pandas: {e}")

try:
    import sqlmodel
    print(f"[OK] SQLModel {sqlmodel.__version__}")
except ImportError as e:
    print(f"[ERROR] SQLModel: {e}")

try:
    import plotly
    print(f"[OK] Plotly {plotly.__version__}")
except ImportError as e:
    print(f"[ERROR] Plotly: {e}")

try:
    import nltk
    print(f"[OK] NLTK {nltk.__version__}")
except ImportError as e:
    print(f"[ERROR] NLTK: {e}")

try:
    from wordcloud import WordCloud
    print(f"[OK] WordCloud")
except ImportError as e:
    print(f"[ERROR] WordCloud: {e}")

print()
print("Checking core modules...")
try:
    from core.config import APP_TITLE, APP_AUTH_PIN
    print(f"[OK] core.config - APP_TITLE: {APP_TITLE}, PIN: {APP_AUTH_PIN}")
except Exception as e:
    print(f"[ERROR] core.config: {e}")

try:
    from core.db import init_db
    init_db()
    print(f"[OK] core.db - Database initialized")
except Exception as e:
    print(f"[ERROR] core.db: {e}")

try:
    from core.ai import get_client
    client = get_client()
    if client:
        print(f"[OK] core.ai - OpenAI client available")
    else:
        print(f"[WARNING] core.ai - OpenAI client not available (no API key)")
except Exception as e:
    print(f"[ERROR] core.ai: {e}")

try:
    from core.styles import apply_beach_theme
    print(f"[OK] core.styles")
except Exception as e:
    print(f"[ERROR] core.styles: {e}")

try:
    from core.auth import check_auth
    print(f"[OK] core.auth")
except Exception as e:
    print(f"[ERROR] core.auth: {e}")

print()
print("Checking app.py...")
try:
    with open("app.py", "r", encoding="utf-8") as f:
        code = f.read()
        if "st.set_page_config" in code:
            print("[OK] app.py contains st.set_page_config")
        else:
            print("[ERROR] app.py missing st.set_page_config")
        if "import streamlit" in code:
            print("[OK] app.py imports streamlit")
        else:
            print("[ERROR] app.py missing streamlit import")
except Exception as e:
    print(f"[ERROR] Error reading app.py: {e}")

print()
print("Checking pages...")
pages_dir = "pages"
if os.path.exists(pages_dir):
    pages = [f for f in os.listdir(pages_dir) if f.endswith(".py")]
    print(f"[OK] Found {len(pages)} page(s): {', '.join(pages)}")
else:
    print(f"[ERROR] Pages directory not found")

print()
print("=" * 50)
print("Diagnostic complete!")
print("=" * 50)
print()
print("To start Streamlit, run:")
print("  py -m streamlit run app.py")
print()
print("If you see errors above, fix them first.")
print("If everything shows [OK], Streamlit should work!")

