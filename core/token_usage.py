"""Token usage and cost calculation utilities."""
from typing import Dict, List, Tuple
from core.db import Entry


# OpenAI pricing per 1M tokens (as of 2024)
# Prices are in USD per million tokens
MODEL_PRICING = {
    "gpt-4o-mini": {
        "input": 0.15 / 1_000_000,  # $0.15 per 1M tokens
        "output": 0.60 / 1_000_000,  # $0.60 per 1M tokens
    },
    "gpt-4o-mini-2024-07-18": {
        "input": 0.15 / 1_000_000,
        "output": 0.60 / 1_000_000,
    },
    "gpt-3.5-turbo": {
        "input": 0.50 / 1_000_000,  # $0.50 per 1M tokens
        "output": 1.50 / 1_000_000,  # $1.50 per 1M tokens
    },
    "gpt-4o": {
        "input": 2.50 / 1_000_000,  # $2.50 per 1M tokens
        "output": 10.00 / 1_000_000,  # $10.00 per 1M tokens
    },
    "gpt-4": {
        "input": 30.00 / 1_000_000,  # $30.00 per 1M tokens
        "output": 60.00 / 1_000_000,  # $60.00 per 1M tokens
    },
}

# Default pricing if model not found
DEFAULT_PRICING = {
    "input": 0.50 / 1_000_000,
    "output": 1.50 / 1_000_000,
}


def get_model_pricing(model_name: str) -> Dict[str, float]:
    """Get pricing for a specific model."""
    # Try exact match
    if model_name in MODEL_PRICING:
        return MODEL_PRICING[model_name]
    
    # Try partial match (e.g., "gpt-4o-mini" for "gpt-4o-mini-2024-07-18")
    for model, pricing in MODEL_PRICING.items():
        if model_name.startswith(model.split("-")[0]):
            return pricing
    
    return DEFAULT_PRICING


def calculate_token_cost(tokens: int, model_name: str) -> float:
    """
    Calculate cost for tokens based on model.
    
    Since we store total_tokens, we estimate:
    - Input tokens: ~70% of total
    - Output tokens: ~30% of total
    """
    if tokens == 0:
        return 0.0
    
    pricing = get_model_pricing(model_name)
    
    # Estimate input/output distribution
    input_tokens = int(tokens * 0.7)
    output_tokens = tokens - input_tokens
    
    input_cost = input_tokens * pricing["input"]
    output_cost = output_tokens * pricing["output"]
    
    return input_cost + output_cost


def get_token_usage_stats(entries: List[Entry]) -> Dict:
    """Get comprehensive token usage statistics."""
    total_tokens = 0
    total_cost = 0.0
    entries_with_tokens = 0
    model_usage = {}
    
    for entry in entries:
        if entry.tokens > 0:
            total_tokens += entry.tokens
            entries_with_tokens += 1
            
            model_name = entry.model_used or "unknown"
            cost = calculate_token_cost(entry.tokens, model_name)
            total_cost += cost
            
            if model_name not in model_usage:
                model_usage[model_name] = {
                    "tokens": 0,
                    "count": 0,
                    "cost": 0.0,
                }
            
            model_usage[model_name]["tokens"] += entry.tokens
            model_usage[model_name]["count"] += 1
            model_usage[model_name]["cost"] += cost
    
    return {
        "total_tokens": total_tokens,
        "total_cost": total_cost,
        "entries_with_tokens": entries_with_tokens,
        "average_tokens_per_entry": total_tokens / entries_with_tokens if entries_with_tokens > 0 else 0,
        "model_usage": model_usage,
    }


