# colivara-py

[![PyPI](https://img.shields.io/pypi/v/colivara-py.svg)](https://pypi.org/project/colivara-py/)
[![Changelog](https://img.shields.io/github/v/release/tjmlabs/colivara-py?include_prereleases&label=changelog)](https://github.com/tjmlabs/colivara-py/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/tjmlabs/colivara-py/blob/main/LICENSE)
[![Tests](https://github.com/tjmlabs/colivara-py/actions/workflows/test.yml/badge.svg)](https://github.com/tjmlabs/colivara-py/actions/workflows/test.yml) [![codecov](https://codecov.io/gh/tjmlabs/ColiVara/branch/main/graph/badge.svg)](https://codecov.io/gh/tjmlabs/ColiVara)

The official Python SDK for the ColiVara API. ColiVara is a document search and retrieval API that uses advanced machine learning techniques to index and search documents. This SDK allows you to interact with the API to create collections, upload documents, search for documents, and generate embeddings.

## Installation

Install this library using `pip`:
```bash
pip install colivara-py
```
## Usage

Please see the [ColiVara API documentation](https://docs.colivara.com) for more information on how to use this library.

You will need to either self-host the API (see the [ColiVara API repo](https://github.com/tjmlabs/ColiVara)) or use the hosted version at https://colivara.com. You will also need an API key, which you can obtain by signing up at [ColiVara](https://colivara.com) or from your self-hosted API.

```python
import os
from colivara_py import ColiVara


rag_client = ColiVara(
     # This is the default and can be omitted
    api_key=os.environ.get("COLIVARA_API_KEY"),
    # This is the default and can be omitted
    base_url="https://api.colivara.com"
)
# Create a new collection (optional)
new_collection = rag_client.create_collection(name="my_collection", metadata={"description": "A sample collection"})
print(f"Created collection: {new_collection.name}")

# Upload a document to the collection
document = rag_client.upsert_document(
    name="sample_document",
    # optional, defaults to "default_collection"
    collection_name="my_collection", 
    url="https://example.com/sample.pdf",
    metadata={"author": "John Doe"}
)
print(f"Uploaded document: {document.name}")

# Search for documents
search_results = rag_client.search(
    query="machine learning",
    collection_name="my_collection",
    top_k=3
)
for result in search_results.results:
    print(f"Page {result.page_number} of {result.document_name}: Score {result.normalized_score}")

# List documents in a collection
documents = client.list_documents(collection_name="my_collection")
for doc in documents:
    print(f"Document: {doc.name}, Pages: {doc.num_pages}")

# Generate embeddings
embeddings = rag_client.create_embedding(
    input_data=["This is a sample text for embedding"],
    task="query"
)
print(f"Generated {len(embeddings.data)} embeddings")

# Delete a document
rag_client.delete_document("sample_document", collection_name="my_collection")
print("Document deleted")
```

## Development

To contribute to this library, first checkout the code. Then create a new virtual environment:

We use uv, but you can use the pip interface if you prefer:

```bash
cd colivara-py
uv venv
source .venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
uv sync --extra dev-dependencies
```
To run the tests:
```bash
pytest
```

To build the documenation locally:
```bash
pdocs server colivara_py #to see the documentation locally.  
pdocs as_html colivara_py --overwrite #to generate HTML.
pdocs as_markdown colivara_py #to generate markdown.
```

## License
This SDK is distributed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). The API is licensed under Functional Source License, Version 1.1, Apache 2.0 Future License. See the [LICENSE.md](LICENSE.md) file for details.

For commercial licensing, please contact us at [tjmlabs.com](https://tjmlabs.com). We are happy to work with you to provide a license that meets your needs.