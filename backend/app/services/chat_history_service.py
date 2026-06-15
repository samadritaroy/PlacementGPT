"""
Chat History Service
Stores conversation history in memory (per session).
Later we'll move this to Supabase in Phase 4.
"""

from collections import defaultdict
from typing import List, Dict
import uuid
import time

# In-memory store: { session_id: [{"role": ..., "content": ..., "timestamp": ...}] }
_sessions: Dict[str, list] = defaultdict(list)
_session_metadata: Dict[str, dict] = {}


def create_session(session_type: str = "general", company: str = None) -> str:
    """Create a new chat session. Returns session_id."""
    session_id = str(uuid.uuid4())
    _session_metadata[session_id] = {
        "type": session_type,
        "company": company,
        "created_at": time.time()
    }
    return session_id


def add_message(session_id: str, role: str, content: str):
    """Add a message to a session. role = 'user' or 'assistant'."""
    _sessions[session_id].append({
        "role": role,
        "content": content,
        "timestamp": time.time()
    })


def get_history(session_id: str) -> List[dict]:
    """Get all messages in a session (without timestamps, just role+content)."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in _sessions.get(session_id, [])
    ]


def get_history_for_display(session_id: str) -> List[dict]:
    """Get messages with timestamps for frontend display."""
    return _sessions.get(session_id, [])


def clear_session(session_id: str):
    """Clear a session's history."""
    _sessions.pop(session_id, None)
    _session_metadata.pop(session_id, None)


def list_sessions() -> List[dict]:
    """List all active sessions."""
    return [
        {"session_id": sid, **meta}
        for sid, meta in _session_metadata.items()
    ]


def get_session_count() -> int:
    return len(_sessions)