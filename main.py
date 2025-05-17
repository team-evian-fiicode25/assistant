#!/bin/env python3

from dotenv import load_dotenv

from assistant_chain import get_chain
from chatgpt import ChatGpt
from messages.chat_bot_reply import SettingsAdviceReply
from messages.user_message import UserMessage
from thread import ThreadFactory


def main():
    load_dotenv()

    gpt = ChatGpt(
                thread_provider=ThreadFactory()
            )
    thread = gpt.get_thread_by_user("balls")
    
    chain = get_chain()

    response = chain.send_message(thread, UserMessage("How drive efficiently?"))

    if isinstance(response, SettingsAdviceReply):
        print(response)
        print(response.path)
        print(*thread.messages(), sep="\n\n")
    else:
        print(response)
        print(":(")


if __name__ == "__main__":
    main()
