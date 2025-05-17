from typing import Optional
from openai import OpenAI
from messages import UserMessage, deserialize
from messages.base_message import BaseMessage

class Thread:
    _client: OpenAI
    _thread_id: str

    def __init__(self, client: OpenAI, thread_id: str):
        self._client = client
        self._thread_id = thread_id
    
    @property
    def id(self):
        return self._thread_id

    def validate_id(self):
        self._client.beta.threads.retrieve(self.id)

    def send_message(self, msg: BaseMessage, assistant_id: str) -> Optional[BaseMessage]:
        _ = self._client.beta.threads.messages.create(thread_id=self.id, role=msg.ROLE, content=msg.serialize())
        run = self._client.beta.threads.runs.create_and_poll(
                thread_id=self.id,
                assistant_id=assistant_id
                )

        if run.status != "completed":
            return None

        response_message = next(iter(self._client.beta.threads.messages.list(self.id)))

        try:
            return deserialize(response_message)
        except TypeError:
            self._client.beta.threads.messages.delete(response_message.id, thread_id=self.id)
            return None


    def messages(self):
        yield from (deserialize(x) for x in self._client.beta.threads.messages.list(self.id))


class ThreadFactory:
    def byId(self, client: OpenAI, id: str):
        t = Thread(client, id)
        t.validate_id()
        return t

    def new(self, client: OpenAI):
        thread = client.beta.threads.create()
        return Thread(client, thread.id)
