import json

from messages.base_message import BaseMessage

class UserMessage(BaseMessage):
    ROLE="user"
    message: str

    def __init__(self, msg: str):
        self.message = msg

    def serialize(self):
        return '{ "userMessage": '+ json.dumps(self.message) +' }'

    @classmethod
    def deserialize(cls, encoded: str):
        o = json.loads(encoded)

        if type(o) is not dict or "userMessage" not in o:
            raise TypeError

        if type(o["userMessage"]) is not str:
            raise TypeError

        return cls(o["userMessage"])

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"UserMessage {str(self)}"
