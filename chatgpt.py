import os
from typing import Dict
from openai import OpenAI
from thread import ThreadFactory

class ChatGpt:
    _client: OpenAI
    _thread_provider: ThreadFactory

    _user_thread_map: Dict["str", "str"] = {}

    def __init__(self, thread_provider: ThreadFactory):
        if "OPENAI_API_KEY" not in os.environ:
            raise TypeError("OPEN_API_KEY env var not defined")

        self._thread_provider = thread_provider

        self._client = OpenAI()

    def get_thread_by_user(self, user_id: str): 
        if user_id in self._user_thread_map:
            return self._thread_provider.byId(self._client, self._user_thread_map[user_id])

        thread = self._thread_provider.new(self._client)
        self._user_thread_map[user_id] = thread.id
        return thread
