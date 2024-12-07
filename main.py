import json
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def create_id():

    id_list = []

    ps1 = [random.choice(letters) for _ in range(3)]
    ps2 = [random.choice(symbols) for _ in range(2)]
    ps3 = [random.choice(numbers) for _ in range(3)]

    id_list += ps1 + ps2 + ps3

    random.shuffle(id_list)
    id = "B_" + "".join(id_list)
    return id



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


BookShelf = []

if __name__=='__main__':

    while True:
        option = input("Welcome to online book system. Please choose an option:\n1) Add a book\n2) Delete a book\n3) Search for books\n4) Show all books\n5) Change status of a book  \n6) Exit\n")

        if option == '1':
            id = create_id()
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            year = input("Enter book year: ")
            status = input("Enter book status: ")
            newBook = Book(id, title, author, year, status)

            try:
                with open("Concole Version/data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("Concole Version/data.json", "w") as file:
                    json.dump(newBook, file, indent=4, default=lambda o: o.__dict__())
            else:
                is_new = True

                for key,value in data.items():
                    if title == value['title'] and author == value['author']:
                        r = input("Such author and book title already exist in our system!\nDo you want to update existing book? [y/n] ")
                        if r=='y':
                            value['year'] = year
                            value['status'] = status
                            print("Successfully updated the book!")
                        is_new = False

                        if BookShelf:
                            for book in BookShelf:
                                if book.id == key:
                                    BookShelf.remove(book)
                                    BookShelf.append(Book.deserialize(key, value))


                if is_new:
                    data.update(newBook.__dict__())
                    if BookShelf:
                        BookShelf.append(newBook)
                    print("Successfully added new book!")

                with open("Concole Version/data.json", "w") as file:
                    json.dump(data, file, indent=4)




        elif option == '2':
            id_to_delete = input("Enter book id: ")
            with open("Concole Version/data.json", "r") as file:
                data = json.load(file)

            if id_to_delete in data:
                del data[id_to_delete]

                with open("Concole Version/data.json", "w") as file:
                    json.dump(data, file, indent=4)

                if BookShelf:
                    for book in BookShelf:
                        if book.id == id_to_delete:
                            BookShelf.remove(book)
                            break

                print("Successfully deleted book!")

            else:
                print("Book not found!")


        elif option == '3':
            s = input("Введите название, автора или год издания книги: ")
            results = []

            if not BookShelf:
                with open("Concole Version/data.json", "r") as file:
                    books = json.load(file)

                for key,value in books.items():
                    BookShelf.append(Book.deserialize(key, value))

            for book in BookShelf:
                if book.id == s or book.title == s or book.author == s or book.year == s:
                    results.append(book)

            if not results:
                print("Book not found!")
                continue

            for book in results:
                print(book)


        elif option == '4':
            if BookShelf:
                for index, book in enumerate(BookShelf, start=1):
                    print(f'{index}) {book}')
            else:
                with open("Concole Version/data.json", "r") as file:
                    books = json.load(file)

                for key,value in books.items():
                    BookShelf.append(Book.deserialize(key, value))

                for index, book in enumerate(BookShelf, start=1):
                    print(f'{index}) {book}')

        elif option == '5':
            id_to_update = input("Enter book id: ")

            with open("Concole Version/data.json", "r") as file:
                data = json.load(file)


            if id_to_update in data:
                new_status = input("Enter new status: ")
                data[id_to_update]['status'] = new_status

                with open("Concole Version/data.json", "w") as file:
                    json.dump(data, file, indent=4)

                for book in BookShelf:
                    if book.id == id_to_update:
                        BookShelf.remove(book)
                        BookShelf.append(Book.deserialize(id_to_update, data[id_to_update]))
                        break

                print("Successfully updated a book!")

            else:
                print("Book not found!")


        elif option == '6':
            break
