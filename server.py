from flask import Flask, request
import requests
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/flow", methods=["GET"])
def do_get():
    return "hello world"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
