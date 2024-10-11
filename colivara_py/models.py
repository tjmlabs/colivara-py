
from typing import Optional
from pydantic import BaseModel, model_validator, Field
from typing_extensions import Self

class CollectionIn(BaseModel):
    name: str
    metadata: Optional[dict] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_name(self) -> Self:
        if self.name.lower() == "all":
            raise ValueError("Collection name 'all' is not allowed.")
        return self

class PatchCollectionIn(BaseModel):
    name: Optional[str] = None
    # metadata can be Not provided = keep the old metadata
    # emtpy dict = override the metadata with an empty dict
    # dict = update the metadata with the provided dict
    metadata: Optional[dict] = None

    @model_validator(mode="after")
    def validate_name(self) -> Self:
        if self.name and self.name.lower() == "all":
            raise ValueError("Collection name 'all' is not allowed.")
        if not any([self.name, self.metadata]):
            raise ValueError("At least one field must be provided to update.")
        return self



class CollectionOut(BaseModel):
    id: int
    name: str
    metadata: dict


class GenericError(BaseModel):
    detail: str
