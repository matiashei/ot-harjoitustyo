from tkinter import Label, Entry, Button, Frame
from src.db import get_database_connection
from src.repositories.user_repository import UserRepository
from src.services.user_services import UserService

class RegisterView:
    def __init__(self, root, show_login_view):
        self._root = root
        self._show_login_view = show_login_view
        self._frame = Frame(self._root)
        connection = get_database_connection()
        user_repository = UserRepository(connection)
        self._user_service = UserService(user_repository)
        self._username_entry = None
        self._password_entry = None
        self._password_confirm_entry = None
        self._status_label = None


    def start(self):
        register_label = Label(self._frame, text="Register", font=("Arial", 24, "bold"), bg="lightgreen")
        username_label = Label(self._frame, text="Username")
        self._username_entry = Entry(self._frame)
        password_label = Label(self._frame, text="Password")
        self._password_entry = Entry(self._frame, show="*")
        password_confirm_label = Label(self._frame, text="Confirm password")
        self._password_confirm_entry = Entry(self._frame, show="*")
        self._status_label = Label(self._frame, text="", fg="red")
        submit_button = Button(self._frame, text="Submit", command=self.register)
        login_view_button = Button(self._frame, text="Login", command=self._show_login_view)

        register_label.grid(row=0, column=0, columnspan=2, pady=30)
        username_label.grid(row=1, column=0)
        self._username_entry.grid(row=1, column=1, pady=5)
        password_label.grid(row=2, column=0, pady=5)
        self._password_entry.grid(row=2, column=1)
        password_confirm_label.grid(row=3, column=0, pady=5)
        self._password_confirm_entry.grid(row=3, column=1)
        self._status_label.grid(row=4, column=0, columnspan=3)
        submit_button.grid(row=5, column=1, pady=10)
        login_view_button.grid(row=5, column=2, pady=10)

        self._frame.pack()

    def destroy(self):
        self._frame.destroy()

    def register(self):
        username = self._username_entry.get().strip()
        password = self._password_entry.get()
        password_confirm = self._password_confirm_entry.get()

        if not username or not password:
            self._status_label.config(text="Username and password are required")
            return

        if password != password_confirm:
            self._status_label.config(text="Passwords do not match")
            return

        if self._user_service.find_user_by_username(username):
            self._status_label.config(text="Username already exists")
            return

        self._user_service.create_user(username, password)
        self._show_login_view()