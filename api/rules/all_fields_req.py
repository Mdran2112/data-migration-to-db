import logging
from typing import Dict, Any
from pandas import NaT

from api.rules.data_rule import DataRule


class AllFieldsRequired(DataRule):

    def satisfies(self, _object: Dict[str, Any]) -> bool:
        if (None in _object.values()) or (NaT in _object.values()):
            logging.warning(f"Object {_object} doesn't have all required fields! Will be omitted.")
            return False
        return True
