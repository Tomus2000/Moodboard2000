import os
import json
from typing import Any, Dict, List, Tuple

import requests
import streamlit as st
from dotenv import load_dotenv
import yake

# Optional OpenAI chat for supportive message and sentiment fallback
try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover
    OpenAI = None  # type: ignore

# Load env vars
load_dotenv()

APP_TITLE = os.getenv("APP_TITLE", "How Are You Feeling? 💛")
APP_FOOTER = os.getenv("APP_FOOTER", "Built with ❤️ using Streamlit.")
SENTIMENT_PROVIDER = os.getenv("SENTIMENT_PROVIDER", "hf")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
SENTIMENT_MODEL_ID = os.getenv("SENTIMENT_MODEL_ID", "cardiffnlp/twitter-roberta-base-sentiment-latest")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

st.set_page_config(page_title=APP_TITLE, page_icon="💛")
st.title(APP_TITLE)

prompt = st.text_area("What's on your mind?", height=120, placeholder="Type a sentence to analyze your sentiment...")

analyze = st.button("Analyze sentiment")


def _normalize_hf_output(data: Any) -> List[Dict[str, Any]]:
    # HF sentiment may return [[{label, score}...]] or [{label, score}...]
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
        return data[0]
    if isinstance(data, list):
        return data
    return []


def _top_label(items: List[Dict[str, Any]]) -> Tuple[str, float]:
    if not items:
        return ("unknown", 0.0)
    best = max(items, key=lambda x: x.get("score", 0.0))
    return best.get("label", "unknown"), float(best.get("score", 0.0))


def extract_keywords(text: str, top_k: int = 5) -> List[str]:
    kw_extractor = yake.KeywordExtractor(lan="en", n=1, top=top_k)
    keywords_with_scores = kw_extractor.extract_keywords(text)
    # YAKE returns list of (keyword, score). Lower score is more important.
    keywords_sorted = sorted(keywords_with_scores, key=lambda x: x[1])
    return [kw for kw, _ in keywords_sorted[:top_k]]


def craft_support_message(sentiment_label: str, confidence: float, keywords: List[str]) -> str:
    key_text = ", ".join(keywords[:5]) if keywords else "your thoughts"
    friendly_conf = f"{confidence:.2f}"
    label = sentiment_label.lower()
    if "neg" in label or label in {"negative", "sad", "anger", "fear"}:
        return (
            f"Thank you for sharing. It sounds difficult, and your feelings are valid. "
            f"You're not alone in this — taking a moment to notice {key_text} is a brave step. "
            f"On a scale of 0–1, we sensed a {label} tone (confidence {friendly_conf}). "
            "Try one gentle action today: take three slow breaths, stretch your shoulders, or message someone you trust."
        )
    if "pos" in label or label in {"positive", "joy", "love"}:
        return (
            f"That's wonderful to hear! Noticing {key_text} shows what matters to you. "
            f"We sensed a positive tone (confidence {friendly_conf}). "
            "Consider jotting down one thing you're grateful for to reinforce this feeling."
        )
    # neutral / mixed
    return (
        f"Thanks for opening up. We picked up a more neutral or mixed tone (confidence {friendly_conf}). "
        f"Your focus on {key_text} matters. "
        "If you'd like, set a tiny goal for the next hour — a short walk, a glass of water, or a quick stretch."
    )


def chat_support_message(user_text: str, sentiment_label: str, confidence: float, keywords: List[str]) -> str:
    if not OPENAI_API_KEY or OpenAI is None:
        return craft_support_message(sentiment_label, confidence, keywords)

    system = (
        "You are a caring school counselor. Respond in 1 short paragraph (max 70 words). "
        "Acknowledge the student's feelings, reflect gently, and offer 1-2 simple, practical steps. "
        "Be warm, inclusive, and age-appropriate (teen). Avoid clinical language."
    )
    key_text = ", ".join(keywords[:5]) if keywords else "their thoughts"
    user = (
        f"Student text: {user_text}\n"
        f"Detected sentiment: {sentiment_label} (confidence {confidence:.2f}).\n"
        f"Keywords: {key_text}.\n"
        "Compose a supportive, heartwarming reply as instructed."
    )
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.7,
            max_tokens=140,
        )
        content = completion.choices[0].message.get("content", "").strip()
        return content or craft_support_message(sentiment_label, confidence, keywords)
    except Exception:
        return craft_support_message(sentiment_label, confidence, keywords)


@st.cache_data(show_spinner=False)
def hf_sentiment(text: str) -> Any:
    if not HUGGINGFACE_API_KEY:
        raise ValueError("HUGGINGFACE_API_KEY is not set.")
    api_url = f"https://api-inference.huggingface.co/models/{SENTIMENT_MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    payload = {"inputs": text, "options": {"wait_for_model": True}}
    response = requests.post(api_url, headers=headers, json=payload, timeout=60)
    if response.status_code >= 400:
        try:
            err = response.json()
        except Exception:
            response.raise_for_status()
        raise RuntimeError(err.get("error") or err)
    return response.json()


@st.cache_data(show_spinner=False)
def openai_sentiment(text: str) -> List[Dict[str, Any]]:
    if not OPENAI_API_KEY or OpenAI is None:
        raise ValueError("OPENAI_API_KEY is not set or OpenAI client unavailable.")
    client = OpenAI(api_key=OPENAI_API_KEY)
    system = (
        "Classify the overall sentiment as one of: positive, neutral, negative. "
        "Return a single JSON object with fields 'label' (string) and 'score' (0..1). "
        "The 'score' should reflect confidence. Do not include any other text."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": f"Text: {text}"},
    ]
    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.0,
        max_tokens=60,
    )
    content = completion.choices[0].message.get("content", "{}").strip()
    try:
        data = json.loads(content)
        label = str(data.get("label", "neutral")).lower()
        score = float(data.get("score", 0.5))
        return [{"label": label, "score": score}]
    except Exception:
        # Fallback naive heuristic if parsing failed
        return [{"label": "neutral", "score": 0.5}]


col1, col2 = st.columns(2)

if analyze:
    if not prompt.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Analyzing..."):
            try:
                provider_used = SENTIMENT_PROVIDER
                if SENTIMENT_PROVIDER == "hf" and HUGGINGFACE_API_KEY:
                    raw = hf_sentiment(prompt.strip())
                    items = _normalize_hf_output(raw)
                elif OPENAI_API_KEY and OpenAI is not None:
                    provider_used = "openai"
                    items = openai_sentiment(prompt.strip())
                else:
                    raise ValueError("No sentiment provider available. Set HUGGINGFACE_API_KEY or OPENAI_API_KEY.")

                label, score = _top_label(items)
                result = {"label": label, "confidence": round(score, 4), "raw": items, "provider": provider_used}

                # Keywords and message
                keywords = extract_keywords(prompt.strip(), top_k=5)
                if OPENAI_API_KEY and OpenAI is not None:
                    message = chat_support_message(prompt.strip(), result["label"], result["confidence"], keywords)
                else:
                    message = craft_support_message(result["label"], result["confidence"], keywords)
            except Exception as e:
                st.error(f"Error: {e}")
                result = None
                keywords = []
                message = None

        if result is not None:
            st.subheader("Result")
            st.metric("Sentiment", result["label"], delta=f"confidence {result['confidence']:.2f}")
            st.caption(f"Provider: {result['provider']}")
            if keywords:
                st.write("Keywords:", ", ".join(keywords))
            if message:
                st.success(message)
            with st.expander("Raw response"):
                st.json(result["raw"])
        else:
            if not (HUGGINGFACE_API_KEY or OPENAI_API_KEY):
                st.info("Set OPENAI_API_KEY or HUGGINGFACE_API_KEY in your .env and restart the app.")

st.divider()
st.caption(APP_FOOTER)
