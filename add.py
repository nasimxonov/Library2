from PyQt5.QtWidgets import *
from db import get_connection


class AddWindow(QDialog):
    def __init__(self, main_window, book=None):
        super().__init__()
        self.main_window = main_window
        self.book = book

        self.setWindowTitle("Add Book" if not book else "Update Book")

        form_layout = QFormLayout()

        self.name = QLineEdit(self)
        self.author = QLineEdit(self)
        self.page_count = QLineEdit(self)

        if book:
            self.name.setText(book[1])
            self.author.setText(book[2])
            self.page_count.setText(str(book[3]))

        form_layout.addRow("Nomi:", self.name)
        form_layout.addRow("Avtori:", self.author)
        form_layout.addRow("Sahifa soni:", self.page_count)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.rejected.connect(self.cancel_window)
        buttons.accepted.connect(self.save_data)

        form_layout.addRow(buttons)
        self.setLayout(form_layout)

    def cancel_window(self):
        self.close()

    def save_data(self):
        name = self.name.text()
        author = self.author.text()
        page_count = self.page_count.text()

        conn = get_connection()
        conn.autocommit = True
        with conn.cursor() as cursor:
            if self.book:
                cursor.execute("UPDATE books SET name=%s, author=%s, page_count=%s WHERE id=%s",
                               (name, author, page_count, self.book[0]))
            else:
                cursor.execute("INSERT INTO books (name, author, page_count) VALUES (%s, %s, %s)",
                               (name, author, page_count))
            self.main_window.load_data()
            self.close()
