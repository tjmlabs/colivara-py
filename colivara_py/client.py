import os
import requests
from typing import Optional, Dict, Any, List
from .models import CollectionIn, CollectionOut, GenericError, PatchCollectionIn

class Colivara:
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = base_url or "https://api.colivara.com"  
        self.api_key = api_key or os.getenv("COLIVARA_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either through parameter or COLIVARA_API_KEY environment variable.")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def create_collection(self, name: str, metadata: Optional[Dict[str, Any]] = {}) -> CollectionOut:
        url = f"{self.base_url}/v1/collections/"
        payload = CollectionIn(name=name, metadata=metadata).model_dump()
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code == 201:
            return CollectionOut(**response.json())
        elif response.status_code == 409:
            error = GenericError(**response.json())
            raise Exception(f"Conflict error: {error.detail}")
        else:
            response.raise_for_status()


    def list_collections(self) -> List[CollectionOut]:
        url = f"{self.base_url}/v1/collections/"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status() 
        
        if response.status_code == 200:
            collections_data = response.json()
            # Handle potential empty list
            if isinstance(collections_data, list):
                return [CollectionOut(**collection) for collection in collections_data]
            else:
                raise ValueError(f"Unexpected response format: {collections_data}")
        else:
            response.raise_for_status()


    def get_collection(self, collection_name: str) -> CollectionOut:
        url = f"{self.base_url}/v1/collections/{collection_name}/"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return CollectionOut(**response.json())
        elif response.status_code == 404:
            raise Exception(f"Collection '{collection_name}' not found.")
        else:
            response.raise_for_status()


    def partial_update_collection(self, collection_name: str, name: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> CollectionOut:
        """
        Partially updates a collection.

        Args:
            collection_name: The name of the collection to update.
            new_name: The new name for the collection (optional).
            new_metadata: The new metadata for the collection (optional).

        Returns:
            The updated CollectionOut object.

        Raises:
            Exception: If the collection is not found or there's a problem with the update.
        """

        url = f"{self.base_url}/v1/collections/{collection_name}/"
        
        # Create a CollectionIn object with sane defaults and only updated fields
        updated_data = PatchCollectionIn(name=name, metadata=metadata)

        payload = updated_data.model_dump() 
        response = requests.patch(url, json=payload, headers=self.headers)

        if response.status_code == 200:
            return CollectionOut(**response.json())
        elif response.status_code == 404:
            raise Exception(f"Collection '{collection_name}' not found.")
        else:
            response.raise_for_status()

    def delete_collection(self, collection_name: str) -> None:
        url = f"{self.base_url}/v1/collections/{collection_name}/"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return
        elif response.status_code == 404:
            raise Exception(f"Collection '{collection_name}' not found.")
        else:
            response.raise_for_status()