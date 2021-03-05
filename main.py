from fastapi import FastAPI, HTTPException
from zoomParser import ZoomURL, ZoomParser
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return "Welcome"


@app.post("/urlParser")
def read_item(zoom_url: ZoomURL):
    zoom_parser = ZoomParser()
    response, success = zoom_parser.parse_url(zoom_url.link)
    if not success:
        raise HTTPException(status_code=400, detail=response)
    return response
