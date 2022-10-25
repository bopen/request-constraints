from typing import Any, Dict, Set, List
from request_constraints import constrictor

possible_selections: Dict[str, List[Any]] = {
    "level": ["500", "850", "1000"],
    "param": ["Z", "T"],
    "step": ["24", "36", "48"],
    "number": ["1", "2", "3"]
}

valid_combinations: List[Dict[str, List[Any]]] = [
    {"level": ["500"], "param": ["Z", "T"], "step": ["24", "36", "48"]},
    {"level": ["1000"], "param": ["Z"], "step": ["24", "48"]},
    {"level": ["850"], "param": ["T"], "step": ["36", "48"]},
]

test_selections: List[Dict[str, List[Any]]] = [
    {},  # 0
    {"number": ["1", "2"]},  # 1
    {"level": ["850"], "param": ["Z"]},  # 2
    {"level": ["850"], "param": ["Z"], "number": ["1", "2"]},  # 3
    {"level": ["850"]},  # 4
    {"level": ["850"], "number": ["1"]},  # 5
    {"level": ["1000"], "step": ["24"]},  # 6
    {"level": ["850", "1000"], "param": ["T", "Z"]},  # 7
    {"level": ["850"], "param": ["T"], "step": ["48", "36"], "number": ["1"]},  # 8
    {"level": ["850"], "param": ["T"], "step": ["48", "36"], "number": ["1", "2", "3"]},  # 9
    {"level": ["1000", "850", "500"], "param": ["T", "Z"], "step": ["48", "36", "24"], "number": ["1", "2", "3"]}  # 10
]

expected_results: List[Dict[str, List[Any]]] = [
    {"level": ["1000", "850", "500"], "param": ["T", "Z"], "step": ["48", "36", "24"], "number": ["1", "2", "3"]},  # 0
    {"level": ["1000", "850", "500"], "param": ["T", "Z"], "step": ["48", "36", "24"], "number": ["1", "2", "3"]},  # 1
    {},   # 2
    {},   # 3
    {"level": ["850"], "param": ["T"], "step": ["48", "36"], "number": ["1", "2", "3"]},  # 4
    {"level": ["850"], "param": ["T"], "step": ["48", "36"], "number": ["1", "2", "3"]},  # 5
    {"level": ["1000"], "param": ["Z"], "step": ["24", "48"], "number": ["1", "2", "3"]},  # 6
    {"level": ["850", "1000"], "param": ["T", "Z"], "step": ["24", "48", "36"], "number": ["1", "2", "3"]},  # 7
    {"level": ["850"], "param": ["T"], "step": ["48", "36"], "number": ["1", "2", "3"]},  # 8
    {"level": ["850"], "param": ["T"], "step": ["48", "36"], "number": ["1", "2", "3"]},  # 9
    {"level": ["1000", "850", "500"], "param": ["T", "Z"], "step": ["48", "36", "24"], "number": ["1", "2", "3"]}  # 10
]


def test_get_possible_values() -> None:
    for i in range(len(test_selections)):
        parsed_possible_selections = constrictor.parse_possible_selections(possible_selections)
        parsed_current_selection = constrictor.parse_current_selection(test_selections[i])
        parsed_valid_combinations = constrictor.parse_valid_combinations(valid_combinations)

        result = constrictor.get_possible_values(
            parsed_possible_selections,
            parsed_current_selection,
            parsed_valid_combinations
        )

        for key, value in expected_results[i].items():
            assert set(value) == set(result[key])