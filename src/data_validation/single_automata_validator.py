from typing import Any, Dict
from .types.Result import Result
from .types.Validator import Validator, all_of, sequential


def __check_duplicates(lst):
    set_lst = set()
    set_duplicates = set()

    for item in lst:
        if item in set_lst:
            set_duplicates.add(item)
        else:
            set_lst.add(item)

    return set_duplicates, set_lst


def __check_keys_match(test_set, correct_set):
    extra_fields = test_set.difference(correct_set)
    required_fields = correct_set.difference(test_set)

    return extra_fields, required_fields


def __check_keys_subset(test_set, correct_set):
    diff_set = test_set.difference(correct_set)

    return diff_set


def __automata_structure_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет структуру файла.
    Все нужные поля присутствуют и нет лишних
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        correct_keys = {
            "glossary",
            "states",
            "initial_state",
            "terminal_states",
            "is_dfa", "edges",
            "edges_epsilon"
        }
        extra_keys, missed_keys = __check_keys_match(
            set(data.keys()),
            correct_keys
        )

        if len(extra_keys) == 0 and len(missed_keys) == 0:
            return Result.ok(None)
        else:
            return Result.error(
                f"Wrong fields in data: unknown fields {extra_keys}, "
                f"missing fields {missed_keys}"
            )

    return Validator(inner)


def __states_duplication_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет отсутствие дубликатов в списке состояний
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        states_duplicates, _ = __check_duplicates(data["states"])

        if len(states_duplicates) == 0:
            return Result.ok(None)
        else:
            return Result.error(
                f"Duplication of states for {states_duplicates}"
            )

    return Validator(inner)


def __initial_state_in_states_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет наличие начального состояния в списке состояний
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        if data['initial_state'] in data['states']:
            return Result.ok(None)
        else:
            return Result.error(
                f"Initial state {data['initial_state']} is not in states"
            )

    return Validator(inner)


def __duplicates_in_terminals_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет отсутствие дубликатов в списке терминалов
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        terminal_states_duplicates, _ = __check_duplicates(
            data["terminal_states"]
        )

        if len(terminal_states_duplicates) == 0:
            return Result.ok(None)
        else:
            return Result.error(
                "Duplication of terminal states for "
                f"{terminal_states_duplicates}"
            )

    return Validator(inner)


def __terminal_states_in_states_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет, что все терминальные состояния содержатся в списке состояний
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        diff_terminal_states = __check_keys_subset(
            set(data['terminal_states']),
            set(data['states'])
        )

        if len(diff_terminal_states) == 0:
            return Result.ok(None)
        else:
            return Result.error(
                f"States {diff_terminal_states} of terminal states"
                " are not in states"
            )

    return Validator(inner)


def __terminal_states_validator() -> Validator[Dict[str, Any]]:
    '''
    Выполняет валидацию терминальных состояний
    '''
    return all_of([
        __duplicates_in_terminals_validator(),
        __terminal_states_in_states_validator()
    ])


def __duplicates_in_glossary_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет отсутствие дубликатов в алфавите
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        glossary_duplicates, _ = __check_duplicates(data["glossary"])

        if len(glossary_duplicates) == 0:
            return Result.ok(None)
        else:
            return Result.error(
                f"Duplication of symbols in glossary for {glossary_duplicates}"
            )

    return Validator(inner)


def __all_states_presented_in_edges_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет наличие всех состояний и отсутствие лишних в списке переходов
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        extra_keys_edges, required_keys_edges = \
            __check_keys_match(set(data["edges"].keys()), set(data['states']))

        if len(extra_keys_edges) == 0 and len(required_keys_edges) == 0:
            return Result.ok(None)
        else:
            return Result.error(
                f"Set of edges keys doesn't equal set of states: "
                f"unknown fields {extra_keys_edges}, "
                f"missing fields {required_keys_edges}"
            )

    return Validator(inner)


def __duplications_in_edges_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет отсутствие дубликатов в списке переходов
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        errors = []

        for start_state, edges in data["edges"].items():
            set_edges = set()
            set_symbols = set()

            for end_state, edge in edges:
                if end_state not in data['states']:
                    errors.append(
                        f"State {end_state} in edges "
                        f"(for {start_state}: ({end_state}, {edge})) "
                        "is not in states"
                    )

                if edge not in data['glossary']:
                    errors.append(
                        f"Edge {edge} in edges "
                        f"(for {start_state}: ({end_state}, {edge})) "
                        "is not in glossary"
                    )

                if (end_state, edge) in set_edges:
                    errors.append(
                        f"Duplication of edge {start_state}: "
                        f"({end_state}, {edge}) in edges"
                    )
                else:
                    set_edges.add((end_state, edge))

                if data["is_dfa"] and (edge in set_symbols):
                    errors.append(
                        f"Multiple edges '{edge}' "
                        f"were specified for {start_state} in DFA."
                    )
                else:
                    set_symbols.add(edge)

        return Validator.combine_log(errors)

    return Validator(inner)


def __edges_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет валидность рёбер.
    '''
    return all_of([
        __all_states_presented_in_edges_validator(),
        __duplications_in_edges_validator()
    ])


def __all_states_presented_in_epsilon_edges_validator() \
        -> Validator[Dict[str, Any]]:
    '''
    Проверяет наличие всех состояний в списке рёбер с эпсилон-переходами
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        extra_keys_epsilon_edges, required_keys_epsilon_edges = \
            __check_keys_match(
                set(data["edges_epsilon"].keys()),
                set(data['states'])
            )

        if (
            len(extra_keys_epsilon_edges) == 0
                and len(required_keys_epsilon_edges) == 0
        ):
            return Result.ok(None)
        else:
            return Result.error(
                f"Set of epsilon edges keys doesn't equal set of states: "
                f"unknown keys {extra_keys_epsilon_edges}, "
                f"missing keys {required_keys_epsilon_edges}"
            )

    return Validator(inner)


def __duplications_in_epsilon_edges_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет наличие дубликатов в рёбрах с эпсилон-переходами
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        errors = []

        for start_state, edges in data["edges_epsilon"].items():
            if data["is_dfa"] and edges:
                errors.append("Epsilon edges can not be specified for DFA.")
                break
            else:
                edges_duplicate, set_edges = __check_duplicates(edges)

                if len(edges_duplicate) > 0:
                    errors.append(
                        "Duplication of epsilon edges for "
                        f"{start_state}: {edges_duplicate}"
                    )

                diff_epsilon_edges = __check_keys_subset(
                    set_edges,
                    set(data['states'])
                )

                if len(diff_epsilon_edges) > 0:
                    errors.append(
                        f"States {diff_epsilon_edges} for {start_state} "
                        "in epsilon edges are not in states"
                    )

        return Validator.combine_log(errors)

    return Validator(inner)


def __epsilon_edges_validator() -> Validator[Dict[str, Any]]:
    '''
    Валидирует рёбра с эписилон переходами
    '''
    return all_of([
        __all_states_presented_in_epsilon_edges_validator(),
        __duplications_in_epsilon_edges_validator()
    ])


def automata_validator() -> Validator[Dict[str, Any]]:
    '''
    Валидирует один автомат
    '''
    return sequential([
        __automata_structure_validator(),
        all_of([
            __states_duplication_validator(),
            __initial_state_in_states_validator(),
            __terminal_states_validator(),
            __duplicates_in_glossary_validator(),
            __edges_validator(),
            __epsilon_edges_validator()
        ])
    ])
