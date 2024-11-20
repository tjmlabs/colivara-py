from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field, model_validator
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
    num_documents: int


class GenericError(BaseModel):
    detail: str


class GenericMessage(BaseModel):
    detail: str


class WebhookOut(BaseModel):
    app_id: str
    endpoint_id: str
    webhook_secret: str


class DocumentIn(BaseModel):
    name: str
    metadata: dict = Field(default_factory=dict)
    collection_name: str = Field(
        "default_collection",
        description="""The name of the collection to which the document belongs. If not provided, the document will be added to the default_collection. Use 'all' to access all collections belonging to the user.""",
    )
    url: Optional[str] = None
    base64: Optional[str] = None
    wait: Optional[bool] = False

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
    num_pages: int
    collection_name: str
    pages: Optional[List[PageOut]] = None


class DocumentInPatch(BaseModel):
    name: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    collection_name: Optional[str] = Field(
        "default_collection",
        description="""The name of the collection to which the document belongs. If not provided, the document will be added to the default_collection. Use 'all' to access all collections belonging to the user.""",
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


class QueryFilter(BaseModel):
    class onEnum(str, Enum):
        document = "document"
        collection = "collection"

    class lookupEnum(str, Enum):
        key_lookup = "key_lookup"
        contains = "contains"
        contained_by = "contained_by"
        has_key = "has_key"
        has_keys = "has_keys"
        has_any_keys = "has_any_keys"

    on: onEnum = onEnum.document
    # key is a str or a list of str
    key: Union[str, List[str]]
    # value can be any - we can accept int, float, str, bool
    value: Optional[Union[str, int, float, bool]] = None
    lookup: lookupEnum = lookupEnum.key_lookup

    # validation rules:
    # 1. if looks up is contains or contained_by, value must be a string, and key must be a string
    # 2. if lookup is has_keys, or has_any_keys, key must be a list of strings - we can transform automatically - value must be None
    # 3. if lookup is has_key, key must be a string, value must be None
    @model_validator(mode="after")
    def validate_filter(self) -> Self:
        if self.lookup in ["contains", "contained_by", "key_lookup"]:
            if not isinstance(self.key, str):
                raise ValueError("Key must be a string.")
            if self.value is None:
                raise ValueError("Value must be provided.")
        if self.lookup in ["has_key"]:
            if not isinstance(self.key, str):
                raise ValueError("Key must be a string.")
            if self.value is not None:
                raise ValueError("Value must be None.")
        if self.lookup in ["has_keys", "has_any_keys"]:
            if not isinstance(self.key, list):
                raise ValueError("Key must be a list of strings.")
            if self.value is not None:
                raise ValueError("Value must be None.")
        return self


class QueryIn(BaseModel):
    query: str
    collection_name: Optional[str] = "all"
    top_k: Optional[int] = 3
    query_filter: Optional[QueryFilter] = None


class PageOutQuery(BaseModel):
    collection_name: str
    collection_id: int
    collection_metadata: Optional[dict] = {}
    document_name: str
    document_id: int
    document_metadata: Optional[dict] = {}
    page_number: int
    raw_score: float
    normalized_score: float
    img_base64: str


class QueryOut(BaseModel):
    query: str
    results: List[PageOutQuery]


class FileOut(BaseModel):
    img_base64: str
    page_number: int


class TaskEnum(str, Enum):
    image = "image"
    query = "query"


class EmbeddingsIn(BaseModel):
    input_data: List[str]
    task: TaskEnum


class EmbeddingsOut(BaseModel):
    _object: str
    data: List[dict]
    model: str
    usage: dict
