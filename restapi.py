import json
from typing import Any, Dict, List

from tranquilizer import tranquilize

from cads_catalogue_api_service import constrictor


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
