from PyQt5.QtWidgets import *
from db import get_connection
from add import AddWindow


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library2")
        vertical = QVBoxLayout()

        buttons_layout = QHBoxLayout()

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_book)

        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self.update_book)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_book)

        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.update_btn)
        buttons_layout.addWidget(self.delete_btn)

        self.list_widget = QListWidget()
        self.load_data()

        vertical.addLayout(buttons_layout)
        vertical.addWidget(self.list_widget)
        self.setLayout(vertical)

    def load_data(self):
        self.list_widget.clear()
        conn = get_connection()
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM books")
            books = cursor.fetchall()

        for book in books:
            text = f"{book[0]}. {book[1]}, {book[2]}, {book[3]}"
            self.list_widget.addItem(QListWidgetItem(text))

    def add_book(self):
        add_window = AddWindow(self)
        add_window.exec_()

    def update_book(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            book_id = int(selected_item.text().split(".")[0])
            conn = get_connection()
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM books WHERE id=%s", (book_id,))
                book = cursor.fetchone()
            if book:
                add_window = AddWindow(self, book)
                add_window.exec_()

    def delete_book(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            book_id = int(selected_item.text().split(".")[0])
            conn = get_connection()
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
            self.load_data()


app = QApplication([])
window = Window()
window.show()

app.exec_()
