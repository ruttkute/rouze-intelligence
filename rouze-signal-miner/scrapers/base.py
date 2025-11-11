from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseScraper(ABC):
    name: str = "base"

    @abstractmethod
    def run(self) -> List[Dict[str, Any]]:
        """Return a list of normalized records (dicts)."""
        raise NotImplementedError
