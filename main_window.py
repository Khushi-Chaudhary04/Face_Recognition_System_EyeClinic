import tkinter as tk
from tkinter import ttk, messagebox
from registration_page import RegistrationPage
from face_recognizer import FaceRecognizer
import mysql

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="clinic"
)

class MainWindow:
    def __init__(self, parent):
        self.parent = parent
        self.main_window = tk.Toplevel(self.parent)
        self.main_window.title("Clinic Management System")
        self.main_window.geometry("600x400")
        self.main_window.configure(bg='#333333')

        # Initialize registration data
        self.registration_data = []

        self.setup_main_window()

    def setup_main_window(self):
        frame = tk.Frame(self.main_window, bg='#333333')

        # Creating widgets
        title_label = tk.Label(frame, text="Hospital Management System", bg='#333333', fg="#FF3399", font=("Arial", 24))
        registration_button = ttk.Button(frame, text="New Registration", command=self.open_registration)
        medical_history_button = ttk.Button(frame, text="Get Medical History With Face Recognition", command=self.open_medical_history)
        # queue_management_button = ttk.Button(frame, text="Queue Management", command=self.open_queue_management)

        # Placing widgets on the screen
        title_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=20)
        registration_button.grid(row=1, column=0, columnspan=2, pady=10, padx=50, ipadx=20)
        medical_history_button.grid(row=2, column=0, columnspan=2, pady=10, padx=50, ipadx=20)
        # queue_management_button.grid(row=3, column=0, columnspan=2, pady=10, padx=50, ipadx=20)

        frame.pack()

    def open_registration(self):
        registration_window = RegistrationPage(self.main_window, db_connection)

    def open_medical_history(self):
        image_directory = "dataset"
        recognizer = FaceRecognizer(image_directory)
        recognizer.recognize_faces()
        recognizer.run()

    # def open_queue_management(self):
    #     queue_management_window = QueueManagementWindow(
    #         self.main_window, self.registration_data)
    #     queue_management_window.grab_set()  # Make the queue management window modal
    #     self.main_window.wait_window(queue_management_window)

    def show(self):
        self.main_window.mainloop()

