from datetime import datetime
from typing import Any
import json
import re

def load_combinations(path: str) -> list[dict[str, set[Any]]]:
    combinations = json.load(open(path))
    for combination in combinations:
        for field_name, field_values in combination.items():
            combination[field_name] = set(field_values)
    return combinations

def apply_constraints(valid_combinations, current_selection):
    return get_possible_values(current_selection, valid_combinations)

# Le combinazioni valide sono quelle per le quali, PER OGNI CAMPO,
# è presente almeno 1 elemento della current selection
def get_possible_values(
        current_selection: dict[str, set[Any]],
        valid_combinations: list[dict[str, set[Any]]],
) -> dict[str, set[Any]]:
    result: dict[str, set[Any]] = {}
    for valid_combination in valid_combinations:
        ok = True
        for filed_name, selected_values in current_selection.items():
            if (len(selected_values & valid_combination[filed_name]) == 0):
                ok = False
                break
        if ok:
            for filed_name, valid_values in valid_combination.items():
                current = result.setdefault(filed_name, set())
                current |= valid_values
    return result
