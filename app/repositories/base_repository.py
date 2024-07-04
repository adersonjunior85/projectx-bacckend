from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

_T = TypeVar("_T")


class BaseRepository(ABC, Generic[_T]):
    """
    Abstract generic Repository
    """

    @abstractmethod
    def create(self, entity: _T) -> _T:
        raise NotImplementedError()

    @abstractmethod
    def get_list(self, params: dict) -> Sequence[_T]:
        raise NotImplementedError()

    @abstractmethod
    def get_by_id(self, id_: int) -> _T | None:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: _T) -> _T:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, id_: int) -> _T:
        raise NotImplementedError()
