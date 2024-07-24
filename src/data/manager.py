from abc import ABC, abstractmethod
from typing import Any

from src.serializers import Serializer


class DataBase(ABC):

    @abstractmethod
    def all(self) -> list[Any]:
        pass

    @abstractmethod
    def get(self, **kwargs) -> Any | None:
        pass

    @abstractmethod
    def save(self, obj: Any) -> None:
        pass

    @abstractmethod
    def delete(self, obj: Any) -> None:
        pass

    @abstractmethod
    def update(self, obj: Any) -> None:
        pass


class DBManager(DataBase):

    def __init__(self, db: DataBase, serializer: Serializer):
        self.db = db
        self.serializer = serializer

    def all(self) -> list[Any]:
        all_ = self.db.all()
        return [self.serializer.deserialize(obj) for obj in all_]

    def get(self, **kwargs) -> Any | None:
        return self.serializer.deserialize(self.db.get(**kwargs))

    def save(self, obj: Any) -> None:
        self.db.save(self.serializer.serialize(obj))

    def delete(self, obj: Any) -> None:
        self.db.delete(self.serializer.serialize(obj))

    def update(self, obj: Any, /, **kwargs) -> None:
        serialized = self.serializer.serialize(obj)
        self.db.update(serialized, **kwargs)
