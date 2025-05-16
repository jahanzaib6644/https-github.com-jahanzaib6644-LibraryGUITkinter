import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog
)
from book_library import Book, EBook, Library

class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.library = Library()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Library Management System - PyQt5")
        self.setGeometry(100, 100, 700, 500)

        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QGridLayout()
        btn_layout = QHBoxLayout()

        # Form elements
        self.title_label = QLabel("Title:")
        self.title_input = QLineEdit()

        self.author_label = QLabel("Author:")
        self.author_input = QLineEdit()

        self.isbn_label = QLabel("ISBN:")
        self.isbn_input = QLineEdit()

        self.ebook_checkbox = QCheckBox("eBook?")
        self.ebook_checkbox.stateChanged.connect(self.toggle_ebook_size)

        self.size_label = QLabel("Download Size (MB):")
        self.size_input = QLineEdit()
        self.size_input.setEnabled(False)

        # Add widgets to form layout
        form_layout.addWidget(self.title_label, 0, 0)
        form_layout.addWidget(self.title_input, 0, 1)

        form_layout.addWidget(self.author_label, 1, 0)
        form_layout.addWidget(self.author_input, 1, 1)

        form_layout.addWidget(self.isbn_label, 2, 0)
        form_layout.addWidget(self.isbn_input, 2, 1)

        form_layout.addWidget(self.ebook_checkbox, 3, 1)
        form_layout.addWidget(self.size_label, 4, 0)
        form_layout.addWidget(self.size_input, 4, 1)

        # Buttons
        self.add_btn = QPushButton("Add Book")
        self.add_btn.clicked.connect(self.add_book)

        self.lend_btn = QPushButton("Lend Book")
        self.lend_btn.clicked.connect(self.lend_book)

        self.return_btn = QPushButton("Return Book")
        self.return_btn.clicked.connect(self.return_book)

        self.remove_btn = QPushButton("Remove Book")
        self.remove_btn.clicked.connect(self.remove_book)

        self.view_author_btn = QPushButton("View Books by Author")
        self.view_author_btn.clicked.connect(self.view_books_by_author)

        self.back_btn = QPushButton("Show All Books")
        self.back_btn.clicked.connect(self.update_book_table)
        self.back_btn.setVisible(False)  # hidden initially

        self.update_btn = QPushButton("Update Book by ISBN")
        self.update_btn.clicked.connect(self.update_book)

        # Add buttons to button layout
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.lend_btn)
        btn_layout.addWidget(self.return_btn)
        btn_layout.addWidget(self.remove_btn)
        btn_layout.addWidget(self.update_btn)

        # Book Table
        self.book_table = QTableWidget()
        self.book_table.setColumnCount(4)
        self.book_table.setHorizontalHeaderLabels(["Title", "Author", "ISBN", "Download Size (MB)"])
        self.book_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Add widgets to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.back_btn)
        main_layout.addWidget(QLabel("Library Inventory:"))
        main_layout.addWidget(self.book_table)

        self.setLayout(main_layout)

        self.update_book_table()

    def toggle_ebook_size(self):
        checked = self.ebook_checkbox.isChecked()
        self.size_input.setEnabled(checked)
        if not checked:
            self.size_input.clear()

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        isbn = self.isbn_input.text().strip()
        is_ebook = self.ebook_checkbox.isChecked()
        size_text = self.size_input.text().strip()

        if not title or not author or not isbn:
            QMessageBox.warning(self, "Input Error", "Title, Author, and ISBN are required.")
            return

        if is_ebook:
            if not size_text:
                QMessageBox.warning(self, "Input Error", "Download size is required for eBooks.")
                return
            if not size_text.isdigit():
                QMessageBox.warning(self, "Input Error", "Download size must be a number.")
                return
            size_mb = int(size_text)
            book = EBook(title, author, isbn, size_mb)
        else:
            book = Book(title, author, isbn)

        try:
            self.library.add_book(book)
            QMessageBox.information(self, "Success", f"Book '{title}' added.")
            self.clear_inputs()
            self.update_book_table()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def lend_book(self):
        isbn, ok = QInputDialog.getText(self, "Lend Book", "Enter ISBN:")
        if ok and isbn:
            try:
                self.library.lend_book(isbn)
                QMessageBox.information(self, "Success", "Book lent successfully.")
                self.update_book_table()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def return_book(self):
        isbn, ok = QInputDialog.getText(self, "Return Book", "Enter ISBN:")
        if ok and isbn:
            try:
                self.library.return_book(isbn)
                QMessageBox.information(self, "Success", "Book returned successfully.")
                self.update_book_table()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def remove_book(self):
        isbn, ok = QInputDialog.getText(self, "Remove Book", "Enter ISBN:")
        if ok and isbn:
            self.library.remove_book(isbn)
            QMessageBox.information(self, "Success", "Book removed successfully.")
            self.update_book_table()

    def view_books_by_author(self):
        author, ok = QInputDialog.getText(self, "View Books by Author", "Enter author's name:")
        if ok and author:
            books = self.library.books_by_author(author)
            if not books:
                QMessageBox.information(self, "Info", f"No books found by author '{author}'.")
                return
            self.display_books(books)
            self.back_btn.setVisible(True)

    def update_book(self):
        isbn, ok = QInputDialog.getText(self, "Update Book", "Enter ISBN of book to update:")
        if not (ok and isbn):
            return

        # Check if book exists
        book_to_update = None
        for b in self.library.get_all_books():
            if b.isbn == isbn:
                book_to_update = b
                break
        if not book_to_update:
            QMessageBox.warning(self, "Error", "Book not found.")
            return

        # Get new title
        new_title, ok = QInputDialog.getText(self, "Update Book", "Enter new title (leave blank to keep current):")
        if not ok:
            return
        if not new_title.strip():
            new_title = None

        # Get new author
        new_author, ok = QInputDialog.getText(self, "Update Book", "Enter new author (leave blank to keep current):")
        if not ok:
            return
        if not new_author.strip():
            new_author = None

        # If ebook, get new size
        new_size = None
        if isinstance(book_to_update, EBook):
            new_size_str, ok = QInputDialog.getText(self, "Update Book", "Enter new download size in MB (leave blank to keep current):")
            if not ok:
                return
            if new_size_str.strip():
                if not new_size_str.isdigit():
                    QMessageBox.warning(self, "Error", "Download size must be a number.")
                    return
                new_size = int(new_size_str)

        try:
            self.library.update_book(isbn, title=new_title, author=new_author, size_mb=new_size)
            QMessageBox.information(self, "Success", "Book updated successfully.")
            self.update_book_table()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def clear_inputs(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.ebook_checkbox.setChecked(False)
        self.size_input.clear()

    def update_book_table(self):
        books = self.library.get_all_books()
        self.display_books(books)
        self.back_btn.setVisible(False)

    def display_books(self, books):
        self.book_table.setRowCount(len(books))
        for row, book in enumerate(books):
            self.book_table.setItem(row, 0, QTableWidgetItem(book.title))
            self.book_table.setItem(row, 1, QTableWidgetItem(book.author))
            self.book_table.setItem(row, 2, QTableWidgetItem(book.isbn))
            if isinstance(book, EBook):
                self.book_table.setItem(row, 3, QTableWidgetItem(str(book.size_mb)))
            else:
                self.book_table.setItem(row, 3, QTableWidgetItem("Physical"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())
