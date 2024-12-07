from library import Library

def print_menu():
    """
    Выводит меню доступных операций.
    """
    print("\n--- Меню библиотеки ---")
    print("1. Добавить книгу")
    print("2. Удалить книгу")
    print("3. Найти книгу")
    print("4. Отобразить все книги")
    print("5. Изменить статус книги")
    print("6. Выйти")

def get_int_input(prompt):
    """
    Получает целочисленный ввод от пользователя.
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Пожалуйста, введите целое число.")



if __name__ == "__main__":
    library = Library()

    while True:
        print_menu()
        choice = input("Выберите опцию: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            year = get_int_input("Enter book year: ")
            new_book = library.add_book(title, author, year)
            print(f"Книга добавлена с ID: {new_book.id}")


        elif choice == '2':
            book_id = input("Введите ID книги для удаления: ")
            if library.remove_book(book_id):
                print("Книга успешно удалена.")
            else:
                print("Книга с таким ID не найдена.")

        elif choice == '3':
            print("Поиск книги:")
            search = input("Введите название, автора или год издания книги): ")
            results = library.search_books(search)

            if results:
                print(f"Найдено {len(results)} книга(и):")
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == '4':
            books = library.display_books()
            if books:
                print(f"Всего книг: {len(books)}")
                print("_________________________")
                for index, book in enumerate(books, start=1):
                    print(f'{index}) {book}')
            else:
                print("В библиотеке нет книг.")

        elif choice == '5':
            book_id = input("Введите ID книги для изменения статуса: ")
            new_status = input("Введите новый статус ('в наличии' или 'выдана'): ").strip().lower()
            try:
                if library.update_status(book_id, new_status):
                    print("Статус книги обновлен.")
                else:
                    print("Книга с таким ID не найдена.")
            except ValueError as ve:
                print(ve)

        elif choice == '6':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
