import json
from request_constraints import constrictor
from tranquilizer import tranquilize


@tranquilize(method="post")
def validate(constraints: str, selection: str) -> str:
    parsed_constraints = constrictor.load_combinations(json.loads(constraints))
    parsed_selection = json.loads(selection)
    result = constrictor.apply_constraints(parsed_constraints, parsed_selection)
    return result
