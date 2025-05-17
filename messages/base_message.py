from typing import Literal


class BaseMessage:
    ROLE: Literal['user', 'assistant']

    def serialize(self) -> str:
        raise NotImplementedError("Not implemented on base class")

    @classmethod
    def deserialize(cls, encoded: str) -> "BaseMessage":
        raise NotImplementedError("Not implemented on base class")
