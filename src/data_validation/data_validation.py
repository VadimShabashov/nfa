from functools import reduce
from typing import Dict, Any, Set
from src.data_validation.single_automata_validator import automata_validator
from src.data_validation.types.Result import Result
from src.data_validation.types.Validator import \
    Validator, all_of, combine_results, sequential

KEYWORDS = {'union', 'concat', 'diff', 'intersect', 'star'}


def __dependency_graph(data: Dict[str, Any]) -> Dict[str, Set[str]]:
    '''
    Строит граф зависимостей по файлу с автоматами
    '''
    g = {name: set() for name in data.keys()}

    for name, value in data.items():
        if isinstance(value, list):
            for e in value:
                if isinstance(e, str) and e not in KEYWORDS:
                    g[name].add(e)

    return g


def __has_cyclic_dependency(
    from_: str,
    visited: Set[str],
    g: Dict[str, Set[str]]
) -> bool:
    '''
    Реализация DFS проверяющая наличие циклов в графе
    '''
    visited.add(from_)

    for n in g[from_]:
        if n in visited:
            return True
        else:
            return __has_cyclic_dependency(n, visited, g)

    return False


def __all_explicitly_specified_automata_validator() \
        -> Validator[Dict[str, Any]]:
    '''
    Проверяет все автоматы, которые объявлены в файле явно
    (не через набор операций)
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        automata_list = []

        for value in data.values():
            if isinstance(value, dict):
                automata_list.append(value)
            elif isinstance(value, list):
                for e in value:
                    if isinstance(value, dict):
                        automata_list.append(value)

        return reduce(
            combine_results,
            [automata_validator().validate(a) for a in automata_list],
            Result.ok(None)
        )

    return Validator(inner)


def __all_names_valid_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет, что все использованные имена
    либо являются зарезервированными словами для операций
    либо именами объявленных в файле автоматов
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        errors = []
        automata_names = data.keys()

        for name, value in data.items():
            if name in KEYWORDS:
                return errors.append(f'Automata name cannot be in ${KEYWORDS}')

            if isinstance(value, list):
                for e in value:
                    if isinstance(e, str):
                        if e not in automata_names and e not in KEYWORDS:
                            errors.append(f'Name {e} not presented in file')

        return Validator.combine_log(errors)

    return Validator(inner)


def __string_tokens_in_correct_sequence_validator() \
        -> Validator[Dict[str, Any]]:
    '''
    Проверяет последовательность всех строковых токенов в файле.
    Запрещает последовательно идущие операции или автоматы.
    Запрещает операции в начале или конце последовательности
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        errors = []
        automata_names = data.keys()

        for value in data.values():
            if isinstance(value, list):
                if isinstance(value[0], str) and value[0] in KEYWORDS:
                    errors.append(f'Sequence cannot starts with {value[0]}')

                if isinstance(value[-1], str) and value[-1] in KEYWORDS:
                    errors.append(f'Sequence cannot ends with {value[0]}')

                for idx in range(len(value) - 1):
                    if (
                        isinstance(value[idx], str)
                        and isinstance(value[idx + 1], str)
                        and ((
                                value[idx] in KEYWORDS
                                and value[idx + 1] in KEYWORDS
                            )
                            or (
                                value[idx] in automata_names
                                and value[idx + 1] in automata_names
                        ))
                    ):
                        errors.append(
                            f'{value[idx]} and {value[idx + 1]} '
                            'cannot follow in sequence'
                        )

        return Validator.combine_log(errors)

    return Validator(inner)


def __no_cyclic_dependencies_validator() -> Validator[Dict[str, any]]:
    '''
    Проверяет отсутствие циклических зависимостей между автоматами
    '''
    def inner(data: Dict[str, Any]) -> Result[None, str]:
        g = __dependency_graph(data)
        visited = set()

        for v in g.keys():
            if v not in visited:
                r = __has_cyclic_dependency(v, visited, g)

                if r:
                    return Result.error('Cyclic dependency found')

        return Result.ok(None)

    return Validator(inner)


def __automata_object_validator() -> Validator[Dict[str, Any]]:
    '''
    Проверяет валидность всего объекта с автоматами
    '''
    return sequential([
        all_of([
            __all_explicitly_specified_automata_validator(),
            __all_names_valid_validator(),
            __string_tokens_in_correct_sequence_validator()
        ]),
        __no_cyclic_dependencies_validator()
    ])


def validate(data: Dict[str, Any]) -> None | str:
    '''
    Запускает валидации на полученном объекте
    и возвращает None или сообщение об ошибке
    '''
    r = __automata_object_validator().validate(data)

    return None if r.is_ok() else r.get_error()
