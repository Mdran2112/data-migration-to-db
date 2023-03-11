import logging
from typing import Dict, Any
from pandas import NaT

from api.rules.data_rule import DataRule


class AllFieldsRequired(DataRule):
    """
    Whether a field is missing or not in an object that has to be inserted in a table.
    """
    def satisfies(self, _object: Dict[str, Any]) -> bool:
        if (None in _object.values()) or (NaT in _object.values()):
            # NaT is considered too, in case of missing datetime.
            logging.warning(f"Object {_object} doesn't have all required fields! Will be omitted.")
            return False
        return True
