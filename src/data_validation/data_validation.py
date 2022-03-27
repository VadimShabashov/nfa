from functools import reduce
from typing import Dict, Any, Optional
from src.data_validation.single_automata_validator import automata_validator
from src.data_validation.types.Result import Result
from src.data_validation.types.Validator import \
    Validator, all_of, combine_results, sequential
import networkx as nx

KEYWORDS = {'union', 'concat', 'diff', 'intersect', 'star'}


def __dependency_graph(data: Dict[str, Any]) -> nx.DiGraph:
    '''
    Строит граф зависимостей по файлу с автоматами
    '''
    edges = []

    for name, value in data.items():
        if isinstance(value, list):
            for e in value:
                if isinstance(e, str) and e not in KEYWORDS:
                    edges.append((name, e))

    return nx.DiGraph(edges)


def __has_cyclic_dependency(g: nx.DiGraph) -> bool:
    for _ in nx.simple_cycles(g):
        return True

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
                # Начинается с ключевого слова
                if isinstance(value[0], str) and value[0] in KEYWORDS:
                    errors.append(f'Sequence cannot starts with {value[0]}')

                # Заканчивается ключевым словом
                if isinstance(value[-1], str) and value[-1] in KEYWORDS:
                    errors.append(f'Sequence cannot ends with {value[0]}')

                for idx in range(len(value) - 1):
                    if (
                        # Два ключевых слова подряд
                        (
                            isinstance(value[idx], str)
                            and isinstance(value[idx + 1], str)
                            and value[idx] in KEYWORDS
                            and value[idx + 1] in KEYWORDS
                        )
                        # Два имени автомата подряд
                        or (
                            isinstance(value[idx], str)
                            and isinstance(value[idx + 1], str)
                            and value[idx] in automata_names
                            and value[idx + 1] in automata_names
                        )
                        # Два анонимных автомата подряд
                        or (
                            isinstance(value[idx], dict)
                            and isinstance(value[idx + 1], dict)
                        )
                        # Имя автомата, а потом анонимный автомат
                        or (
                            isinstance(value[idx], dict)
                            and isinstance(value[idx + 1], str)
                            and value[idx + 1] in automata_names
                        )
                        # Анонимный автомат, а затем имя автомата
                        or (
                            isinstance(value[idx], str)
                            and isinstance(value[idx + 1], dict)
                            and value[idx] in automata_names
                        )
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
        return Result.ok(None) \
            if not __has_cyclic_dependency(__dependency_graph(data)) \
            else Result.error('Cycle dependency found')

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


def validate(data: Dict[str, Any]) -> Optional[str]:
    '''
    Запускает валидации на полученном объекте
    и возвращает None или сообщение об ошибке
    '''
    r = __automata_object_validator().validate(data)

    return None if r.is_ok() else r.get_error()
