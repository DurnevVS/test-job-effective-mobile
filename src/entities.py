from dataclasses import dataclass
from enum import Enum


class BookStatus(Enum):
    IN_STOCK = 'в наличии'
    GONE = 'выдана'


@dataclass
class Book:
    title: str
    author: str
    year: int
    status: BookStatus = BookStatus.IN_STOCK

    
