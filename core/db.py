"""Database models and CRUD operations using SQLModel."""
import json
import time
from typing import Optional, List
from datetime import datetime, timedelta
from sqlmodel import SQLModel, Field, create_engine, Session, select
from core.config import DB_URL

# Create engine with extend_existing to handle module reloads
engine = create_engine(DB_URL, echo=False)

# Define models with extend_existing=True to handle Streamlit module reloads
# This prevents errors when Streamlit reloads modules on page navigation
# Using __table_args__ with extend_existing=True allows redefinition during module reloads

class User(SQLModel, table=True):
    """User model."""
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    role: str = Field(default="student")  # student, teacher
    created_at: int = Field(default_factory=lambda: int(time.time()))


class Entry(SQLModel, table=True):
    """Mood entry model."""
    __tablename__ = "entry"
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: int = Field(default_factory=lambda: int(time.time()), index=True)
    text: str
    summary: str = ""
    sentiment: float = 0.0
    mood_score: int = 50
    emotions_json: str = "{}"
    tags: str = ""
    source: str = "manual"
    timezone: str = ""
    model_used: str = ""
    tokens: int = 0


class Cohort(SQLModel, table=True):
    """Cohort model for grouping students."""
    __tablename__ = "cohort"
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: int = Field(default_factory=lambda: int(time.time()))


class CohortMember(SQLModel, table=True):
    """Cohort membership model."""
    __tablename__ = "cohortmember"
    __table_args__ = {"extend_existing": True}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    cohort_id: int = Field(foreign_key="cohort.id", index=True)


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


def get_or_create_user(username: str = "default", role: str = "student") -> User:
    """Get or create a user."""
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            user = User(username=username, role=role)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user


def add_entry(
    user_id: int,
    text: str,
    summary: str = "",
    sentiment: float = 0.0,
    mood_score: int = 50,
    emotions: dict = None,
    tags: str = "",
    source: str = "manual",
    model_used: str = "",
    tokens: int = 0,
) -> Entry:
    """Add a new entry."""
    emotions_json = json.dumps(emotions or {})
    entry = Entry(
        user_id=user_id,
        text=text,
        summary=summary,
        sentiment=sentiment,
        mood_score=mood_score,
        emotions_json=emotions_json,
        tags=tags,
        source=source,
        model_used=model_used,
        tokens=tokens,
    )
    with Session(engine) as session:
        session.add(entry)
        session.commit()
        session.refresh(entry)
        return entry


def get_entries(
    user_id: int = 1,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    tags: Optional[List[str]] = None,
    limit: Optional[int] = None,
) -> List[Entry]:
    """Get entries with optional filters."""
    with Session(engine) as session:
        stmt = select(Entry).where(Entry.user_id == user_id)
        
        if start_date:
            start_ts = int(start_date.timestamp())
            stmt = stmt.where(Entry.created_at >= start_ts)
        
        if end_date:
            end_ts = int(end_date.timestamp())
            stmt = stmt.where(Entry.created_at <= end_ts)
        
        if tags:
            # Filter by tags (comma-separated in database)
            for tag in tags:
                stmt = stmt.where(Entry.tags.contains(tag))
        
        stmt = stmt.order_by(Entry.created_at.desc())
        
        if limit:
            stmt = stmt.limit(limit)
        
        return list(session.exec(stmt).all())


def search_entries(user_id: int, query: str) -> List[Entry]:
    """Search entries by text content."""
    with Session(engine) as session:
        stmt = select(Entry).where(
            Entry.user_id == user_id,
            Entry.text.contains(query)
        ).order_by(Entry.created_at.desc())
        return list(session.exec(stmt).all())


def get_streak(user_id: int) -> int:
    """Calculate current streak of consecutive days with entries."""
    entries = get_entries(user_id=user_id, limit=365)
    if not entries:
        return 0
    
    # Get unique dates
    dates = set()
    for entry in entries:
        date = datetime.fromtimestamp(entry.created_at).date()
        dates.add(date)
    
    dates = sorted(dates, reverse=True)
    if not dates:
        return 0
    
    # Calculate streak
    streak = 0
    today = datetime.now().date()
    current_date = today
    
    for date in dates:
        if date == current_date or date == current_date - timedelta(days=1):
            if date == current_date:
                streak += 1
            elif date == current_date - timedelta(days=1):
                streak += 1
                current_date = date
        else:
            break
    
    return streak


def get_all_tags(user_id: int) -> List[str]:
    """Get all unique tags for a user."""
    entries = get_entries(user_id=user_id)
    tags = set()
    for entry in entries:
        if entry.tags:
            tags.update(entry.tags.split(","))
    return sorted([tag.strip() for tag in tags if tag.strip()])


def get_cohort_entries(cohort_id: int) -> List[Entry]:
    """Get entries for all users in a cohort (for teacher mode)."""
    with Session(engine) as session:
        members = session.exec(
            select(CohortMember).where(CohortMember.cohort_id == cohort_id)
        ).all()
        user_ids = [m.user_id for m in members]
        
        if not user_ids:
            return []
        
        stmt = select(Entry).where(Entry.user_id.in_(user_ids))
        return list(session.exec(stmt).all())

