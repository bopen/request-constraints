import json
from request_constraints import constrictor
from tranquilizer import tranquilize
from typing import Any, Dict, List


@tranquilize(method="post")
def validate(
    constraints: str, selection: str, configuration: str
) -> Dict[str, List[Any]]:
    parsed_possible_selections = constrictor.parse_possible_selections(
        json.loads(configuration)
    )
    parsed_valid_combinations = constrictor.parse_valid_combinations(
        json.loads(constraints)
    )
    parsed_current_selection = constrictor.parse_current_selection(
        json.loads(selection)
    )
    result = constrictor.apply_constraints(
        parsed_possible_selections, parsed_valid_combinations, parsed_current_selection
    )
    return result
