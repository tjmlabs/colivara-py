# colivara-py


[![PyPI](https://img.shields.io/pypi/v/colivara-py.svg)](https://pypi.org/project/colivara-py/)
[![Changelog](https://img.shields.io/github/v/release/tjmlabs/colivara-py?include_prereleases&label=changelog)](https://github.com/tjmlabs/colivara-py/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/tjmlabs/colivara-py/blob/main/LICENSE)
[![Tests](https://github.com/tjmlabs/colivara-py/actions/workflows/test.yml/badge.svg)](https://github.com/tjmlabs/colivara-py/actions/workflows/test.yml) [![codecov](https://codecov.io/gh/tjmlabs/ColiVara/branch/main/graph/badge.svg)](https://codecov.io/gh/tjmlabs/ColiVara)

The official Python SDK for the ColiVara API. ColiVara is a document search and retrieval API that uses advanced machine learning techniques to index and search documents. This SDK allows you to interact with the API to create collections, upload documents, search for documents, and generate embeddings.

## Installation

Install `colivara-py` using pip:

```bash
pip install colivara-py
```

---

## Usage

Refer to the [ColiVara API documentation](https://docs.colivara.com) for detailed guidance on how to use this library.

### Requirements
- You need access to the ColiVara API, which you can self-host (see [ColiVara API repo](https://github.com/tjmlabs/ColiVara)) or use the hosted version at [colivara.com](https://colivara.com).
- Obtain an API key by signing up at [ColiVara](https://colivara.com) or from your self-hosted API.

### Example Code

```python
import os
from colivara_py import ColiVara

rag_client = ColiVara(api_key="your_api_key")

# Create a new collection (optional)
new_collection = rag_client.create_collection(name="my_collection", metadata={"description": "A sample collection"})
print(f"Created collection: {new_collection.name}")

# Upload a document to the collection (jpg, md, png, pdf, docx, etc... supported)
document = rag_client.upsert_document(
    name="sample_document",
    collection_name="my_collection",  # Defaults to "default_collection"
    document_url="https://example.com/sample.pdf", # Alternatively, use document_path="path/to/document.pdf" 
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


# Search using images
image_search_results = rag_client.search_image(
    collection_name="my_collection",
    image_path="path/to/image.jpg",  # Alternatively, use image_base64="base64_encoded_string"
    top_k=3
)
for result in image_search_results.results:
    print(f"Page {result.page_number} of {result.document_name}: Score {result.normalized_score}")

# List documents in a collection
documents = rag_client.list_documents(collection_name="my_collection")
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

---

## Development

### Setting up the Development Environment

1. Clone the repository and navigate to the project directory:

    ```bash
    cd colivara-py
    ```

2. Create a virtual environment:

    ```bash
    uv venv
    ```

3. Activate the virtual environment:

    **macOS/Linux:**
    ```bash
    source .venv/bin/activate
    ```

    **Windows:**
    ```bash
    .venv\Scripts\activate
    ```

4. Install the development dependencies:

    ```bash
    uv sync --extra dev-dependencies
    ```

5. Run tests:

    ```bash
    pytest
    ```

### Regenerating the SDK

If the OpenAPI specification is updated, regenerate the SDK as follows:

1. Install the OpenAPI generator (on macOS, use Homebrew):

    ```bash
    brew install openapi-generator
    ```

2. Verify the installation:

    ```bash
    openapi-generator version
    ```

3. Run the OpenAPI generator from the project directory:

    ```bash
    openapi-generator generate -i https://api.colivara.com/v1/openapi.json -g python -c config.yaml --ignore-file-override .openapi-generator-ignore --template-dir ./templates
    ```


---

## Updating the SDK and Documentation

Follow these steps for major changes to the OpenAPI spec:

1. Regenerate the SDK using the OpenAPI generator.  
2. Update the client interface in `colivara_py/client.py`. if needed
3. Modify tests in the `tests` directory to reflect the changes. if needed.
4. Run tests to ensure functionality.  


---

## Building Documentation Locally

Generate and view the SDK documentation:

1. To serve the documentation locally:

    ```bash
    pdocs server colivara_py
    ```

2. To generate documentation as HTML:

    ```bash
    pdocs as_html colivara_py --overwrite
    ```

3. To generate documentation as Markdown:

    ```bash
    pdocs as_markdown colivara_py
    ```

---

## License

This SDK is licensed under the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0). The ColiVara API is licensed under the Functional Source License, Version 1.1, Apache 2.0 Future License. See [LICENSE.md](LICENSE.md) for details.

For commercial licensing, contact us via [tjmlabs.com](https://tjmlabs.com). We’re happy to work with you to provide a license tailored to your needs.

