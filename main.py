from src.screens import StartScreen


# db = DBManager(
#     db=JsonDataBase('books.json'),
#     serializer=BookSerializer()
# )


def main():

    screen = StartScreen()
    screen.render()
    while True:
        user_input = input().strip().lower()

        if user_input in screen:
            screen = screen(user_input)
            screen.render()
        else:
            print('Такой команды нет')


if __name__ == "__main__":
    main()
