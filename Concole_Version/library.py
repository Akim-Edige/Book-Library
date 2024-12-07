import json
import os
import random

DATA_FILE = "books.json"


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

class Book():
    def __init__(self, id, title, author, year, status):

        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f'Book id: {self.id} \ntitle: {self.title} \nauthor: {self.author} \nyear: {self.year} \nstatus: {self.status}\n'

    def __dict__(self):
        return {self.id: {'title': self.title, 'author': self.author, 'year': self.year, 'status': self.status}}

    @classmethod
    def deserialize(cls, id, data):
        return cls(id, data['title'], data['author'], data['year'], data['status'])


class Library:
    def __init__(self):
        self.data_file = DATA_FILE
        self.book_shelf = []


    def _generate_id(self):
        """
        Генерирует уникальный идентификатор для новой книги.
        """

        id_list = []

        ps1 = [random.choice(letters) for _ in range(3)]
        ps2 = [random.choice(symbols) for _ in range(2)]
        ps3 = [random.choice(numbers) for _ in range(3)]

        id_list += ps1 + ps2 + ps3

        random.shuffle(id_list)
        id = "B_" + "".join(id_list)
        return id

    # def _save_books(self):
    #     """
    #     Сохраняет книги в JSON файл.
    #     """
    #     with open(self.data_file, 'w', encoding='utf-8') as f:
    #         json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)


    def add_book(self, title: str, author: str, year: int) -> Book:
        """
        Добавляет новую книгу в библиотеку.
        """
        new_book = Book(title=title, author=author, year=year, id=self._generate_id(), status='В наличии')

        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_book, file, indent=4, default=lambda o: o.__dict__())
        else:
            is_new = True

            for key, value in data.items():
                if title == value['title'] and author == value['author']:
                    r = input(
                        "Such author and book title already exist in our system!\nDo you want to update existing book? [y/n] ")
                    if r == 'y':
                        value['year'] = year
                        print("Successfully updated the book!")
                    is_new = False

                    if self.book_shelf:
                        for book in self.book_shelf:
                            if book.id == key:
                                self.book_shelf.remove(book)
                                self.book_shelf.append(Book.deserialize(key, value))

            if is_new:
                data.update(new_book.__dict__())
                if self.book_shelf:
                    self.book_shelf.append(new_book)

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

        return new_book


    def remove_book(self, book_id: int) -> bool:
        """
        Удаляет книгу по ее идентификатору.
        """
        with open("data.json", "r") as file:
            data = json.load(file)

        if book_id in data:
            del data[book_id]

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

            if self.book_shelf:
                for book in self.book_shelf:
                    if book.id == book_id:
                        self.book_shelf.remove(book)
                        break

            return True
        else:
            return False

    def search_books(self, s:str):
        """
        Ищет книги по заданным критериям.
        """
        results = []

        if not self.book_shelf:
            with open("data.json", "r") as file:
                books = json.load(file)

            for key, value in books.items():
                self.book_shelf.append(Book.deserialize(key, value))

        for book in self.book_shelf:
            if book.id == s or book.title == s or book.author == s or book.year == s:
                results.append(book)

        return results


    def display_books(self):
        """
        Возвращает список всех книг.
        """
        if not self.book_shelf:
            with open("data.json", "r") as file:
                books = json.load(file)

            for key, value in books.items():
                self.book_shelf.append(Book.deserialize(key, value))

        return self.book_shelf

    def update_status(self, book_id:str, new_status: str) -> bool:
        """
        Обновляет статус книги.
        """

        if new_status not in ["в наличии", "выдана"]:
            raise ValueError("Недопустимый статус книги.")

        with open("data.json", "r") as file:
            data = json.load(file)

        if book_id in data:
            data[book_id]['status'] = new_status

            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

            for book in self.book_shelf:
                if book.id == book_id:
                    self.book_shelf.remove(book)
                    self.book_shelf.append(Book.deserialize(book_id, data[book_id]))
                    break
            return True
        else:
            return False

