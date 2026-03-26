from tkinter import Label, Entry, Button, Frame
from db import get_database_connection
from repositories.user_repository import UserRepository
from services.user_services import UserService

class LoginView:
    def __init__(self, root, show_register_view, show_accounts_view):
        self._root = root
        self._show_register_view = show_register_view
        self._show_accounts_view = show_accounts_view
        self._frame = Frame(self._root)
        connection = get_database_connection()
        user_repository = UserRepository(connection)
        self._user_service = UserService(user_repository)
        self._username_entry = None
        self._password_entry = None
        self._status_label = None

    def start(self):
        login_label = Label(self._frame, text= "Login", font=("Arial", 24, "bold"), bg="lightgreen")
        username_label = Label(self._frame, text= "Username")
        self._username_entry = Entry(self._frame)
        password_label = Label(self._frame, text= "Password")
        self._password_entry = Entry(self._frame, show="*")
        self._status_label = Label(self._frame, text="", fg="red")
        submit_button = Button(self._frame, text= "Submit", command=self.login)
        register_button = Button(self._frame, text= "Register", command=self._show_register_view)

        login_label.grid(row=0, column=0, columnspan=2, pady=30)
        username_label.grid(row=1, column=0)
        self._username_entry.grid(row=1, column=1, pady=5)
        password_label.grid(row=2, column=0, pady=5)
        self._password_entry.grid(row=2, column=1)
        self._status_label.grid(row=3, column=0, columnspan=3)
        submit_button.grid(row=4, column=1, pady=10)
        register_button.grid(row=4, column=2, pady=10)

        self._frame.pack()

    def destroy(self):
        self._frame.destroy()

    def login(self):
        username = self._username_entry.get().strip()
        password = self._password_entry.get()

        if self._user_service.authenticate(username, password):
            self._show_accounts_view(username)
            return

        self._status_label.config(text="Invalid username or password")
