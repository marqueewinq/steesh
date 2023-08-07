# type: ignore
import os.path
import tempfile

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from steesh.renderer import (
    TEMPLATE_TABLE_PATH,
    generate_pdf,
    read_deck,
    read_library,
    read_template,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "templates/index.html")
DEFAULT_LIBRARY_PATH = os.path.join(BASE_DIR, "assets/default_library.csv")
DEFAULT_CARD_TEMPLATE_PATH = os.path.join(
    BASE_DIR, "templates/default_card_template.html"
)

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
def api__index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/example/library", response_class=FileResponse)
def api__example__library(request: Request):
    return FileResponse(
        DEFAULT_LIBRARY_PATH,
        headers={"Content-Disposition": "attachment; filename=library.csv"},
    )


@app.get("/example/template", response_class=FileResponse)
def api__example__template(request: Request):
    return FileResponse(
        DEFAULT_CARD_TEMPLATE_PATH,
        headers={"Content-Disposition": "attachment; filename=template.html"},
    )


@app.post("/generate-pdf/")
async def api__generate_pdf(
    request: Request,
    library_file: UploadFile = File(...),
    deck: str = Form(...),
    template_file: UploadFile = File(None),
    name_column: str = Form("Name"),
    xlsx_sheet_index: int = Form(0),
):
    with tempfile.TemporaryDirectory() as tmpdir:
        _, ext = os.path.splitext(library_file.filename)
        library_path = os.path.join(tmpdir, "library." + ext)
        with open(library_path, "wb") as fd:
            fd.write(await library_file.read())

        template_path = DEFAULT_CARD_TEMPLATE_PATH
        if template_file is not None:
            template_path = os.path.join(tmpdir, "template.html")
            with open(template_path, "wb") as fd:
                fd.write(await template_file.read())

        deck = deck.replace("\\n", "\n")
        deck_path = os.path.join(tmpdir, "deck.txt")
        with open(deck_path, "w") as fd:
            fd.write(deck)

        try:
            library = read_library(
                library_path,
                name_column=name_column,
                xlsx_sheet_index=xlsx_sheet_index,
            )
            deck = read_deck(deck_path)
            template = read_template(template_path)
            page_template = read_template(TEMPLATE_TABLE_PATH)
        except Exception as e:
            return templates.TemplateResponse(
                "index.html", {"request": request, "messages": [str(e)]}
            )

    output_path = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name
    try:
        generate_pdf(
            library=library,
            deck=deck,
            card_template=template,
            page_template=page_template,
            output_path=output_path,
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", {"request": request, "messages": [str(e)]}
        )

    return FileResponse(
        output_path,
        headers={"Content-Disposition": "attachment; filename=output.pdf"},
    )
