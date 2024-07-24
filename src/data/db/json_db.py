import json
import os
from typing import Any
from src.data.manager import DataBase


class JsonDataBase(DataBase):

    def __init__(self, filepath: str):
        self.file = filepath
        if not os.path.exists(self.file):
            self._dump([])

    def _dump(self, obj_list: list[dict[str, Any]]):
        with open(self.file, 'w') as f:
            json.dump(obj_list, f, indent=4, ensure_ascii=False)

    def all(self) -> list[dict[str, Any]]:
        with open(self.file, 'r') as f:
            return json.load(f)

    def get(self, **kwargs) -> dict[str, Any]:
        all_ = self.all()
        for obj in all_:
            for k, v in kwargs.items():
                if obj[k] != v:
                    break
            else:
                return obj
        raise KeyError(f'Objects with {kwargs} not found')

    def save(self, obj: dict[str, Any]) -> None:
        all_ = self.all()
        obj['id'] = all_[-1]['id'] + 1 if all_ else 0
        all_.append(obj)
        self._dump(all_)

    def delete(self, obj: dict[str, Any]) -> None:
        all_ = self.all()
        to_delete = self.get(**obj)
        all_.remove(to_delete)
        self._dump(all_)

    def update(self, obj: dict[str, Any], /, **kwargs) -> None:
        all_ = self.all()
        to_update = self.get(**obj)
        all_.remove(to_update)
        for k, v in kwargs.items():
            print(k, v)
            to_update[k] = v
        all_.append(to_update)
        self._dump(all_)
