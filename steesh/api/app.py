from typing import Any

from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world() -> Any:
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
