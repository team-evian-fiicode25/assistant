from dotenv import load_dotenv
from flask import Flask, abort, request
import flask

from assistant_chain import get_chain
from chatgpt import ChatGpt
from messages.user_message import UserMessage
from thread import ThreadFactory

app = Flask(__name__)


@app.route("/send_message", methods=["POST"])
def send_message() -> flask.Response:
    body = request.get_json()


    if "userId" not in body or \
        "message" not in body:
            abort(400)

    user_id = body["userId"]
    message = body["message"]

    if type(user_id) is not str or \
        type(message) is not str:
            abort(400)

    gpt = ChatGpt(
                thread_provider=ThreadFactory()
            )

    thread = gpt.get_thread_by_user(user_id)
    
    chain = get_chain()

    response = chain.send_message(thread, UserMessage(message))

    if response is not None:
        print(response.serialize())
        res = flask.Response(response.serialize(), status=200, mimetype="application/json")


        return res

    abort(418)


@app.route("/messages")
def messages() -> flask.Response:
    body = request.get_json()

    if "userId" not in body:
            abort(400)

    user_id = body["userId"]

    if type(user_id) is not str:
            abort(400)

    gpt = ChatGpt(
                thread_provider=ThreadFactory()
            )

    thread = gpt.get_thread_by_user(user_id)
    
    return flask.Response(f'[{",".join([m.serialize() for m in thread.messages()])}]',
                          mimetype="application/json",
                          status=200)


if __name__ == "__main__":
    load_dotenv()

    app.run(port=8000)
