from typing import Any
import fastapi
import json
import fastapi.staticfiles
from pydantic import BaseModel
from cads_catalogue_api_service import constrictor

app = fastapi.FastAPI()


class Data(BaseModel):
    constraints: str
    selection: str
    configuration: str


@app.post("/validate")
def validate(
    data: Data,
) -> dict[str, list[Any]]:
    parsed_possible_selections = constrictor.parse_possible_selections(
        json.loads(data.configuration)
    )
    parsed_valid_combinations = constrictor.parse_valid_combinations(
        json.loads(data.constraints)
    )
    parsed_current_selection = constrictor.parse_current_selection(
        json.loads(data.selection)
    )
    result = constrictor.apply_constraints(
        parsed_possible_selections, parsed_valid_combinations, parsed_current_selection
    )
    return result


app.mount(
    "/", fastapi.staticfiles.StaticFiles(directory="webapp", html=True), name="webapp"
)
