"""OpenAI integration for sentiment and emotion analysis."""
import os
import json
import re
from typing import Dict, List, Optional
from pathlib import Path
from openai import OpenAI
from core.config import OPENAI_API_KEY, OPENAI_MODEL, PROMPTS_DIR, EMOTIONS

# Load system prompt
SYSTEM_PROMPT_PATH = PROMPTS_DIR / "system.txt"
if SYSTEM_PROMPT_PATH.exists():
    SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
else:
    SYSTEM_PROMPT = (
        "You are a kind, concise mood analyst for students. "
        "You return JSON only. Detect overall sentiment (−1..1), "
        "a normalized distribution across emotions [joy, sad, anger, fear, anticipation, trust, surprise, disgust] "
        "that sums to 1, a 2–3 sentence summary, and two gentle suggestions. "
        "Avoid therapy; focus on day-to-day study actions and self-care."
    )


def get_client() -> Optional[OpenAI]:
    """Get OpenAI client if API key is available."""
    # Re-check API key at runtime (in case it's loaded from Streamlit secrets)
    api_key = OPENAI_API_KEY
    if not api_key:
        # Try to get it again at runtime (Streamlit context might be available now)
        from core.config import get_config
        api_key = get_config("OPENAI_API_KEY", "")
    
    if not api_key or api_key.strip() == "":
        return None
    
    try:
        return OpenAI(api_key=api_key.strip())
    except Exception:
        return None


def analyze_text(text: str, tags: Optional[List[str]] = None) -> Dict:
    """
    Analyze text and return sentiment, emotions, summary, and suggestions.
    
    Returns:
        dict with keys: sentiment, mood_score, emotions, summary, suggestions, model_used, tokens
    """
    client = get_client()
    
    # If no API key, return default values
    if not client:
        return {
            "sentiment": 0.0,
            "mood_score": 50,
            "emotions": {emotion: 0.125 for emotion in EMOTIONS},  # Equal distribution
            "summary": "AI analysis unavailable. Your entry has been saved.",
            "suggestions": ["Take a moment to reflect on your day", "Consider talking to someone you trust"],
            "model_used": "none",
            "tokens": 0,
        }
    
    # Build user prompt
    tags_str = ", ".join(tags) if tags else "none"
    user_prompt = f'''Text: """{text}"""

Tags: {tags_str}

Return JSON with keys:
- sentiment (float between -1 and 1)
- emotions (object with keys: joy, sad, anger, fear, anticipation, trust, surprise, disgust; values should sum to 1)
- summary (string, max 320 characters)
- suggestions (array of exactly 2 short strings)

Return only valid JSON, no other text.'''
    
    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=500,
        )
        
        content = response.choices[0].message.content
        model_used = response.model
        tokens = response.usage.total_tokens if response.usage else 0
        
        # Extract JSON from response
        json_str = content.strip()
        if "```json" in json_str:
            json_str = re.search(r"```json\s*(.*?)\s*```", json_str, re.DOTALL).group(1)
        elif "```" in json_str:
            json_str = re.search(r"```\s*(.*?)\s*```", json_str, re.DOTALL).group(1)
        elif "{" in json_str:
            json_str = re.search(r"\{.*\}", json_str, re.DOTALL).group(0)
        
        data = json.loads(json_str)
        
        # Sanitize and normalize
        sentiment = max(-1.0, min(1.0, float(data.get("sentiment", 0.0))))
        mood_score = int((sentiment + 1) * 50)
        
        # Normalize emotions
        emotions = data.get("emotions", {})
        # Ensure all emotions are present
        for emotion in EMOTIONS:
            if emotion not in emotions:
                emotions[emotion] = 0.0
        
        # Normalize to sum to 1
        total = sum(float(v) for v in emotions.values())
        if total == 0:
            emotions = {emotion: 1.0 / len(EMOTIONS) for emotion in EMOTIONS}
        else:
            emotions = {k: max(0.0, float(v)) / total for k, v in emotions.items()}
        
        # Get summary and suggestions
        summary = data.get("summary", "No summary available.")
        if len(summary) > 320:
            summary = summary[:317] + "..."
        
        suggestions = data.get("suggestions", [])
        if not isinstance(suggestions, list):
            suggestions = []
        suggestions = [str(s) for s in suggestions[:2]]
        while len(suggestions) < 2:
            suggestions.append("Take care of yourself today")
        
        return {
            "sentiment": sentiment,
            "mood_score": mood_score,
            "emotions": emotions,
            "summary": summary,
            "suggestions": suggestions,
            "model_used": model_used,
            "tokens": tokens,
        }
        
    except json.JSONDecodeError:
        # Retry once with stricter prompt
        try:
            retry_prompt = f'''Text: """{text}"""

Return JSON only with keys: sentiment (float -1 to 1), emotions (object with keys: joy, sad, anger, fear, anticipation, trust, surprise, disgust; values sum to 1), summary (string), suggestions (array of 2 strings).

JSON:'''
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Return only valid JSON. No other text."},
                    {"role": "user", "content": retry_prompt},
                ],
                temperature=0.1,
                max_tokens=500,
            )
            content = response.choices[0].message.content
            json_str = re.search(r"\{.*\}", content, re.DOTALL).group(0)
            data = json.loads(json_str)
            
            # Same sanitization as above
            sentiment = max(-1.0, min(1.0, float(data.get("sentiment", 0.0))))
            mood_score = int((sentiment + 1) * 50)
            emotions = data.get("emotions", {})
            for emotion in EMOTIONS:
                if emotion not in emotions:
                    emotions[emotion] = 0.0
            total = sum(float(v) for v in emotions.values()) or 1.0
            emotions = {k: max(0.0, float(v)) / total for k, v in emotions.items()}
            summary = data.get("summary", "No summary available.")[:320]
            suggestions = data.get("suggestions", [])[:2]
            while len(suggestions) < 2:
                suggestions.append("Take care of yourself today")
            
            return {
                "sentiment": sentiment,
                "mood_score": mood_score,
                "emotions": emotions,
                "summary": summary,
                "suggestions": suggestions,
                "model_used": response.model,
                "tokens": response.usage.total_tokens if hasattr(response, 'usage') else 0,
            }
        except Exception:
            # Final fallback
            return {
                "sentiment": 0.0,
                "mood_score": 50,
                "emotions": {emotion: 1.0 / len(EMOTIONS) for emotion in EMOTIONS},
                "summary": "Analysis unavailable. Your entry has been saved.",
                "suggestions": ["Take a moment to reflect", "Consider talking to someone"],
                "model_used": "error",
                "tokens": 0,
            }
    
    except Exception as e:
        # Graceful degradation - log error for debugging
        import logging
        error_msg = str(e)
        logging.error(f"OpenAI API error: {error_msg}")
        
        # User-friendly error messages
        if "401" in error_msg or "Incorrect API key" in error_msg or "Invalid API key" in error_msg:
            user_message = "API key is invalid or expired. Please check your OpenAI API key in settings. Your entry has been saved."
        elif "429" in error_msg or "rate limit" in error_msg.lower():
            user_message = "API rate limit reached. Please try again later. Your entry has been saved."
        elif "500" in error_msg or "503" in error_msg:
            user_message = "OpenAI service is temporarily unavailable. Please try again later. Your entry has been saved."
        else:
            user_message = "AI analysis is temporarily unavailable. Your entry has been saved."
        
        return {
            "sentiment": 0.0,
            "mood_score": 50,
            "emotions": {emotion: 1.0 / len(EMOTIONS) for emotion in EMOTIONS},
            "summary": user_message,
            "suggestions": ["Take a moment to reflect", "Consider talking to someone"],
            "model_used": "error",
            "tokens": 0,
        }

