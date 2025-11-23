from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from . import Item, ContentModerator, get_classifier


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_classifier()
    yield


app = FastAPI(title="Content Moderator API", lifespan=lifespan)


def get_moderator():
    return ContentModerator(get_classifier())


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(item: Item, moderator: ContentModerator = Depends(get_moderator)):
    return moderator.predict_text(item.text)
