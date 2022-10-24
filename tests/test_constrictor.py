from typing import Any, Dict, Set, List
from request_constraints import constrictor

valid_combinations: List[Dict[str, Set[Any]]] = [
    {"level": {"500"}, "param": {"Z", "T"}, "step": {"24", "36", "48"}},
    {"level": {"1000"}, "param": {"Z"}, "step": {"24", "48"}},
    {"level": {"850"}, "param": {"T"}, "step": {"36", "48"}},
]


def test_get_possible_values() -> None:
    res = constrictor.get_possible_values(
        {},
        valid_combinations
    )
    for key, value in res.items():
        assert set(value) == set({"level": ["1000", "850", "500"], "param": ["T", "Z"], "step": ["48", "36", "24"]}[key])

    res = constrictor.get_possible_values(
        {"level": {"850"}},
        valid_combinations
    )
    for key, value in res.items():
        assert set(value) == set({"level": ["850"], "param": ["T"], "step": ["48", "36"]}[key])

    res = constrictor.get_possible_values(
        {"level": {"1000"}, "step": {"24"}},
        valid_combinations
    )
    for key, value in res.items():
        assert set(value) == set({"level": ["1000"], "param": ["Z"], "step": ["24", "48"]}[key])