from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar
from uuid import UUID

_T = TypeVar("_T")


class BaseService(ABC, Generic[_T]):
    @abstractmethod
    def get_by_id(self, _id: UUID) -> _T | None:
        raise NotImplementedError()

    @abstractmethod
    def get_list(self, params: dict) -> Sequence[_T]:
        raise NotImplementedError()

    @abstractmethod
    def create(self, entity: _T) -> _T:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: _T) -> _T:
        raise NotImplementedError()

    @abstractmethod
    def delete_by_id(self, _id: UUID) -> None:
        raise NotImplementedError()
