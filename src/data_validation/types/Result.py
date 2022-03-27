from __future__ import annotations
from typing import Generic, TypeVar

R = TypeVar('R')
E = TypeVar('E')


class Result(Generic[R, E]):
    '''
    Результат какой-то операции, которая может завершиться с ошибкой
    '''
    __token = object()

    def __init__(self, token: object, value: R | E, is_ok: bool) -> None:
        assert token is self.__token,\
            'Result can be created through `ok` and `error` methods only'

        self.__is_ok = is_ok
        self.__value = value

    @classmethod
    def ok(cls, val: R) -> Result[R, E]:
        return Result(cls.__token, val, True)

    @classmethod
    def error(cls, e: E) -> Result[R, E]:
        return Result(cls.__token, e, False)

    def is_ok(self) -> bool:
        return self.__is_ok

    def is_error(self) -> bool:
        return not self.__is_ok

    def get_result(self) -> R:
        assert self.is_ok()

        return self.__value

    def get_error(self) -> E:
        assert self.is_error()

        return self.__value
