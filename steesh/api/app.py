import os
import tempfile
from typing import Any

from flask import Flask, flash, redirect, render_template, request
from werkzeug.utils import secure_filename

from steesh.api.render_response import render_response

app = Flask(__name__, template_folder="../../web/templates/")
app.secret_key = os.urandom(12).hex()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ["csv", "xlsx"]


@app.route("/", methods=["GET", "POST"])
def index() -> Any:
    if request.method == "GET":
        return render_template("index.html")
    try:
        assert "library" in request.files and "deck" in request.form
        with tempfile.TemporaryDirectory() as td:
            file = request.files["library"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(td, filename))
                if "" in request.form["deck"].split("\r\n"):
                    raise ValueError("Deck contains empty lines")

                html = render_response(
                    library_path=os.path.join(td, filename),
                    deck=request.form["deck"].split("\r\n"),
                )
                return html
            flash(
                f"File type .{file.filename.rsplit('.', 1)[1].lower()} is not allowed"
            )
            return redirect(request.url)
    except AssertionError:
        return "Bad request", 400
    except Exception as e:
        app.logger.log(0, str(e))
        flash(str(e))
        return redirect(request.url)


if __name__ == "__main__":
    debug = bool(os.environ.get("STEESH_DBUG", False))
    app.run(host="0.0.0.0", debug=debug)
