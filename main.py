from fastapi import FastAPI
from zoomParser import ZoomURL, ZoomParser

app = FastAPI()


@app.get("/")
def read_root():
    return "Welcome"


@app.post("/urlParser")
def read_item(zoom_url: ZoomURL):
    zoom_parser = ZoomParser()
    response = zoom_parser.parse_url(zoom_url.link)
    return response
