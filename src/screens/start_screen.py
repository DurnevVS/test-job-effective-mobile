from ast import literal_eval

from src.entities import Book
from src.serializers import BookSerializer
from src.data import DBManager
from src.data.db import JsonDataBase

from .screen import Screen, Command


def get_db() -> DBManager:
    return DBManager(
        db=JsonDataBase('books.json'),
        serializer=BookSerializer()
    )


class StartScreen(Screen):

    @property
    def commands(self) -> list[Command]:
        return [
            AddCommand('add', 'add', 'Добавляет книгу', self.context),
            DelCommand('del', 'del', 'Удаляет книгу', self.context),
            AllCommand('all', 'all', 'Показывает все книги', self.context),
            FindCommand('find', 'find', 'Найти книги', self.context),
            UpdateCommand('update', 'update', 'Редактирует книгу', self.context),
            ExitCommand('exit', 'exit', 'Выйти из программы', self.context)
        ]


class ExitCommand(Command):
    '''Команда завершения работы программы'''

    def execute(self, user_input: str):
        exit(0)


class AddCommand(Command):
    '''Команда добавления книги'''

    def execute(self, user_input: str):
        print(f'Заполните поля для добавления книги:')
        book = Book(
            title=input('Название: '),
            author=input('Автор: '),
            year=int(input('Год: ')),
        )
        db = get_db()
        db.save(book)
        print('Книга добавлена')
        return StartScreen()


class AllCommand(Command):
    '''Команда показа всех книг'''

    def execute(self, user_input: str):
        db = get_db()
        [print(f'{book.id}. {book}') for book in db.all()]
        return StartScreen()


class DelCommand(Command):
    '''Команда удаления книги'''

    def execute(self, user_input: str):
        db = get_db()
        id_ = int(input(f'Введите id книги, чтобы удалить:'))
        try:
            book = db.get(id=id_)
            db.delete(book)
            print('Книга удалена')
        except KeyError:
            print('Книга не найдена')
        return StartScreen()


class FindCommand(Command):
    '''Команда поиска книги'''

    def execute(self, user_input: str):
        db = get_db()
        prompt = (
            f"Введите параметры для поиска в python dict формате('key': value)\n"
            f"Если параметров несколько, запишите их через запятую('key': value, 'key': 'value')\n"
            f'Доступные параметры:\n'
            f'{[var for var in Book.__dataclass_fields__]}\n')

        kwargs = literal_eval('{' + input(prompt) + '}')
        try:
            book = db.get(**kwargs)
            print(book)
            print('Эта книга?')
        except KeyError:
            print('Книга не найдена')
        return StartScreen()


class UpdateCommand(Command):
    '''Команда редактирования книги'''

    def execute(self, user_input: str):
        db = get_db()
        id_ = int(input(f'Введите id книги, для её изменения:'))
        try:
            book = db.get(id=id_)
            prompt = (
                f"Введите параметры для изменения в python dict формате('key': value)\n"
                f"Если параметров несколько, запишите их через запятую('key': value, 'key': 'value')\n"
                f'Доступные параметры:\n'
                f'{[var for var in Book.__dataclass_fields__]}\n')
            kwargs = literal_eval('{' + input(prompt) + '}')

            db.update(book, **kwargs)
            print('Книга обновлена')
        except KeyError:
            print('Книга не найдена')
        return StartScreen()
