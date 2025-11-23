from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from . import Item, ContentModerator, get_classifier


@asynccontextmanager
async def lifespan(_: FastAPI):
    get_classifier()
    yield


app = FastAPI(title="Content Moderator API", lifespan=lifespan)


def get_moderator():
    classifier = get_classifier()
    return ContentModerator(classifier)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(item: Item, moderator: ContentModerator = Depends(get_moderator)):
    try:
        return moderator.predict_text(item.text)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Model Error")
