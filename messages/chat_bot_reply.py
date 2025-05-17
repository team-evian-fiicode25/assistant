import json

from messages.base_message import BaseMessage

class ChatBotReply(BaseMessage):
    ROLE="assistant"
    message: str

    def __init__(self, msg: str):
        self.message = msg

    def serialize(self):
        return '{ "chatBotReply": { "text": '+ json.dumps(self.message) +'} }'

    @classmethod
    def deserialize(cls, encoded: str):
        o = json.loads(encoded)

        if type(o) is not dict or "chatBotReply" not in o:
            raise TypeError

        o = o["chatBotReply"]
        if type(o) is not dict or "text" not in o:
            raise TypeError

        return ChatBotReply(o["text"])

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"ChatBotReply {str(self)}"


class SettingsAdviceReply(ChatBotReply):
    path: str

    def __init__(self, msg: str, path: str):
        super().__init__(msg)
        self.path = path

    def serialize(self): 
        return '{ "chatBotReply": { "text": ' \
                + json.dumps(self.message) \
                + ', "settingsResponse": {"path": ' \
                + json.dumps(self.path) \
                + '}} }'

    @classmethod
    def deserialize(cls, encoded: str):
        obj = super().deserialize(encoded)

        try:
            return cls(obj.message, json.loads(encoded)["chatBotReply"]["settingsResponse"]["path"])
        except KeyError:
            raise TypeError
