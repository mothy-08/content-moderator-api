from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import Item, ContentModerator, get_classifier


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_classifier()
    yield


app = FastAPI(title="Content Moderator API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with the app's specific URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_moderator():
    return ContentModerator(get_classifier())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(item: Item, moderator: ContentModerator = Depends(get_moderator)):
    return moderator.predict_text(item.text)
