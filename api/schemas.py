from typing_extensions import Annotated
from pydantic import BaseModel, StringConstraints


class Item(BaseModel):
    text: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True, strict=True, min_length=1, max_length=2500
        ),
    ]
