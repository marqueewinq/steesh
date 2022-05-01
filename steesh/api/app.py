import os
import tempfile
from typing import Any

from flask import Flask, flash, redirect, render_template, request
from werkzeug.utils import secure_filename

from steesh.api.utils import allowed_file, format_deck, render_response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates/"),
)
app.secret_key = os.environ.get("STEESH_SECRET_KEY", os.urandom(12).hex())


@app.route("/", methods=["GET", "POST"])
def index() -> Any:
    if request.method == "GET":
        return render_template("index.html")

    if "library" not in request.files or "deck" not in request.form:
        return "Bad request", 400

    file = request.files["library"]
    if not (file and allowed_file(file.filename)):
        flash(
            f"File type .{str(file.filename).rsplit('.', 1)[1].lower()} is not allowed"
        )
        return redirect(request.url)

    with tempfile.TemporaryDirectory() as td:
        filename = secure_filename(str(file.filename))
        file.save(os.path.join(td, filename))

        try:
            html = render_response(
                library_path=os.path.join(td, filename),
                deck=format_deck(request.form["deck"]),
            )
        except ValueError as e:
            flash(f"Error while rendering: {e}")
            return redirect(request.url)
        return render_template("p2p.html", rendered_html=html)


if __name__ == "__main__":
    debug = bool(os.environ.get("STEESH_DEBUG", False))
    app.run(host="0.0.0.0", debug=debug)
