from tkinter import Label, Button, Frame

class AccountsView:
    def __init__(self, root, show_login_view, username):
      self._root = root
      self._show_login_view = show_login_view
      self._frame = Frame(self._root)
      self._username = username

    def start(self):
        default_label = Label(self._frame, text= f"You are logged in as {self._username}", font=("Arial", 24, "bold"), bg="lightgreen")
        logout_button = Button(self._frame, text= "Logout", command=self._show_login_view)

        default_label.grid(row=0, column=0, columnspan=2, pady=30)
        logout_button.grid(row=1, column=0, pady=10)

        self._frame.pack()

    def destroy(self):
        self._frame.destroy()

