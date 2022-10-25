import json
from request_constraints import constrictor
from tranquilizer import tranquilize
from typing import Any, Dict, List


possible_selections: Dict[str, List[Any]] = {
    "level": ["500", "850", "1000"],
    "param": ["Z", "T"],
    "step": ["24", "36", "48"],
    "number": ["1", "2", "3"]
}


@tranquilize(method="post")
def validate(constraints: str, selection: str) -> Dict[str, List[Any]]:
    parsed_possible_selections = constrictor.parse_possible_selections(possible_selections)
    parsed_valid_combinations = constrictor.parse_valid_combinations(json.loads(constraints))
    parsed_current_selection = constrictor.parse_current_selection(json.loads(selection))
    result = constrictor.apply_constraints(
        parsed_possible_selections,
        parsed_valid_combinations,
        parsed_current_selection
    )
    return result
