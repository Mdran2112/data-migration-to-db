from typing import Dict, Any


class DataRule:
    """
    Abstract class for implementing different kinds of rules over input data.
    """
    def satisfies(self, _object: Dict[str, Any]) -> bool:
        raise NotImplementedError
