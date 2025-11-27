"""NLP utilities for text preprocessing, n-grams, and word clouds."""
import re
from typing import List, Dict, Tuple
from collections import Counter
import nltk
from wordcloud import WordCloud

# Download NLTK data if not available (for Streamlit Cloud)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Download required NLTK data (if not already downloaded)
try:
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt", quiet=True)
except Exception:
    pass

try:
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    STOPWORDS = set(stopwords.words("english"))
except Exception:
    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
        "be", "have", "has", "had", "do", "does", "did", "will", "would",
        "should", "could", "may", "might", "must", "can", "this", "that",
        "these", "those", "i", "you", "he", "she", "it", "we", "they",
        "me", "him", "her", "us", "them", "my", "your", "his", "her",
        "its", "our", "their", "what", "which", "who", "whom", "whose",
        "where", "when", "why", "how", "all", "each", "every", "both",
        "few", "more", "most", "other", "some", "such", "no", "nor",
        "not", "only", "own", "same", "so", "than", "too", "very",
    }


def clean_text(text: str) -> str:
    """Clean text by removing special characters and normalizing whitespace."""
    # Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    # Remove email addresses
    text = re.sub(r"\S+@\S+", "", text)
    # Remove phone numbers
    text = re.sub(r"\d{3}-\d{3}-\d{4}|\d{10}", "", text)
    # Remove special characters except spaces and punctuation
    text = re.sub(r"[^a-zA-Z0-9\s.,!?;:'-]", "", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def scrub_pii(text: str) -> str:
    """Remove personally identifiable information from text."""
    # Remove emails
    text = re.sub(r"\S+@\S+", "[EMAIL]", text)
    # Remove phone numbers
    text = re.sub(r"\d{3}-\d{3}-\d{4}|\d{10}", "[PHONE]", text)
    # Remove credit card numbers (basic pattern)
    text = re.sub(r"\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}", "[CARD]", text)
    # Remove SSN (basic pattern)
    text = re.sub(r"\d{3}-\d{2}-\d{4}", "[SSN]", text)
    return text


def tokenize(text: str, remove_stopwords: bool = True) -> List[str]:
    """Tokenize text and optionally remove stopwords."""
    text = clean_text(text.lower())
    try:
        tokens = word_tokenize(text)
    except Exception:
        tokens = text.split()
    
    if remove_stopwords:
        tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]
    
    return tokens


def extract_ngrams(tokens: List[str], n: int = 2) -> List[Tuple[str, ...]]:
    """Extract n-grams from tokens."""
    if len(tokens) < n:
        return []
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def get_top_ngrams(texts: List[str], n: int = 2, top_k: int = 10) -> List[Tuple[str, int]]:
    """Get top n-grams from a list of texts."""
    all_ngrams = []
    for text in texts:
        tokens = tokenize(text, remove_stopwords=True)
        ngrams = extract_ngrams(tokens, n)
        all_ngrams.extend(ngrams)
    
    counter = Counter(all_ngrams)
    top = counter.most_common(top_k)
    return [(" ".join(ngram), count) for ngram, count in top]


def get_wordcloud(text: str, width: int = 800, height: int = 400):
    """Generate word cloud image from text."""
    # Clean and tokenize
    tokens = tokenize(text, remove_stopwords=True)
    text_clean = " ".join(tokens)
    
    if not text_clean:
        return None
    
    try:
        from io import BytesIO
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color="white",
            max_words=100,
            colormap="viridis",
            relative_scaling=0.5,
        ).generate(text_clean)
        
        img = wordcloud.to_image()
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        return img_bytes
    except Exception:
        return None


def get_positive_negative_words(texts: List[str], top_k: int = 10) -> Tuple[List[str], List[str]]:
    """Extract positive and negative words (simple heuristic based on common words)."""
    # This is a simple heuristic - in a real app, you might use a sentiment lexicon
    positive_words = {
        "good", "great", "happy", "joy", "love", "excited", "amazing", "wonderful",
        "fantastic", "excellent", "best", "better", "nice", "pleased", "grateful",
        "thankful", "proud", "confident", "hopeful", "optimistic", "calm", "peaceful",
    }
    negative_words = {
        "bad", "terrible", "awful", "sad", "angry", "frustrated", "stressed", "worried",
        "anxious", "scared", "afraid", "disappointed", "upset", "mad", "hate", "difficult",
        "hard", "tough", "struggle", "pain", "hurt", "tired", "exhausted", "overwhelmed",
    }
    
    all_tokens = []
    for text in texts:
        tokens = tokenize(text, remove_stopwords=True)
        all_tokens.extend(tokens)
    
    counter = Counter(all_tokens)
    positive = [word for word, count in counter.most_common(top_k * 2) if word in positive_words][:top_k]
    negative = [word for word, count in counter.most_common(top_k * 2) if word in negative_words][:top_k]
    
    return positive, negative

