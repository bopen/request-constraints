from typing import Any, Dict, Set, List


def parse_valid_combinations(
        valid_combinations
) -> List[Dict[str, Set[Any]]]:
    """
    Parse valid combinations for a given dataset.

    :param valid_combinations: valid combinations in json format
    :type: List[Dict[str, List[Any]]]

    :rtype: list[Dict[str, Set[Any]]]:
    :return: list of dictionaries containing all valid combinations for a
    given dataset.

    """
    for combination in valid_combinations:
        for field_name, field_values in combination.items():
            combination[field_name] = set(field_values)
    return valid_combinations


def parse_possible_selections(
    possible_selections
) -> Dict[str, Set[Any]]:
    for field_name, field_values in possible_selections.items():
        possible_selections[field_name] = set(field_values)
    return possible_selections


def parse_current_selection(
    current_selection
) -> Dict[str, Set[Any]]:
    for field_name, field_values in current_selection.items():
        current_selection[field_name] = set(field_values)
    return current_selection


def apply_constraints(
    possible_selections: Dict[str, Set[Any]],
    valid_combinations: List[Dict[str, Set[Any]]],
    current_selection: Dict[str, Set[Any]],
) -> Dict[str, List[Any]]:
    """Checks the current selection against all valid combinations.
    TODO: Handle special cases such as the "date" field.
    A combination is valid if every field contains
    at least one value from the current selection.
    If a combination is valid, its values are added to the pool
    of valid values (i.e. those that can still be selected without
    running into an invalid request).

    :param possible_selections: a dict of all selectable fields and values
    e.g. possible_selections = {
        "date": {"1990-01-01;1999-12-31", "2010-10-10;2011-11-11"},
        "city": {"rome", "paris", "london"},
        "level": ["500", "850", "1000"],
        "param": ["Z", "T"],
        "step": ["24", "36", "48"],
        "number": ["1", "2", "3"]
    }
    :type: dict[str, set[Any]]:

    :param valid_combinations: a list of dictionaries representing
    all valid combinations for a specific dataset
    e.g. valid_combinations = [{
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
        "date": ['1990-01-01;1999-12-31'],
        "param": ['T'],
        "level": ['850'],
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
    return get_possible_values(possible_selections, current_selection, valid_combinations)


def get_possible_values1(
    possible_selections: Dict[str, Set[Any]],
    current_selection: Dict[str, Set[Any]],
    valid_combinations: List[Dict[str, Set[Any]]],
) -> Dict[str, List[Any]]:
    """Works only for enumerated fields, i.e. fields with values
     that must be selected one by one (no ranges).
    Checks the current selection against all valid combinations.
    A combination is valid if every field contains
    at least one value from the current selection.
    If a combination is valid, its values are added to the pool
    of valid values (i.e. those that can still be selected without
    running into an invalid request).

    :param possible_selections: a dict of all selectable fields and values
    e.g. possible_selections = {
        "level": ["500", "850", "1000"],
        "param": ["Z", "T"],
        "step": ["24", "36", "48"],
        "number": ["1", "2", "3"]
    }
    :type: dict[str, set[Any]]:

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
        "param": ["T"],
        "level": ["850", "500"],
        "step": ["36"]
    }
    :type: dict[str, set[Any]]:

    :rtype: Dict[str, Set[Any]]
    :return: a dictionary containing all possible values,
    i.e. those that can still be selected without running into an invalid request
    e.g. {'level': {'500', '850'}, 'param': {'T', 'Z'}, 'step': {'24', '36', '48'}}

    """
    result: Dict[str, Set[Any]] = {}
    for valid_combination in valid_combinations:
        ok = True
        for field_name, selected_values in current_selection.items():
            if field_name in valid_combination.keys():
                if len(set(selected_values) & valid_combination[field_name]) == 0:
                    ok = False
                    break
        if ok:
            for field_name, valid_values in valid_combination.items():
                current = result.setdefault(field_name, set())
                current |= set(valid_values)
    if result:
        result.update(get_always_valid_params(possible_selections, valid_combinations))
    return {k: list(v) for (k, v) in result.items()}


def get_possible_values(
    possible_selections: Dict[str, Set[Any]],
    current_selection: Dict[str, Set[Any]],
    valid_combinations: List[Dict[str, Set[Any]]],
) -> Dict[str, List[Any]]:
    """Works only for enumerated fields, i.e. fields with values
     that must be selected one by one (no ranges).
    Checks the current selection against all valid combinations.
    A combination is valid if every field contains
    at least one value from the current selection.
    If a combination is valid, its values are added to the pool
    of valid values (i.e. those that can still be selected without
    running into an invalid request).

    :param possible_selections: a dict of all selectable fields and values
    e.g. possible_selections = {
        "level": ["500", "850", "1000"],
        "param": ["Z", "T"],
        "step": ["24", "36", "48"],
        "number": ["1", "2", "3"]
    }
    :type: dict[str, set[Any]]:

    :param valid_combinations: a list of dictionaries representing
    all valid combinations for a specific dataset
    e.g. valid_combinations = [
        {"level": {"500"}, "param": {"Z", "T"}, "step": {"24", "36", "48"}},
        {"level": {"1000"}, "param": {"Z"}, "step": {"24", "48"}},
        {"level": {"850"}, "param": {"T"}, "step": {"36", "48"}},
    ]
    :type: list[dict[str, set[Any]]]:

    :param current_selection: a dictionary containing the current selection
    e.g. current_selection = {
        "param": ["T"],
        "level": ["850", "500"],
        "step": ["36"]
    }
    :type: dict[str, set[Any]]:

    :rtype: Dict[str, Set[Any]]
    :return: a dictionary containing all possible values,
    i.e. those that can still be selected without running into an invalid request
    e.g. {'level': {'500', '850'}, 'param': {'T', 'Z'}, 'step': {'24', '36', '48'}}

    """
    result: Dict[str, Set[Any]] = {}
    for name in possible_selections:
        sub_selection = current_selection.copy()
        if name in sub_selection:
            sub_selection.pop(name)
        sub_results = get_possible_values1(
            possible_selections, sub_selection, valid_combinations
        )
        result[name] = sub_results[name]
    return result


def get_always_valid_params(
        possible_selections: Dict[str, Set[Any]],
        valid_combinations: List[Dict[str, Set[Any]]],
) -> Dict[str, Set[Any]]:
    result: Dict[str, Set[Any]] = {}
    for field_name, field_values in possible_selections.items():
        if field_name not in valid_combinations[0].keys():
            result.setdefault(field_name, field_values)
    return result
