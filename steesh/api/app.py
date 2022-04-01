import os
import tempfile
from typing import Any

from flask import Flask, flash, redirect, request
from werkzeug.utils import secure_filename

from steesh.renderer.renderer import api_render_html

app = Flask(__name__, static_folder="../../web/static/")
app.secret_key = os.urandom(12).hex()


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ["csv", "xlsx"]


@app.route("/", methods=["GET", "POST"])
def hello_world() -> Any:
    if request.method == "GET":
        return app.send_static_file("index.html")
    try:
        with tempfile.TemporaryDirectory() as td:
            file = request.files["library"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(td, filename))
                html = api_render_html(
                    library_path=os.path.join(td, filename),
                    deck=request.form["deck"].split("\r\n"),
                )
                return html

    except Exception as e:
        app.logger.error(str(e))
        flash(str(e))
        return redirect(request.url)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
