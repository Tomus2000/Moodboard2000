"""Export and import functionality for entries."""
import json
import csv
import io
from typing import List, Dict
from datetime import datetime
from core.db import Entry, add_entry, get_or_create_user


def export_to_csv(entries: List[Entry]) -> str:
    """Export entries to CSV format."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "id", "user_id", "created_at", "text", "summary",
        "sentiment", "mood_score", "emotions_json", "tags",
        "source", "model_used", "tokens",
    ])
    
    # Data rows
    for entry in entries:
        writer.writerow([
            entry.id,
            entry.user_id,
            datetime.fromtimestamp(entry.created_at).isoformat(),
            entry.text,
            entry.summary,
            entry.sentiment,
            entry.mood_score,
            entry.emotions_json,
            entry.tags,
            entry.source,
            entry.model_used,
            entry.tokens,
        ])
    
    return output.getvalue()


def export_to_json(entries: List[Entry]) -> str:
    """Export entries to JSON format."""
    data = []
    for entry in entries:
        data.append({
            "id": entry.id,
            "user_id": entry.user_id,
            "created_at": datetime.fromtimestamp(entry.created_at).isoformat(),
            "text": entry.text,
            "summary": entry.summary,
            "sentiment": entry.sentiment,
            "mood_score": entry.mood_score,
            "emotions": json.loads(entry.emotions_json),
            "tags": entry.tags.split(",") if entry.tags else [],
            "source": entry.source,
            "model_used": entry.model_used,
            "tokens": entry.tokens,
        })
    
    return json.dumps(data, indent=2)


def import_from_csv(csv_content: str, user_id: int) -> Dict[str, int]:
    """Import entries from CSV content."""
    reader = csv.DictReader(io.StringIO(csv_content))
    
    imported = 0
    errors = 0
    
    for row in reader:
        try:
            # Parse datetime
            created_at = datetime.fromisoformat(row["created_at"])
            created_at_ts = int(created_at.timestamp())
            
            # Parse emotions
            emotions_json = row.get("emotions_json", "{}")
            try:
                emotions = json.loads(emotions_json)
            except Exception:
                emotions = {}
            
            # Parse tags
            tags = row.get("tags", "")
            
            # Create entry
            add_entry(
                user_id=user_id,
                text=row["text"],
                summary=row.get("summary", ""),
                sentiment=float(row.get("sentiment", 0.0)),
                mood_score=int(row.get("mood_score", 50)),
                emotions=emotions,
                tags=tags,
                source=row.get("source", "import"),
                model_used=row.get("model_used", ""),
                tokens=int(row.get("tokens", 0)),
            )
            imported += 1
        except Exception as e:
            errors += 1
            continue
    
    return {"imported": imported, "errors": errors}


def import_from_json(json_content: str, user_id: int) -> Dict[str, int]:
    """Import entries from JSON content."""
    data = json.loads(json_content)
    
    imported = 0
    errors = 0
    
    for item in data:
        try:
            # Parse datetime
            created_at = datetime.fromisoformat(item["created_at"])
            created_at_ts = int(created_at.timestamp())
            
            # Parse emotions
            emotions = item.get("emotions", {})
            
            # Parse tags
            tags = item.get("tags", [])
            if isinstance(tags, list):
                tags = ",".join(tags)
            else:
                tags = str(tags)
            
            # Create entry
            add_entry(
                user_id=user_id,
                text=item["text"],
                summary=item.get("summary", ""),
                sentiment=float(item.get("sentiment", 0.0)),
                mood_score=int(item.get("mood_score", 50)),
                emotions=emotions,
                tags=tags,
                source=item.get("source", "import"),
                model_used=item.get("model_used", ""),
                tokens=int(item.get("tokens", 0)),
            )
            imported += 1
        except Exception as e:
            errors += 1
            continue
    
    return {"imported": imported, "errors": errors}


