# book_library.py

class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_lent = False

    def lend(self):
        if self.is_lent:
            raise Exception("Book is already lent out.")
        self.is_lent = True

    def return_book(self):
        if not self.is_lent:
            raise Exception("Book is not lent.")
        self.is_lent = False

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class EBook(Book):
    def __init__(self, title, author, isbn, size_mb):
        super().__init__(title, author, isbn)
        self.size_mb = size_mb

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.size_mb} MB (eBook)"

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        # prevent duplicate ISBN
        for b in self.books:
            if b.isbn == book.isbn:
                raise Exception("ISBN already exists.")
        self.books.append(book)

    def lend_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.lend()
                return
        raise Exception("Book not found.")

    def return_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.return_book()
                return
        raise Exception("Book not found.")

    def remove_book(self, isbn):
        self.books = [b for b in self.books if b.isbn != isbn]

    def update_book(self, isbn, title=None, author=None, size_mb=None):
        for book in self.books:
            if book.isbn == isbn:
                if title:
                    book.title = title
                if author:
                    book.author = author
                if isinstance(book, EBook) and size_mb is not None:
                    book.size_mb = size_mb
                return
        raise Exception("Book not found.")

    def books_by_author(self, author):
        return [b for b in self.books if b.author.lower() == author.lower()]

    def get_all_books(self):
        return self.books
