"""Small in-memory conversation store for WeatherGPT.

The project currently has no authentication/session database. Conversation IDs
therefore provide lightweight per-browser-session context without changing the
existing database schema or migrations.
"""

from __future__ import annotations

from collections import defaultdict, deque
from threading import Lock
from typing import Any


class ConversationStore:
    def __init__(self, max_turns: int = 12) -> None:
        self.max_turns = max_turns
        self._conversations: dict[str, deque[dict[str, str]]] = defaultdict(
            lambda: deque(maxlen=self.max_turns)
        )
        self._lock = Lock()

    def get(self, conversation_id: str) -> list[dict[str, str]]:
        with self._lock:
            return list(self._conversations[conversation_id])

    def add(self, conversation_id: str, role: str, content: str) -> None:
        if role not in {"user", "assistant"} or not content.strip():
            return
        with self._lock:
            self._conversations[conversation_id].append(
                {"role": role, "content": content.strip()}
            )

    def clear(self, conversation_id: str) -> None:
        with self._lock:
            self._conversations.pop(conversation_id, None)


conversation_store = ConversationStore()
