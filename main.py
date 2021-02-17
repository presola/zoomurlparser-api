from fastapi import FastAPI
from zoomParser import ZoomURL, ZoomParser
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:4200",
    "https://zoomurl-angular.herokuapp.com",
]

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
    response = zoom_parser.parse_url(zoom_url.link)
    return response
