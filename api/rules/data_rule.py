from typing import Dict, Any


class DataRule:

    def satisfies(self, _object: Dict[str, Any]) -> bool:
        raise NotImplementedError
