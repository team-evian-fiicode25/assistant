from typing import List

from openai.types.beta.threads import Message

from .chat_bot_reply import ChatBotReply
from .user_message import UserMessage
from .base_message import BaseMessage

MESSAGE_TYPES: List[type[BaseMessage]] = [ChatBotReply, UserMessage]

def deserialize(msg: Message):
    relevant_types = (m for m in MESSAGE_TYPES if m.ROLE == msg.role)

    for t in relevant_types:
        try:
            return t.deserialize(msg.content[0].text.value)
        except TypeError:
            continue


    raise TypeError("Found no match for given type")
