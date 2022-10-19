from typing import Any
import json


def load_valid_combinations(
        path: str
) -> list[dict[str, set[Any]]]:
    """
    Loads valid params combinations from a JSON file
    at path :param:`path`

    :param path: the path to the .json file containing the valid combinations
    :type: srt

    :rtype: list[dict[str, set[Any]]]:
    :return: list of dictionaries containing all the valid combinations for a
    given dataset.

    """
    combinations = json.load(open(path))
    for combination in combinations:
        for field_name, field_values in combination.items():
            combination[field_name] = set(field_values)
    return combinations


def get_possible_values(
        valid_combinations: list[dict[str, set[Any]]],
        current_selection: dict[str, set[Any]],
)-> dict[str, set[Any]]:
    """Checks the current selection against all valid combinations.
    TODO: Handles special cases such as the "date" field.
    A combination is valid if every field contains
    at least one value from the current selection.
    If a combination is valid, its values are added to the pool
    of valid values (i.e. those that can still be selected without
    running into an invalid request).

    :param valid_combinations: a list of dictionaries representing
    all valid combinations for a specific dataset
    e.g. valid_combinations =
    [{
        "date": {"1990-01-01;1999-12-31", "2010-10-10;2011-11-11"},
        "city": {"rome", "paris", "london"},
        "level": {"500"},
        "param": {"Z"},
        "step": {"24", "36", "48"}
      }, {
        "date": {"1990-01-01;2011-12-31"},
        "city": {"paris", "london"},
        "level": {"1000"},
        "param": {"Z"},
        "step": {"24", "48"}
      }, {
        "date": {"1980-01-01;2011-12-31"},
        "city": {"rome", "paris", "london"},
        "level": {"850"},
        "param": {"T"},
        "step": {"36", "48"}
    }]
    :type: list[dict[str, set[Any]]]:

    :param current_selection: a dictionary containing the current selection
    e.g. current_selection = {
        "date": {"1990-01-01;1999-12-31"},
        "param": {"T"},
        "level": {'850'},
    }
    :type: dict[str, set[Any]]:

    :rtype: dict[str, set[Any]]:
    :return: a dictionary containing all possible values,
    i.e. those that can still be selected without running into an invalid request
    e.g. {
        'city': {'london', 'paris', 'rome'},
        'level': {'850'},
        'param': {'T'},
        'step': {'36', '48'},
        'date': {'1990-01-01;1999-12-31'}
     }
    """
    return get_possible_values_no_range(current_selection, valid_combinations)


def get_possible_values_no_range(
        valid_combinations: list[dict[str, set[Any]]],
        current_selection: dict[str, set[Any]],
) -> dict[str, set[Any]]:
    """Works only for enumerated fields, i.e. fields with values
     that must be selected one by one (no ranges).
    Checks the current selection against all valid combinations.
    A combination is valid if every field contains
    at least one value from the current selection.
    If a combination is valid, its values are added to the pool
    of valid values (i.e. those that can still be selected without
    running into an invalid request).

    :param valid_combinations: a list of dictionaries representing
    all valid combinations for a specific dataset
    e.g. valid_combinations = [
    {"level": {"500"}, "param": {"Z", "T"}, "step": {"24", "36", "48"}},
    {"level": {"1000"}, "param": {"Z"}, "step": {"24", "48"}},
    {"level": {"850"}, "param": {"T"}, "step": {"36", "48"}},
    ]
    :type: list[dict[str, set[Any]]]:

    :param current_selection: a dictionary containing the current selectio
    e.g. current_selection = {
    "param": {"T"},
    "level": {"850", "500"},
    "step": {"36"}
    }
    :type: dict[str, set[Any]]:

    :rtype: dict[str, set[Any]]:
    :return: a dictionary containing all possible values,
    i.e. those that can still be selected without running into an invalid request
    e.g. {'level': {'500', '850'}, 'param': {'T', 'Z'}, 'step': {'24', '36', '48'}}

    """

    result: dict[str, set[Any]] = {}
    for valid_combination in valid_combinations:
        ok = True
        for filed_name, selected_values in current_selection.items():
            if len(selected_values & valid_combination[filed_name]) == 0:
                ok = False
                break
        if ok:
            for filed_name, valid_values in valid_combination.items():
                current = result.setdefault(filed_name, set())
                current |= valid_values
    return result
