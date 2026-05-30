"""Data models for the serverless assistant.

Task 1.1: Create data models (ChatMessage, ChatResponse, ConversationHistory)
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal


@dataclass
class ChatMessage:
    """A single message in a conversation."""

    role: Literal["user", "assistant"]
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict:
        """Convert to dictionary for DynamoDB storage."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        """Create a ChatMessage from a DynamoDB item."""
        return cls(
            role=data["role"],
            content=data["content"],
            timestamp=data["timestamp"],
        )


@dataclass
class ChatResponse:
    """Response returned by the chat endpoint."""

    response: str
    session_id: str
    timestamp: str

    def to_dict(self) -> dict:
        """Convert to API response dictionary."""
        return {
            "response": self.response,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
        }


@dataclass
class ConversationHistory:
    """Collection of messages for a session."""

    session_id: str
    messages: list[ChatMessage] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to API response dictionary."""
        return {
            "session_id": self.session_id,
            "messages": [msg.to_dict() for msg in self.messages],
        }
