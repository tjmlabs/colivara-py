from typing import Optional, List
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


class DocumentIn(BaseModel):
    name: str
    metadata: dict = Field(default_factory=dict)
    collection_name: str = Field(
        "default collection",
        description="""The name of the collection to which the document belongs. If not provided, the document will be added to the default collection. Use 'all' to access all collections belonging to the user.""",
    )
    url: Optional[str] = None
    base64: Optional[str] = None

    @model_validator(mode="after")
    def base64_or_url(self) -> Self:
        if not self.url and not self.base64:
            raise ValueError("Either 'url' or 'base64' must be provided.")
        if self.url and self.base64:
            raise ValueError("Only one of 'url' or 'base64' should be provided.")
        return self


class PageOut(BaseModel):
    document_name: Optional[str] = None
    img_base64: str
    page_number: int


class DocumentOut(BaseModel):
    id: int
    name: str
    metadata: dict = Field(default_factory=dict)
    url: Optional[str] = None
    base64: Optional[str] = None
    num_pages: int
    collection_name: str
    pages: Optional[List[PageOut]] = None


class DocumentInPatch(BaseModel):
    name: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    collection_name: Optional[str] = Field(
        "default collection",
        description="""The name of the collection to which the document belongs. If not provided, the document will be added to the default collection. Use 'all' to access all collections belonging to the user.""",
    )
    url: Optional[str] = None
    base64: Optional[str] = None

    @model_validator(mode="after")
    def at_least_one_field(self) -> Self:
        if not any([self.name, self.metadata, self.url, self.base64]):
            raise ValueError("At least one field must be provided to update.")
        if self.url and self.base64:
            raise ValueError("Only one of 'url' or 'base64' should be provided.")
        return self
