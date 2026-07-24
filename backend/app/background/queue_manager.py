"""
Queue Manager.
In-memory FIFO queue for participants waiting to be processed.
"""

import logging
from collections import deque

logger = logging.getLogger("eventflow.queue")

# ---------------------------------------------------------------------------
# Single FIFO queue — shared across watcher and worker
# ---------------------------------------------------------------------------
_queue: deque = deque()


def enqueue(participant_id: int) -> None:
    """Add a participant ID to the end of the queue."""
    _queue.append(participant_id)


def dequeue() -> int | None:
    """Remove and return the next participant ID, or None if empty."""
    if _queue:
        return _queue.popleft()
    return None


def size() -> int:
    """Return the current queue length."""
    return len(_queue)


def is_empty() -> bool:
    """Check if the queue is empty."""
    return len(_queue) == 0
