from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Generic, List, Optional, TypeVar

from .agent import AlphaSwarmAgent

T_Context = TypeVar("T_Context")


class Context(ABC, Generic[T_Context]):
    def __init__(self, context: T_Context, message: str, id: int = 1) -> None:
        self._context = context
        self._message = message
        self._id = id

    @property
    def context(self) -> T_Context:
        return self._context

    @property
    def message(self) -> str:
        return self._message

    def get_id(self) -> int:
        return self._id


@dataclass
class ChatMessage:
    """Represents a message in the chat history"""

    sender: str
    content: str
    timestamp: datetime
    is_command: bool = False

    @classmethod
    def create(cls, sender: str, content: str, is_command: bool = False) -> ChatMessage:
        """Helper method to create a chat message with current timestamp"""
        return cls(sender=sender, content=content, timestamp=datetime.now(), is_command=is_command)


class AlphaSwarmAgentClient(ABC, Generic[T_Context]):

    def __init__(self, agent: AlphaSwarmAgent, client_id: str):
        self._agent = agent
        self._agent_lock = asyncio.Lock()
        self._client_id = client_id
        self._lock: Optional[asyncio.Lock] = None

        # Message history buffer (client_id -> list of messages)
        self._message_buffer: Dict[int, List[ChatMessage]] = defaultdict(list)
        self.max_history = 50

    @property
    def id(self) -> str:
        """Unique identifier for the client"""
        return self._client_id

    @abstractmethod
    async def on_agent_response(self, ctx: Context[T_Context], message: ChatMessage) -> None:
        """Called when the agent successfully processes a message"""
        pass

    @abstractmethod
    async def on_agent_error(self, ctx: Context[T_Context], error: ChatMessage) -> None:
        """Called when an error occurs during message processing"""
        pass

    @abstractmethod
    async def on_start(self) -> None:
        """Called when the client start"""
        pass

    @abstractmethod
    async def on_stop(self) -> None:
        """Called when the client stop"""
        pass

    @abstractmethod
    async def get_message(self) -> Context[T_Context]:
        """Get a message from the user with context"""
        pass

    async def _process_message(self, context: Context[T_Context]) -> None:
        """Send a message with proper locking"""
        if self._lock is None:
            raise RuntimeError("Client not started")

        async with self._lock, self._agent_lock:
            channel_id = context.get_id()
            try:
                response = await self._agent.process_message(self._format_message(channel_id, context.message))
                response_text = response if response else "No response"

                # Add agent response to history
                agent_message = ChatMessage.create(sender="agent", content=response_text)
                self._message_buffer[channel_id].append(agent_message)

                # Trim history if needed
                if len(self._message_buffer[channel_id]) > self.max_history:
                    self._message_buffer[channel_id] = self._message_buffer[channel_id][-self.max_history :]

                await self.on_agent_response(context, agent_message)
            except Exception as e:
                error_msg = f"Error processing message: {str(e)}"
                error_message = ChatMessage.create(sender="agent", content=error_msg)
                self._message_buffer[channel_id].append(error_message)
                await self.on_agent_error(context, error_message)

    async def start(self):
        """Start the client with proper registration"""
        if self._lock:
            raise RuntimeError("Client already started")
        await self.on_start()
        self._lock = asyncio.Lock()
        try:
            while True:
                context = await self.get_message()
                if context.message.lower() == "quit":
                    await self.on_agent_response(context, ChatMessage.create(sender="agent", content="bye"))
                    break

                await self._process_message(context)  # Using default channel_id
                await asyncio.sleep(1)
        finally:
            await self.stop()

    async def stop(self):
        """Stop the client and cleanup"""
        if not self._lock:
            raise RuntimeError("Client not started")
        self._lock = None
        await self.on_stop()

    @property
    def is_running(self) -> bool:
        return self._lock is not None

    def _format_message(self, channel_id: int, message: str) -> str:
        """Format a message for display in the chat"""
        formatted_message = ""
        if self._message_buffer[channel_id]:
            formatted_message += "Previous Messages:\n"
            for msg in self._message_buffer[channel_id]:
                formatted_message += f"- {msg.sender}: {msg.content}\n"
            formatted_message += "\nLatest Message:\n"

        new_message = ChatMessage.create(sender="user", content=message)
        self._message_buffer[channel_id].append(new_message)

        formatted_message += message
        return formatted_message
