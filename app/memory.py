from collections import deque

from langchain_community.chat_message_histories import (
    ChatMessageHistory,
)

MAX_MESSAGES = 10

history = ChatMessageHistory()

message_queue = deque(maxlen=MAX_MESSAGES)


def add_user_message(message):
    history.add_user_message(message)

    message_queue.append(
        history.messages[-1]
    )


def add_ai_message(message):
    history.add_ai_message(message)

    message_queue.append(
        history.messages[-1]
    )


def get_history():
    return list(message_queue)


def clear_history():
    history.clear()

    message_queue.clear()