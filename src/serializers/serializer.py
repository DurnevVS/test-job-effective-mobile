from abc import ABC, abstractmethod
from dataclasses import is_dataclass, asdict
from enum import Enum
from typing import TYPE_CHECKING, Any

from src.entities import Book

if TYPE_CHECKING:
    from _typeshed import DataclassInstance


class ExpectedDataClassException(Exception):
    def __init__(self, obj: Any):
        super().__init__(f'Expected dataclass, but got {obj.__class__}')


class Serializer(ABC):

    @abstractmethod
    def serialize(self, obj: Any) -> Any:
        pass

    @abstractmethod
    def deserialize(self, obj: Any) -> Any:
        pass


class JsonSerializer(Serializer):

    def asdict_factory(self, data):
        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return dict((k, convert_value(v)) for k, v in data)

    def serialize(self, obj: 'DataclassInstance') -> dict[str, Any]:

        if not is_dataclass(obj):
            raise ExpectedDataClassException(obj)

        return asdict(obj, dict_factory=self.asdict_factory)


class BookSerializer(JsonSerializer):

    def deserialize(self, obj: dict[str, Any]) -> 'DataclassInstance':
        id = obj.pop('id')
        book = Book(**obj)
        book.id = id
        return book
