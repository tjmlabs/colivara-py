from .client import ColiVara
from .async_client import AsyncColiVara

# Create aliases
colivara = ColiVara
COLIVARA = ColiVara
Colivara = ColiVara

asynccolivara = AsyncColiVara
ASYNCCOLIVARA = AsyncColiVara
AsyncColivara = AsyncColiVara

__all__ = [
    "ColiVara",
    "colivara",
    "COLIVARA",
    "Colivara",
    "AsyncColiVara",
    "asynccolivara",
    "ASYNCCOLIVARA",
    "AsyncColivara",
]
