from datetime import datetime
from typing import Any, Dict, Set, List
import json
import re


def load_combinations(combinations: List) -> List[Dict[str, Set[Any]]]:
    for combination in combinations:
        for field_name, field_values in combination.items():
            combination[field_name] = set(field_values)
    return combinations


def apply_constraints(valid_combinations, current_selection):
    if current_selection:
        return get_possible_values(current_selection, valid_combinations)
    return {}


# Le combinazioni valide sono quelle per le quali, PER OGNI CAMPO,
# è presente almeno 1 elemento della current selection
def get_possible_values(
    current_selection: Dict[str, Set[Any]],
    valid_combinations: List[Dict[str, List[Any]]],
) -> Dict[str, Set[Any]]:
    result: Dict[str, Set[Any]] = {}
    for valid_combination in valid_combinations:
        ok = True
        for field_name, selected_values in current_selection.items():
            if field_name in valid_combination.keys():
                if len(set(selected_values) & valid_combination[field_name]) == 0:
                    ok = False
                    break
            else:
                result.setdefault(field_name, list(current_selection[field_name]))
        if ok:
            for field_name, valid_values in valid_combination.items():
                current = result.setdefault(field_name, set())
                current |= set(valid_values)
    return {k: list(v) for (k, v) in result.items()}
