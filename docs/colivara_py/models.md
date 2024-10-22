# Module colivara_py.models

??? example "View Source"
        from typing import Optional, List, Union

        from pydantic import BaseModel, model_validator, Field

        from typing_extensions import Self

        from enum import Enum

        

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

## Classes

### CollectionIn

```python3
class CollectionIn(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class CollectionIn(BaseModel):

            name: str

            metadata: Optional[dict] = Field(default_factory=dict)

            @model_validator(mode="after")

            def validate_name(self) -> Self:

                if self.name.lower() == "all":

                    raise ValueError("Collection name 'all' is not allowed.")

                return self

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

    
#### validate_name

```python3
def validate_name(
    self
) -> Self
```

??? example "View Source"
            @model_validator(mode="after")

            def validate_name(self) -> Self:

                if self.name.lower() == "all":

                    raise ValueError("Collection name 'all' is not allowed.")

                return self

### CollectionOut

```python3
class CollectionOut(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class CollectionOut(BaseModel):

            id: int

            name: str

            metadata: dict

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### DocumentIn

```python3
class DocumentIn(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
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

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### base64_or_url

```python3
def base64_or_url(
    self
) -> Self
```

??? example "View Source"
            @model_validator(mode="after")

            def base64_or_url(self) -> Self:

                if not self.url and not self.base64:

                    raise ValueError("Either 'url' or 'base64' must be provided.")

                if self.url and self.base64:

                    raise ValueError("Only one of 'url' or 'base64' should be provided.")

                return self

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### DocumentInPatch

```python3
class DocumentInPatch(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
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

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### at_least_one_field

```python3
def at_least_one_field(
    self
) -> Self
```

??? example "View Source"
            @model_validator(mode="after")

            def at_least_one_field(self) -> Self:

                if not any([self.name, self.metadata, self.url, self.base64]):

                    raise ValueError("At least one field must be provided to update.")

                if self.url and self.base64:

                    raise ValueError("Only one of 'url' or 'base64' should be provided.")

                return self

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### DocumentOut

```python3
class DocumentOut(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class DocumentOut(BaseModel):

            id: int

            name: str

            metadata: dict = Field(default_factory=dict)

            url: Optional[str] = None

            base64: Optional[str] = None

            num_pages: int

            collection_name: str

            pages: Optional[List[PageOut]] = None

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### EmbeddingsIn

```python3
class EmbeddingsIn(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class EmbeddingsIn(BaseModel):

            input_data: List[str]

            task: TaskEnum

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### EmbeddingsOut

```python3
class EmbeddingsOut(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class EmbeddingsOut(BaseModel):

            _object: str

            data: List[dict]

            model: str

            usage: dict

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self: 'BaseModel',
    context: 'Any',
    /
) -> 'None'
```

This function is meant to behave like a BaseModel method to initialise private attributes.

It takes context as an argument since that's what pydantic-core passes when calling it.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| self | None | The BaseModel instance. | None |
| context | None | The context. | None |

??? example "View Source"
        def init_private_attributes(self: BaseModel, context: Any, /) -> None:

            """This function is meant to behave like a BaseModel method to initialise private attributes.

            It takes context as an argument since that's what pydantic-core passes when calling it.

            Args:

                self: The BaseModel instance.

                context: The context.

            """

            if getattr(self, '__pydantic_private__', None) is None:

                pydantic_private = {}

                for name, private_attr in self.__private_attributes__.items():

                    default = private_attr.get_default()

                    if default is not PydanticUndefined:

                        pydantic_private[name] = default

                object_setattr(self, '__pydantic_private__', pydantic_private)

### FileOut

```python3
class FileOut(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class FileOut(BaseModel):

            img_base64: str

            page_number: int

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### GenericError

```python3
class GenericError(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class GenericError(BaseModel):

            detail: str

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### PageOut

```python3
class PageOut(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class PageOut(BaseModel):

            document_name: Optional[str] = None

            img_base64: str

            page_number: int

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### PageOutQuery

```python3
class PageOutQuery(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
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

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### PatchCollectionIn

```python3
class PatchCollectionIn(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
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

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

    
#### validate_name

```python3
def validate_name(
    self
) -> Self
```

??? example "View Source"
            @model_validator(mode="after")

            def validate_name(self) -> Self:

                if self.name and self.name.lower() == "all":

                    raise ValueError("Collection name 'all' is not allowed.")

                if not any([self.name, self.metadata]):

                    raise ValueError("At least one field must be provided to update.")

                return self

### QueryFilter

```python3
class QueryFilter(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
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

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
lookupEnum
```

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

```python3
onEnum
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

    
#### validate_filter

```python3
def validate_filter(
    self
) -> Self
```

??? example "View Source"
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

### QueryIn

```python3
class QueryIn(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class QueryIn(BaseModel):

            query: str

            collection_name: Optional[str] = "all"

            top_k: Optional[int] = 3

            query_filter: Optional[QueryFilter] = None

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### QueryOut

```python3
class QueryOut(
    /,
    **data: 'Any'
)
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/models/

A base class for creating Pydantic models.
#### Attributes

| Name | Type | Description | Default |
|---|---|---|---|
| __class_vars__ | None | The names of the class variables defined on the model. | None |
| __private_attributes__ | None | Metadata about the private attributes of the model. | None |
| __signature__ | None | The synthesized `__init__` [`Signature`][inspect.Signature] of the model. | None |
| __pydantic_complete__ | None | Whether model building is completed, or if there are still undefined fields. | None |
| __pydantic_core_schema__ | None | The core schema of the model. | None |
| __pydantic_custom_init__ | None | Whether the model has a custom `__init__` function. | None |
| __pydantic_decorators__ | None | Metadata containing the decorators defined on the model.<br>This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1. | None |
| __pydantic_generic_metadata__ | None | Metadata for generic models; contains data used for a similar purpose to<br>__args__, __origin__, __parameters__ in typing-module generics. May eventually be replaced by these. | None |
| __pydantic_parent_namespace__ | None | Parent namespace of the model, used for automatic rebuilding of models. | None |
| __pydantic_post_init__ | None | The name of the post-init method for the model, if defined. | None |
| __pydantic_root_model__ | None | Whether the model is a [`RootModel`][pydantic.root_model.RootModel]. | None |
| __pydantic_serializer__ | None | The `pydantic-core` `SchemaSerializer` used to dump instances of the model. | None |
| __pydantic_validator__ | None | The `pydantic-core` `SchemaValidator` used to validate instances of the model. | None |
| __pydantic_extra__ | None | A dictionary containing extra values, if [`extra`][pydantic.config.ConfigDict.extra]<br>is set to `'allow'`. | None |
| __pydantic_fields_set__ | None | The names of fields explicitly set during instantiation. | None |
| __pydantic_private__ | None | Values of private attributes set on the model instance. | None |

??? example "View Source"
        class QueryOut(BaseModel):

            query: str

            results: List[PageOutQuery]

------

#### Ancestors (in MRO)

* pydantic.main.BaseModel

#### Class variables

```python3
model_computed_fields
```

```python3
model_config
```

```python3
model_fields
```

#### Static methods

    
#### construct

```python3
def construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `construct` method is deprecated; use `model_construct` instead.', category=None)

            def construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `construct` method is deprecated; use `model_construct` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_construct(_fields_set=_fields_set, **values)

    
#### from_orm

```python3
def from_orm(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `from_orm` method is deprecated; set '

                "`model_config['from_attributes']=True` and use `model_validate` instead.",

                category=None,

            )

            def from_orm(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `from_orm` method is deprecated; set '

                    "`model_config['from_attributes']=True` and use `model_validate` instead.",

                    category=PydanticDeprecatedSince20,

                )

                if not cls.model_config.get('from_attributes', None):

                    raise PydanticUserError(

                        'You must set the config attribute `from_attributes=True` to use from_orm', code=None

                    )

                return cls.model_validate(obj)

    
#### model_construct

```python3
def model_construct(
    _fields_set: 'set[str] | None' = None,
    **values: 'Any'
) -> 'Self'
```

Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.
Default values are respected, but no other validation is performed.

!!! note
    `model_construct()` generally respects the `model_config.extra` setting on the provided model.
    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`
    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.
    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in
    an error if extra values are passed, but they will be ignored.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| _fields_set | None | A set of field names that were originally explicitly set during instantiation. If provided,<br>this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.<br>Otherwise, the field names from the `values` argument will be used. | None |
| values | None | Trusted or pre-validated data dictionary. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A new instance of the `Model` class with validated data. |

??? example "View Source"
            @classmethod

            def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self:  # noqa: C901

                """Creates a new instance of the `Model` class with validated data.

                Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data.

                Default values are respected, but no other validation is performed.

                !!! note

                    `model_construct()` generally respects the `model_config.extra` setting on the provided model.

                    That is, if `model_config.extra == 'allow'`, then all extra passed values are added to the model instance's `__dict__`

                    and `__pydantic_extra__` fields. If `model_config.extra == 'ignore'` (the default), then all extra passed values are ignored.

                    Because no validation is performed with a call to `model_construct()`, having `model_config.extra == 'forbid'` does not result in

                    an error if extra values are passed, but they will be ignored.

                Args:

                    _fields_set: A set of field names that were originally explicitly set during instantiation. If provided,

                        this is directly used for the [`model_fields_set`][pydantic.BaseModel.model_fields_set] attribute.

                        Otherwise, the field names from the `values` argument will be used.

                    values: Trusted or pre-validated data dictionary.

                Returns:

                    A new instance of the `Model` class with validated data.

                """

                m = cls.__new__(cls)

                fields_values: dict[str, Any] = {}

                fields_set = set()

                for name, field in cls.model_fields.items():

                    if field.alias is not None and field.alias in values:

                        fields_values[name] = values.pop(field.alias)

                        fields_set.add(name)

                    if (name not in fields_set) and (field.validation_alias is not None):

                        validation_aliases: list[str | AliasPath] = (

                            field.validation_alias.choices

                            if isinstance(field.validation_alias, AliasChoices)

                            else [field.validation_alias]

                        )

                        for alias in validation_aliases:

                            if isinstance(alias, str) and alias in values:

                                fields_values[name] = values.pop(alias)

                                fields_set.add(name)

                                break

                            elif isinstance(alias, AliasPath):

                                value = alias.search_dict_for_path(values)

                                if value is not PydanticUndefined:

                                    fields_values[name] = value

                                    fields_set.add(name)

                                    break

                    if name not in fields_set:

                        if name in values:

                            fields_values[name] = values.pop(name)

                            fields_set.add(name)

                        elif not field.is_required():

                            fields_values[name] = field.get_default(call_default_factory=True)

                if _fields_set is None:

                    _fields_set = fields_set

                _extra: dict[str, Any] | None = values if cls.model_config.get('extra') == 'allow' else None

                _object_setattr(m, '__dict__', fields_values)

                _object_setattr(m, '__pydantic_fields_set__', _fields_set)

                if not cls.__pydantic_root_model__:

                    _object_setattr(m, '__pydantic_extra__', _extra)

                if cls.__pydantic_post_init__:

                    m.model_post_init(None)

                    # update private attributes with values set

                    if hasattr(m, '__pydantic_private__') and m.__pydantic_private__ is not None:

                        for k, v in values.items():

                            if k in m.__private_attributes__:

                                m.__pydantic_private__[k] = v

                elif not cls.__pydantic_root_model__:

                    # Note: if there are any private attributes, cls.__pydantic_post_init__ would exist

                    # Since it doesn't, that means that `__pydantic_private__` should be set to None

                    _object_setattr(m, '__pydantic_private__', None)

                return m

    
#### model_json_schema

```python3
def model_json_schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    schema_generator: 'type[GenerateJsonSchema]' = <class 'pydantic.json_schema.GenerateJsonSchema'>,
    mode: 'JsonSchemaMode' = 'validation'
) -> 'dict[str, Any]'
```

Generates a JSON schema for a model class.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| by_alias | None | Whether to use attribute aliases or not. | None |
| ref_template | None | The reference template. | None |
| schema_generator | None | To override the logic used to generate the JSON schema, as a subclass of<br>`GenerateJsonSchema` with your desired modifications | None |
| mode | None | The mode in which to generate the schema. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The JSON schema for the given model class. |

??? example "View Source"
            @classmethod

            def model_json_schema(

                cls,

                by_alias: bool = True,

                ref_template: str = DEFAULT_REF_TEMPLATE,

                schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,

                mode: JsonSchemaMode = 'validation',

            ) -> dict[str, Any]:

                """Generates a JSON schema for a model class.

                Args:

                    by_alias: Whether to use attribute aliases or not.

                    ref_template: The reference template.

                    schema_generator: To override the logic used to generate the JSON schema, as a subclass of

                        `GenerateJsonSchema` with your desired modifications

                    mode: The mode in which to generate the schema.

                Returns:

                    The JSON schema for the given model class.

                """

                return model_json_schema(

                    cls, by_alias=by_alias, ref_template=ref_template, schema_generator=schema_generator, mode=mode

                )

    
#### model_parametrized_name

```python3
def model_parametrized_name(
    params: 'tuple[type[Any], ...]'
) -> 'str'
```

Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| params | None | Tuple of types of the class. Given a generic class<br>`Model` with 2 type variables and a concrete model `Model[str, int]`,<br>the value `(str, int)` would be passed to `params`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | String representing the new class where `params` are passed to `cls` as type variables. |

**Raises:**

| Type | Description |
|---|---|
| TypeError | Raised when trying to generate concrete names for non-generic models. |

??? example "View Source"
            @classmethod

            def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str:

                """Compute the class name for parametrizations of generic classes.

                This method can be overridden to achieve a custom naming scheme for generic BaseModels.

                Args:

                    params: Tuple of types of the class. Given a generic class

                        `Model` with 2 type variables and a concrete model `Model[str, int]`,

                        the value `(str, int)` would be passed to `params`.

                Returns:

                    String representing the new class where `params` are passed to `cls` as type variables.

                Raises:

                    TypeError: Raised when trying to generate concrete names for non-generic models.

                """

                if not issubclass(cls, typing.Generic):

                    raise TypeError('Concrete names should only be generated for generic models.')

                # Any strings received should represent forward references, so we handle them specially below.

                # If we eventually move toward wrapping them in a ForwardRef in __class_getitem__ in the future,

                # we may be able to remove this special case.

                param_names = [param if isinstance(param, str) else _repr.display_as_type(param) for param in params]

                params_component = ', '.join(param_names)

                return f'{cls.__name__}[{params_component}]'

    
#### model_rebuild

```python3
def model_rebuild(
    *,
    force: 'bool' = False,
    raise_errors: 'bool' = True,
    _parent_namespace_depth: 'int' = 2,
    _types_namespace: 'dict[str, Any] | None' = None
) -> 'bool | None'
```

Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during
the initial attempt to build the schema, and automatic rebuilding fails.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| force | None | Whether to force the rebuilding of the model schema, defaults to `False`. | None |
| raise_errors | None | Whether to raise errors, defaults to `True`. | None |
| _parent_namespace_depth | None | The depth level of the parent namespace, defaults to 2. | None |
| _types_namespace | None | The types namespace, defaults to `None`. | None |

**Returns:**

| Type | Description |
|---|---|
| None | Returns `None` if the schema is already "complete" and rebuilding was not required.<br>If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`. |

??? example "View Source"
            @classmethod

            def model_rebuild(

                cls,

                *,

                force: bool = False,

                raise_errors: bool = True,

                _parent_namespace_depth: int = 2,

                _types_namespace: dict[str, Any] | None = None,

            ) -> bool | None:

                """Try to rebuild the pydantic-core schema for the model.

                This may be necessary when one of the annotations is a ForwardRef which could not be resolved during

                the initial attempt to build the schema, and automatic rebuilding fails.

                Args:

                    force: Whether to force the rebuilding of the model schema, defaults to `False`.

                    raise_errors: Whether to raise errors, defaults to `True`.

                    _parent_namespace_depth: The depth level of the parent namespace, defaults to 2.

                    _types_namespace: The types namespace, defaults to `None`.

                Returns:

                    Returns `None` if the schema is already "complete" and rebuilding was not required.

                    If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

                """

                if not force and cls.__pydantic_complete__:

                    return None

                else:

                    if '__pydantic_core_schema__' in cls.__dict__:

                        delattr(cls, '__pydantic_core_schema__')  # delete cached value to ensure full rebuild happens

                    if _types_namespace is not None:

                        types_namespace: dict[str, Any] | None = _types_namespace.copy()

                    else:

                        if _parent_namespace_depth > 0:

                            frame_parent_ns = (

                                _typing_extra.parent_frame_namespace(parent_depth=_parent_namespace_depth, force=True) or {}

                            )

                            cls_parent_ns = (

                                _model_construction.unpack_lenient_weakvaluedict(cls.__pydantic_parent_namespace__) or {}

                            )

                            types_namespace = {**cls_parent_ns, **frame_parent_ns}

                            cls.__pydantic_parent_namespace__ = _model_construction.build_lenient_weakvaluedict(types_namespace)

                        else:

                            types_namespace = _model_construction.unpack_lenient_weakvaluedict(

                                cls.__pydantic_parent_namespace__

                            )

                        types_namespace = _typing_extra.merge_cls_and_parent_ns(cls, types_namespace)

                    # manually override defer_build so complete_model_class doesn't skip building the model again

                    config = {**cls.model_config, 'defer_build': False}

                    return _model_construction.complete_model_class(

                        cls,

                        cls.__name__,

                        _config.ConfigWrapper(config, check=False),

                        raise_errors=raise_errors,

                        types_namespace=types_namespace,

                    )

    
#### model_validate

```python3
def model_validate(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    from_attributes: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate a pydantic model instance.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| from_attributes | None | Whether to extract data from object attributes. | None |
| context | None | Additional context to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated model instance. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                from_attributes: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate a pydantic model instance.

                Args:

                    obj: The object to validate.

                    strict: Whether to enforce types strictly.

                    from_attributes: Whether to extract data from object attributes.

                    context: Additional context to pass to the validator.

                Raises:

                    ValidationError: If the object could not be validated.

                Returns:

                    The validated model instance.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_python(

                    obj, strict=strict, from_attributes=from_attributes, context=context

                )

    
#### model_validate_json

```python3
def model_validate_json(
    json_data: 'str | bytes | bytearray',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

Validate the given JSON data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| json_data | None | The JSON data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

**Raises:**

| Type | Description |
|---|---|
| ValidationError | If `json_data` is not a JSON string or the object could not be validated. |

??? example "View Source"
            @classmethod

            def model_validate_json(

                cls,

                json_data: str | bytes | bytearray,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/json/#json-parsing

                Validate the given JSON data against the Pydantic model.

                Args:

                    json_data: The JSON data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                Raises:

                    ValidationError: If `json_data` is not a JSON string or the object could not be validated.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_json(json_data, strict=strict, context=context)

    
#### model_validate_strings

```python3
def model_validate_strings(
    obj: 'Any',
    *,
    strict: 'bool | None' = None,
    context: 'Any | None' = None
) -> 'Self'
```

Validate the given object with string data against the Pydantic model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| obj | None | The object containing string data to validate. | None |
| strict | None | Whether to enforce types strictly. | None |
| context | None | Extra variables to pass to the validator. | None |

**Returns:**

| Type | Description |
|---|---|
| None | The validated Pydantic model. |

??? example "View Source"
            @classmethod

            def model_validate_strings(

                cls,

                obj: Any,

                *,

                strict: bool | None = None,

                context: Any | None = None,

            ) -> Self:

                """Validate the given object with string data against the Pydantic model.

                Args:

                    obj: The object containing string data to validate.

                    strict: Whether to enforce types strictly.

                    context: Extra variables to pass to the validator.

                Returns:

                    The validated Pydantic model.

                """

                # `__tracebackhide__` tells pytest and some other tools to omit this function from tracebacks

                __tracebackhide__ = True

                return cls.__pydantic_validator__.validate_strings(obj, strict=strict, context=context)

    
#### parse_file

```python3
def parse_file(
    path: 'str | Path',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                'use `model_validate_json`, otherwise `model_validate` instead.',

                category=None,

            )

            def parse_file(  # noqa: D102

                cls,

                path: str | Path,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:

                warnings.warn(

                    'The `parse_file` method is deprecated; load the data from file, then if your data is JSON '

                    'use `model_validate_json`, otherwise `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                obj = parse.load_file(

                    path,

                    proto=proto,

                    content_type=content_type,

                    encoding=encoding,

                    allow_pickle=allow_pickle,

                )

                return cls.parse_obj(obj)

    
#### parse_obj

```python3
def parse_obj(
    obj: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `parse_obj` method is deprecated; use `model_validate` instead.', category=None)

            def parse_obj(cls, obj: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `parse_obj` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(obj)

    
#### parse_raw

```python3
def parse_raw(
    b: 'str | bytes',
    *,
    content_type: 'str | None' = None,
    encoding: 'str' = 'utf8',
    proto: 'DeprecatedParseProtocol | None' = None,
    allow_pickle: 'bool' = False
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                'otherwise load the data then use `model_validate` instead.',

                category=None,

            )

            def parse_raw(  # noqa: D102

                cls,

                b: str | bytes,

                *,

                content_type: str | None = None,

                encoding: str = 'utf8',

                proto: DeprecatedParseProtocol | None = None,

                allow_pickle: bool = False,

            ) -> Self:  # pragma: no cover

                warnings.warn(

                    'The `parse_raw` method is deprecated; if your data is JSON use `model_validate_json`, '

                    'otherwise load the data then use `model_validate` instead.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import parse

                try:

                    obj = parse.load_str_bytes(

                        b,

                        proto=proto,

                        content_type=content_type,

                        encoding=encoding,

                        allow_pickle=allow_pickle,

                    )

                except (ValueError, TypeError) as exc:

                    import json

                    # try to match V1

                    if isinstance(exc, UnicodeDecodeError):

                        type_str = 'value_error.unicodedecode'

                    elif isinstance(exc, json.JSONDecodeError):

                        type_str = 'value_error.jsondecode'

                    elif isinstance(exc, ValueError):

                        type_str = 'value_error'

                    else:

                        type_str = 'type_error'

                    # ctx is missing here, but since we've added `input` to the error, we're not pretending it's the same

                    error: pydantic_core.InitErrorDetails = {

                        # The type: ignore on the next line is to ignore the requirement of LiteralString

                        'type': pydantic_core.PydanticCustomError(type_str, str(exc)),  # type: ignore

                        'loc': ('__root__',),

                        'input': b,

                    }

                    raise pydantic_core.ValidationError.from_exception_data(cls.__name__, [error])

                return cls.model_validate(obj)

    
#### schema

```python3
def schema(
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}'
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `schema` method is deprecated; use `model_json_schema` instead.', category=None)

            def schema(  # noqa: D102

                cls, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn(

                    'The `schema` method is deprecated; use `model_json_schema` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_json_schema(by_alias=by_alias, ref_template=ref_template)

    
#### schema_json

```python3
def schema_json(
    *,
    by_alias: 'bool' = True,
    ref_template: 'str' = '#/$defs/{model}',
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                category=None,

            )

            def schema_json(  # noqa: D102

                cls, *, by_alias: bool = True, ref_template: str = DEFAULT_REF_TEMPLATE, **dumps_kwargs: Any

            ) -> str:  # pragma: no cover

                warnings.warn(

                    'The `schema_json` method is deprecated; use `model_json_schema` and json.dumps instead.',

                    category=PydanticDeprecatedSince20,

                )

                import json

                from .deprecated.json import pydantic_encoder

                return json.dumps(

                    cls.model_json_schema(by_alias=by_alias, ref_template=ref_template),

                    default=pydantic_encoder,

                    **dumps_kwargs,

                )

    
#### update_forward_refs

```python3
def update_forward_refs(
    **localns: 'Any'
) -> 'None'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated(

                'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                category=None,

            )

            def update_forward_refs(cls, **localns: Any) -> None:  # noqa: D102

                warnings.warn(

                    'The `update_forward_refs` method is deprecated; use `model_rebuild` instead.',

                    category=PydanticDeprecatedSince20,

                )

                if localns:  # pragma: no cover

                    raise TypeError('`localns` arguments are not longer accepted.')

                cls.model_rebuild(force=True)

    
#### validate

```python3
def validate(
    value: 'Any'
) -> 'Self'
```

??? example "View Source"
            @classmethod

            @typing_extensions.deprecated('The `validate` method is deprecated; use `model_validate` instead.', category=None)

            def validate(cls, value: Any) -> Self:  # noqa: D102

                warnings.warn(

                    'The `validate` method is deprecated; use `model_validate` instead.', category=PydanticDeprecatedSince20

                )

                return cls.model_validate(value)

#### Instance variables

```python3
model_extra
```

Get extra fields set during validation.

```python3
model_fields_set
```

Returns the set of fields that have been explicitly set on this model instance.

#### Methods

    
#### copy

```python3
def copy(
    self,
    *,
    include: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    exclude: 'AbstractSetIntStr | MappingIntStrAny | None' = None,
    update: 'Dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Returns a copy of the model.

!!! warning "Deprecated"
    This method is now deprecated; use `model_copy` instead.

If you need `include` or `exclude`, use:

```py
data = self.model_dump(include=include, exclude=exclude, round_trip=True)
data = {**data, **(update or {})}
copied = self.model_validate(data)
```

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| include | None | Optional set or mapping specifying which fields to include in the copied model. | None |
| exclude | None | Optional set or mapping specifying which fields to exclude in the copied model. | None |
| update | None | Optional dictionary of field-value pairs to override field values in the copied model. | None |
| deep | None | If True, the values of fields that are Pydantic models will be deep-copied. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A copy of the model with included, excluded and updated fields as specified. |

??? example "View Source"
            @typing_extensions.deprecated(

                'The `copy` method is deprecated; use `model_copy` instead. '

                'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                category=None,

            )

            def copy(

                self,

                *,

                include: AbstractSetIntStr | MappingIntStrAny | None = None,

                exclude: AbstractSetIntStr | MappingIntStrAny | None = None,

                update: Dict[str, Any] | None = None,  # noqa UP006

                deep: bool = False,

            ) -> Self:  # pragma: no cover

                """Returns a copy of the model.

                !!! warning "Deprecated"

                    This method is now deprecated; use `model_copy` instead.

                If you need `include` or `exclude`, use:

                ```py

                data = self.model_dump(include=include, exclude=exclude, round_trip=True)

                data = {**data, **(update or {})}

                copied = self.model_validate(data)

                ```

                Args:

                    include: Optional set or mapping specifying which fields to include in the copied model.

                    exclude: Optional set or mapping specifying which fields to exclude in the copied model.

                    update: Optional dictionary of field-value pairs to override field values in the copied model.

                    deep: If True, the values of fields that are Pydantic models will be deep-copied.

                Returns:

                    A copy of the model with included, excluded and updated fields as specified.

                """

                warnings.warn(

                    'The `copy` method is deprecated; use `model_copy` instead. '

                    'See the docstring of `BaseModel.copy` for details about how to handle `include` and `exclude`.',

                    category=PydanticDeprecatedSince20,

                )

                from .deprecated import copy_internals

                values = dict(

                    copy_internals._iter(

                        self, to_dict=False, by_alias=False, include=include, exclude=exclude, exclude_unset=False

                    ),

                    **(update or {}),

                )

                if self.__pydantic_private__ is None:

                    private = None

                else:

                    private = {k: v for k, v in self.__pydantic_private__.items() if v is not PydanticUndefined}

                if self.__pydantic_extra__ is None:

                    extra: dict[str, Any] | None = None

                else:

                    extra = self.__pydantic_extra__.copy()

                    for k in list(self.__pydantic_extra__):

                        if k not in values:  # k was in the exclude

                            extra.pop(k)

                    for k in list(values):

                        if k in self.__pydantic_extra__:  # k must have come from extra

                            extra[k] = values.pop(k)

                # new `__pydantic_fields_set__` can have unset optional fields with a set value in `update` kwarg

                if update:

                    fields_set = self.__pydantic_fields_set__ | update.keys()

                else:

                    fields_set = set(self.__pydantic_fields_set__)

                # removing excluded fields from `__pydantic_fields_set__`

                if exclude:

                    fields_set -= set(exclude)

                return copy_internals._copy_and_set_values(self, values, fields_set, extra, private, deep=deep)

    
#### dict

```python3
def dict(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False
) -> 'Dict[str, Any]'
```

??? example "View Source"
            @typing_extensions.deprecated('The `dict` method is deprecated; use `model_dump` instead.', category=None)

            def dict(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

            ) -> Dict[str, Any]:  # noqa UP006

                warnings.warn('The `dict` method is deprecated; use `model_dump` instead.', category=PydanticDeprecatedSince20)

                return self.model_dump(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### json

```python3
def json(
    self,
    *,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    encoder: 'Callable[[Any], Any] | None' = PydanticUndefined,
    models_as_dict: 'bool' = PydanticUndefined,
    **dumps_kwargs: 'Any'
) -> 'str'
```

??? example "View Source"
            @typing_extensions.deprecated('The `json` method is deprecated; use `model_dump_json` instead.', category=None)

            def json(  # noqa: D102

                self,

                *,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                encoder: Callable[[Any], Any] | None = PydanticUndefined,  # type: ignore[assignment]

                models_as_dict: bool = PydanticUndefined,  # type: ignore[assignment]

                **dumps_kwargs: Any,

            ) -> str:

                warnings.warn(

                    'The `json` method is deprecated; use `model_dump_json` instead.', category=PydanticDeprecatedSince20

                )

                if encoder is not PydanticUndefined:

                    raise TypeError('The `encoder` argument is no longer supported; use field serializers instead.')

                if models_as_dict is not PydanticUndefined:

                    raise TypeError('The `models_as_dict` argument is no longer supported; use a model serializer instead.')

                if dumps_kwargs:

                    raise TypeError('`dumps_kwargs` keyword arguments are no longer supported.')

                return self.model_dump_json(

                    include=include,

                    exclude=exclude,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                )

    
#### model_copy

```python3
def model_copy(
    self,
    *,
    update: 'dict[str, Any] | None' = None,
    deep: 'bool' = False
) -> 'Self'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

Returns a copy of the model.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| update | None | Values to change/add in the new model. Note: the data is not validated<br>before creating the new model. You should trust this data. | None |
| deep | None | Set to `True` to make a deep copy of the model. | None |

**Returns:**

| Type | Description |
|---|---|
| None | New model instance. |

??? example "View Source"
            def model_copy(self, *, update: dict[str, Any] | None = None, deep: bool = False) -> Self:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#model_copy

                Returns a copy of the model.

                Args:

                    update: Values to change/add in the new model. Note: the data is not validated

                        before creating the new model. You should trust this data.

                    deep: Set to `True` to make a deep copy of the model.

                Returns:

                    New model instance.

                """

                copied = self.__deepcopy__() if deep else self.__copy__()

                if update:

                    if self.model_config.get('extra') == 'allow':

                        for k, v in update.items():

                            if k in self.model_fields:

                                copied.__dict__[k] = v

                            else:

                                if copied.__pydantic_extra__ is None:

                                    copied.__pydantic_extra__ = {}

                                copied.__pydantic_extra__[k] = v

                    else:

                        copied.__dict__.update(update)

                    copied.__pydantic_fields_set__.update(update.keys())

                return copied

    
#### model_dump

```python3
def model_dump(
    self,
    *,
    mode: "Literal['json', 'python'] | str" = 'python',
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'dict[str, Any]'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| mode | None | The mode in which `to_python` should run.<br>If mode is 'json', the output will only contain JSON serializable types.<br>If mode is 'python', the output may contain non-JSON-serializable Python objects. | None |
| include | None | A set of fields to include in the output. | None |
| exclude | None | A set of fields to exclude from the output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to use the field's alias in the dictionary key if defined. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A dictionary representation of the model. |

??? example "View Source"
            def model_dump(

                self,

                *,

                mode: Literal['json', 'python'] | str = 'python',

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> dict[str, Any]:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump

                Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

                Args:

                    mode: The mode in which `to_python` should run.

                        If mode is 'json', the output will only contain JSON serializable types.

                        If mode is 'python', the output may contain non-JSON-serializable Python objects.

                    include: A set of fields to include in the output.

                    exclude: A set of fields to exclude from the output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to use the field's alias in the dictionary key if defined.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A dictionary representation of the model.

                """

                return self.__pydantic_serializer__.to_python(

                    self,

                    mode=mode,

                    by_alias=by_alias,

                    include=include,

                    exclude=exclude,

                    context=context,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                )

    
#### model_dump_json

```python3
def model_dump_json(
    self,
    *,
    indent: 'int | None' = None,
    include: 'IncEx | None' = None,
    exclude: 'IncEx | None' = None,
    context: 'Any | None' = None,
    by_alias: 'bool' = False,
    exclude_unset: 'bool' = False,
    exclude_defaults: 'bool' = False,
    exclude_none: 'bool' = False,
    round_trip: 'bool' = False,
    warnings: "bool | Literal['none', 'warn', 'error']" = True,
    serialize_as_any: 'bool' = False
) -> 'str'
```

Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

Generates a JSON representation of the model using Pydantic's `to_json` method.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| indent | None | Indentation to use in the JSON output. If None is passed, the output will be compact. | None |
| include | None | Field(s) to include in the JSON output. | None |
| exclude | None | Field(s) to exclude from the JSON output. | None |
| context | None | Additional context to pass to the serializer. | None |
| by_alias | None | Whether to serialize using field aliases. | None |
| exclude_unset | None | Whether to exclude fields that have not been explicitly set. | None |
| exclude_defaults | None | Whether to exclude fields that are set to their default value. | None |
| exclude_none | None | Whether to exclude fields that have a value of `None`. | None |
| round_trip | None | If True, dumped values should be valid as input for non-idempotent types such as Json[T]. | None |
| warnings | None | How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,<br>"error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError]. | None |
| serialize_as_any | None | Whether to serialize fields with duck-typing serialization behavior. | None |

**Returns:**

| Type | Description |
|---|---|
| None | A JSON string representation of the model. |

??? example "View Source"
            def model_dump_json(

                self,

                *,

                indent: int | None = None,

                include: IncEx | None = None,

                exclude: IncEx | None = None,

                context: Any | None = None,

                by_alias: bool = False,

                exclude_unset: bool = False,

                exclude_defaults: bool = False,

                exclude_none: bool = False,

                round_trip: bool = False,

                warnings: bool | Literal['none', 'warn', 'error'] = True,

                serialize_as_any: bool = False,

            ) -> str:

                """Usage docs: https://docs.pydantic.dev/2.9/concepts/serialization/#modelmodel_dump_json

                Generates a JSON representation of the model using Pydantic's `to_json` method.

                Args:

                    indent: Indentation to use in the JSON output. If None is passed, the output will be compact.

                    include: Field(s) to include in the JSON output.

                    exclude: Field(s) to exclude from the JSON output.

                    context: Additional context to pass to the serializer.

                    by_alias: Whether to serialize using field aliases.

                    exclude_unset: Whether to exclude fields that have not been explicitly set.

                    exclude_defaults: Whether to exclude fields that are set to their default value.

                    exclude_none: Whether to exclude fields that have a value of `None`.

                    round_trip: If True, dumped values should be valid as input for non-idempotent types such as Json[T].

                    warnings: How to handle serialization errors. False/"none" ignores them, True/"warn" logs errors,

                        "error" raises a [`PydanticSerializationError`][pydantic_core.PydanticSerializationError].

                    serialize_as_any: Whether to serialize fields with duck-typing serialization behavior.

                Returns:

                    A JSON string representation of the model.

                """

                return self.__pydantic_serializer__.to_json(

                    self,

                    indent=indent,

                    include=include,

                    exclude=exclude,

                    context=context,

                    by_alias=by_alias,

                    exclude_unset=exclude_unset,

                    exclude_defaults=exclude_defaults,

                    exclude_none=exclude_none,

                    round_trip=round_trip,

                    warnings=warnings,

                    serialize_as_any=serialize_as_any,

                ).decode()

    
#### model_post_init

```python3
def model_post_init(
    self,
    _BaseModel__context: 'Any'
) -> 'None'
```

Override this method to perform additional initialization after `__init__` and `model_construct`.

This is useful if you want to do some validation that requires the entire model to be initialized.

??? example "View Source"
            def model_post_init(self, __context: Any) -> None:

                """Override this method to perform additional initialization after `__init__` and `model_construct`.

                This is useful if you want to do some validation that requires the entire model to be initialized.

                """

                pass

### TaskEnum

```python3
class TaskEnum(
    *args,
    **kwds
)
```

str(object='') -> str

str(bytes_or_buffer[, encoding[, errors]]) -> str

Create a new string object from the given object. If encoding or
errors is specified, then the object must expose a data buffer
that will be decoded using the given encoding and error handler.
Otherwise, returns the result of object.__str__() (if defined)
or repr(object).
encoding defaults to sys.getdefaultencoding().
errors defaults to 'strict'.

??? example "View Source"
        class TaskEnum(str, Enum):

            image = "image"

            query = "query"

------

#### Ancestors (in MRO)

* builtins.str
* enum.Enum

#### Class variables

```python3
image
```

```python3
name
```

```python3
query
```

```python3
value
```

#### Static methods

    
#### maketrans

```python3
def maketrans(
    ...
)
```

Return a translation table usable for str.translate().

If there is only one argument, it must be a dictionary mapping Unicode
ordinals (integers) or characters to Unicode ordinals, strings or None.
Character keys will be then converted to ordinals.
If there are two arguments, they must be strings of equal length, and
in the resulting dictionary, each character in x will be mapped to the
character at the same position in y. If there is a third argument, it
must be a string, whose characters will be mapped to None in the result.

#### Methods

    
#### capitalize

```python3
def capitalize(
    self,
    /
)
```

Return a capitalized version of the string.

More specifically, make the first character have upper case and the rest lower
case.

    
#### casefold

```python3
def casefold(
    self,
    /
)
```

Return a version of the string suitable for caseless comparisons.

    
#### center

```python3
def center(
    self,
    width,
    fillchar=' ',
    /
)
```

Return a centered string of length width.

Padding is done using the specified fill character (default is a space).

    
#### count

```python3
def count(
    ...
)
```

S.count(sub[, start[, end]]) -> int

Return the number of non-overlapping occurrences of substring sub in
string S[start:end].  Optional arguments start and end are
interpreted as in slice notation.

    
#### encode

```python3
def encode(
    self,
    /,
    encoding='utf-8',
    errors='strict'
)
```

Encode the string using the codec registered for encoding.

encoding
  The encoding in which to encode the string.
errors
  The error handling scheme to use for encoding errors.
  The default is 'strict' meaning that encoding errors raise a
  UnicodeEncodeError.  Other possible values are 'ignore', 'replace' and
  'xmlcharrefreplace' as well as any other name registered with
  codecs.register_error that can handle UnicodeEncodeErrors.

    
#### endswith

```python3
def endswith(
    ...
)
```

S.endswith(suffix[, start[, end]]) -> bool

Return True if S ends with the specified suffix, False otherwise.
With optional start, test S beginning at that position.
With optional end, stop comparing S at that position.
suffix can also be a tuple of strings to try.

    
#### expandtabs

```python3
def expandtabs(
    self,
    /,
    tabsize=8
)
```

Return a copy where all tab characters are expanded using spaces.

If tabsize is not given, a tab size of 8 characters is assumed.

    
#### find

```python3
def find(
    ...
)
```

S.find(sub[, start[, end]]) -> int

Return the lowest index in S where substring sub is found,
such that sub is contained within S[start:end].  Optional
arguments start and end are interpreted as in slice notation.

Return -1 on failure.

    
#### format

```python3
def format(
    ...
)
```

S.format(*args, **kwargs) -> str

Return a formatted version of S, using substitutions from args and kwargs.
The substitutions are identified by braces ('{' and '}').

    
#### format_map

```python3
def format_map(
    ...
)
```

S.format_map(mapping) -> str

Return a formatted version of S, using substitutions from mapping.
The substitutions are identified by braces ('{' and '}').

    
#### index

```python3
def index(
    ...
)
```

S.index(sub[, start[, end]]) -> int

Return the lowest index in S where substring sub is found,
such that sub is contained within S[start:end].  Optional
arguments start and end are interpreted as in slice notation.

Raises ValueError when the substring is not found.

    
#### isalnum

```python3
def isalnum(
    self,
    /
)
```

Return True if the string is an alpha-numeric string, False otherwise.

A string is alpha-numeric if all characters in the string are alpha-numeric and
there is at least one character in the string.

    
#### isalpha

```python3
def isalpha(
    self,
    /
)
```

Return True if the string is an alphabetic string, False otherwise.

A string is alphabetic if all characters in the string are alphabetic and there
is at least one character in the string.

    
#### isascii

```python3
def isascii(
    self,
    /
)
```

Return True if all characters in the string are ASCII, False otherwise.

ASCII characters have code points in the range U+0000-U+007F.
Empty string is ASCII too.

    
#### isdecimal

```python3
def isdecimal(
    self,
    /
)
```

Return True if the string is a decimal string, False otherwise.

A string is a decimal string if all characters in the string are decimal and
there is at least one character in the string.

    
#### isdigit

```python3
def isdigit(
    self,
    /
)
```

Return True if the string is a digit string, False otherwise.

A string is a digit string if all characters in the string are digits and there
is at least one character in the string.

    
#### isidentifier

```python3
def isidentifier(
    self,
    /
)
```

Return True if the string is a valid Python identifier, False otherwise.

Call keyword.iskeyword(s) to test whether string s is a reserved identifier,
such as "def" or "class".

    
#### islower

```python3
def islower(
    self,
    /
)
```

Return True if the string is a lowercase string, False otherwise.

A string is lowercase if all cased characters in the string are lowercase and
there is at least one cased character in the string.

    
#### isnumeric

```python3
def isnumeric(
    self,
    /
)
```

Return True if the string is a numeric string, False otherwise.

A string is numeric if all characters in the string are numeric and there is at
least one character in the string.

    
#### isprintable

```python3
def isprintable(
    self,
    /
)
```

Return True if the string is printable, False otherwise.

A string is printable if all of its characters are considered printable in
repr() or if it is empty.

    
#### isspace

```python3
def isspace(
    self,
    /
)
```

Return True if the string is a whitespace string, False otherwise.

A string is whitespace if all characters in the string are whitespace and there
is at least one character in the string.

    
#### istitle

```python3
def istitle(
    self,
    /
)
```

Return True if the string is a title-cased string, False otherwise.

In a title-cased string, upper- and title-case characters may only
follow uncased characters and lowercase characters only cased ones.

    
#### isupper

```python3
def isupper(
    self,
    /
)
```

Return True if the string is an uppercase string, False otherwise.

A string is uppercase if all cased characters in the string are uppercase and
there is at least one cased character in the string.

    
#### join

```python3
def join(
    self,
    iterable,
    /
)
```

Concatenate any number of strings.

The string whose method is called is inserted in between each given string.
The result is returned as a new string.

Example: '.'.join(['ab', 'pq', 'rs']) -> 'ab.pq.rs'

    
#### ljust

```python3
def ljust(
    self,
    width,
    fillchar=' ',
    /
)
```

Return a left-justified string of length width.

Padding is done using the specified fill character (default is a space).

    
#### lower

```python3
def lower(
    self,
    /
)
```

Return a copy of the string converted to lowercase.

    
#### lstrip

```python3
def lstrip(
    self,
    chars=None,
    /
)
```

Return a copy of the string with leading whitespace removed.

If chars is given and not None, remove characters in chars instead.

    
#### partition

```python3
def partition(
    self,
    sep,
    /
)
```

Partition the string into three parts using the given separator.

This will search for the separator in the string.  If the separator is found,
returns a 3-tuple containing the part before the separator, the separator
itself, and the part after it.

If the separator is not found, returns a 3-tuple containing the original string
and two empty strings.

    
#### removeprefix

```python3
def removeprefix(
    self,
    prefix,
    /
)
```

Return a str with the given prefix string removed if present.

If the string starts with the prefix string, return string[len(prefix):].
Otherwise, return a copy of the original string.

    
#### removesuffix

```python3
def removesuffix(
    self,
    suffix,
    /
)
```

Return a str with the given suffix string removed if present.

If the string ends with the suffix string and that suffix is not empty,
return string[:-len(suffix)]. Otherwise, return a copy of the original
string.

    
#### replace

```python3
def replace(
    self,
    old,
    new,
    count=-1,
    /
)
```

Return a copy with all occurrences of substring old replaced by new.

count
    Maximum number of occurrences to replace.
    -1 (the default value) means replace all occurrences.

If the optional argument count is given, only the first count occurrences are
replaced.

    
#### rfind

```python3
def rfind(
    ...
)
```

S.rfind(sub[, start[, end]]) -> int

Return the highest index in S where substring sub is found,
such that sub is contained within S[start:end].  Optional
arguments start and end are interpreted as in slice notation.

Return -1 on failure.

    
#### rindex

```python3
def rindex(
    ...
)
```

S.rindex(sub[, start[, end]]) -> int

Return the highest index in S where substring sub is found,
such that sub is contained within S[start:end].  Optional
arguments start and end are interpreted as in slice notation.

Raises ValueError when the substring is not found.

    
#### rjust

```python3
def rjust(
    self,
    width,
    fillchar=' ',
    /
)
```

Return a right-justified string of length width.

Padding is done using the specified fill character (default is a space).

    
#### rpartition

```python3
def rpartition(
    self,
    sep,
    /
)
```

Partition the string into three parts using the given separator.

This will search for the separator in the string, starting at the end. If
the separator is found, returns a 3-tuple containing the part before the
separator, the separator itself, and the part after it.

If the separator is not found, returns a 3-tuple containing two empty strings
and the original string.

    
#### rsplit

```python3
def rsplit(
    self,
    /,
    sep=None,
    maxsplit=-1
)
```

Return a list of the substrings in the string, using sep as the separator string.

sep
    The separator used to split the string.

    When set to None (the default value), will split on any whitespace
    character (including \n \r \t \f and spaces) and will discard
    empty strings from the result.
  maxsplit
    Maximum number of splits.
    -1 (the default value) means no limit.

Splitting starts at the end of the string and works to the front.

    
#### rstrip

```python3
def rstrip(
    self,
    chars=None,
    /
)
```

Return a copy of the string with trailing whitespace removed.

If chars is given and not None, remove characters in chars instead.

    
#### split

```python3
def split(
    self,
    /,
    sep=None,
    maxsplit=-1
)
```

Return a list of the substrings in the string, using sep as the separator string.

sep
    The separator used to split the string.

    When set to None (the default value), will split on any whitespace
    character (including \n \r \t \f and spaces) and will discard
    empty strings from the result.
  maxsplit
    Maximum number of splits.
    -1 (the default value) means no limit.

Splitting starts at the front of the string and works to the end.

Note, str.split() is mainly useful for data that has been intentionally
delimited.  With natural text that includes punctuation, consider using
the regular expression module.

    
#### splitlines

```python3
def splitlines(
    self,
    /,
    keepends=False
)
```

Return a list of the lines in the string, breaking at line boundaries.

Line breaks are not included in the resulting list unless keepends is given and
true.

    
#### startswith

```python3
def startswith(
    ...
)
```

S.startswith(prefix[, start[, end]]) -> bool

Return True if S starts with the specified prefix, False otherwise.
With optional start, test S beginning at that position.
With optional end, stop comparing S at that position.
prefix can also be a tuple of strings to try.

    
#### strip

```python3
def strip(
    self,
    chars=None,
    /
)
```

Return a copy of the string with leading and trailing whitespace removed.

If chars is given and not None, remove characters in chars instead.

    
#### swapcase

```python3
def swapcase(
    self,
    /
)
```

Convert uppercase characters to lowercase and lowercase characters to uppercase.

    
#### title

```python3
def title(
    self,
    /
)
```

Return a version of the string where each word is titlecased.

More specifically, words start with uppercased characters and all remaining
cased characters have lower case.

    
#### translate

```python3
def translate(
    self,
    table,
    /
)
```

Replace each character in the string using the given translation table.

table
    Translation table, which must be a mapping of Unicode ordinals to
    Unicode ordinals, strings, or None.

The table must implement lookup/indexing via __getitem__, for instance a
dictionary or list.  If this operation raises LookupError, the character is
left untouched.  Characters mapped to None are deleted.

    
#### upper

```python3
def upper(
    self,
    /
)
```

Return a copy of the string converted to uppercase.

    
#### zfill

```python3
def zfill(
    self,
    width,
    /
)
```

Pad a numeric string with zeros on the left, to fill a field of the given width.

The string is never truncated.