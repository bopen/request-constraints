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
    parsed_form = constrictor.parse_form(
        json.loads(data.configuration)
    )
    parsed_combinations = constrictor.parse_combinations(
        json.loads(data.constraints)
    )
    parsed_selection = constrictor.parse_selection(
        json.loads(data.selection)
    )
    result = constrictor.apply_constraints(
        parsed_form, parsed_combinations, parsed_selection
    )
    return result


app.mount(
    "/", fastapi.staticfiles.StaticFiles(directory="webapp", html=True), name="webapp"
)
