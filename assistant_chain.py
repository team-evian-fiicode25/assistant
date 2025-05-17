from typing import Optional

from thread import Thread
from messages import BaseMessage


class AssistantNode:
    _assistant_id: str
    _next: Optional["AssistantNode"]

    def __init__(self, assistant_id: str):
        self._assistant_id = assistant_id
        self._next = None

    def chain(self, node: "AssistantNode") -> "AssistantNode":
        node._next = self
        return node

    def send_message(self, thread: Thread, msg: BaseMessage) -> BaseMessage | None:
        response = thread.send_message(msg, self._assistant_id)

        if response is not None:
            return response

        if  self._next is not None:
            return self._next.send_message(thread, msg)

        return None


def get_chain() -> AssistantNode:
    return AssistantNode("asst_e9pMjBUT6dxNOtyf0CsS3a7B") \
      .chain(AssistantNode("asst_JlyWuzmW6PwfchaZ9gPgC7re"))
