import json
from constrictor import apply_constraints, load_combinations
from tranquilizer import tranquilize


@tranquilize(method="post")
def validate(constraints: str, selection: str) -> str:
    parsed_constraints = load_combinations(json.loads(constraints))
    parsed_selection = json.loads(selection)
    result = apply_constraints(parsed_constraints, parsed_selection)
    return result
