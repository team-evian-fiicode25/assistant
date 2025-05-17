#!/bin/env python3

from dotenv import load_dotenv

from assistant_chain import get_chain
from chatgpt import ChatGpt
from messages.user_message import UserMessage
from thread import ThreadFactory


def main():
    load_dotenv()

    gpt = ChatGpt(
                thread_provider=ThreadFactory()
            )
    thread = gpt.get_thread_by_user("balls")
    
    chain = get_chain()

    response = chain.send_message(thread, UserMessage(""))

    print(response)


if __name__ == "__main__":
    main()
