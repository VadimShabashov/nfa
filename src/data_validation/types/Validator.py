from __future__ import annotations
from typing import Callable, Generic, Iterable, TypeVar
from .Result import Result

INPUT_TYPE = TypeVar('INPUT_TYPE')


class Validator(Generic[INPUT_TYPE]):
    '''
    Тип-обёртка над валидирующей функцией
    '''
    def __init__(
        self,
        f: Callable[[INPUT_TYPE], Result[None, str]]
    ) -> None:
        self.__f = f

    def validate(self, input: INPUT_TYPE) -> Result[None, str]:
        return self.__f(input)

    @classmethod
    def combine_log(cls, log: Iterable[str]) -> Result[None, str]:
        return Result.ok(None) \
            if len(log) == 0 \
            else Result.error('\n'.join(log))


def all_of(
    validators: Iterable[Validator[INPUT_TYPE]]
) -> Validator[INPUT_TYPE]:
    '''
    Принимает на вход список валидаторов, запускает их все
    и объединяет лог ошибок
    '''
    def inner(input: INPUT_TYPE) -> Result[None, str]:
        log = []

        for v in validators:
            r = v.validate(input)

            if r.is_error():
                log.append(r.get_error())

        return Validator.combine_log(log)

    return Validator(inner)


def sequential(
    validators: Iterable[Validator[INPUT_TYPE]]
) -> Validator[INPUT_TYPE]:
    '''
    Принимает на вход список валидаторов и падает с ошибкой первого же упавшего
    '''
    def inner(input: INPUT_TYPE) -> Result[None, str]:
        for v in validators:
            r = v.validate(input)

            if r.is_error():
                return r

        return r

    return Validator(inner)


def combine_results(
    acc: Result[None, str],
    val: Result[None, str]
) -> Result[None, str]:
    if acc.is_error() and val.is_error():
        return Result.error(acc.get_error() + '\n' + val.get_error())

    if acc.is_error():
        return acc

    if val.is_error():
        return val

    return Result.ok(None)
