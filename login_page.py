import tkinter as tk
from tkinter import ttk, messagebox
from main_window import MainWindow
from registration_page import RegistrationPage


class LoginPage:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.title("Login")
        self.setup_login_window()

    def setup_login_window(self):
        self.login_window.geometry('500x500')
        self.login_window.configure(bg='#333333')

        frame = tk.Frame(self.login_window, bg='#333333')

        # Creating widgets
        login_label = tk.Label(frame, text="Login",
                                bg='#333333', fg="#FF3399", font=("Arial", 30))
        username_label = tk.Label(
            frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        self.username_entry = tk.Entry(frame, font=("Arial", 16))
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 16))
        password_label = tk.Label(
            frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
        login_button = ttk.Button(frame, text="Login", command=self.login)

        # Placing widgets on the screen
        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
        username_label.grid(row=1, column=0)
        self.username_entry.grid(row=1, column=1, pady=20)
        password_label.grid(row=2, column=0)
        self.password_entry.grid(row=2, column=1, pady=20)
        login_button.grid(row=3, column=0, columnspan=2, pady=30)

        frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" and password == "":
            messagebox.showinfo(title="Login Success",
                                message="You successfully logged in.")
            self.open_main_window()
        else:
            messagebox.showerror(
                title="Error", message="Invalid username or password")

    def open_main_window(self):
        self.login_window.withdraw()
        main_window = MainWindow(self.login_window)
        main_window.show()

    def run(self):
        self.login_window.mainloop()
