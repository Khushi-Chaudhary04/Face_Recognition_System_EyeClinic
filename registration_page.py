import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import cv2
import os
from medical_registration import MedicalRegistrations


class RegistrationPage(tk.Toplevel):
    def __init__(self, parent, db_connection):
        super().__init__(parent)

        self.title("New Registration")
        self.geometry("420x520")
        self.configure(bg='#333333')

        self.db_connection = db_connection
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self, bg='#333333')

        # Create labels and entry fields for registration information
        name_label = tk.Label(frame, text="Name:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.name_entry = tk.Entry(frame, font=("Arial", 12))

        age_label = tk.Label(frame, text="Age:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.age_entry = tk.Entry(frame, font=("Arial", 12))

        gender_label = tk.Label(frame, text="Gender:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.gender_entry = tk.Entry(frame, font=("Arial", 12))

        phone_label = tk.Label(frame, text="Phone No:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.phone_entry = tk.Entry(frame, font=("Arial", 12))

        email_label = tk.Label(frame, text="Email:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.email_entry = tk.Entry(frame, font=("Arial", 12))

        address_label = tk.Label(frame, text="Address:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.address_entry = tk.Entry(frame, font=("Arial", 12))

        self.photo_label = tk.Label(frame, text="Photo:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))

        self.photo_button = ttk.Button(frame, text="Capture Photo", command=self.capture_photo)

        self.save_button = ttk.Button(frame, text="Save", command=self.save_registration)

        # Placing widgets on the screen
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        age_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.gender_entry.grid(row=2, column=1, padx=10, pady=5)

        phone_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.phone_entry.grid(row=3, column=1, padx=10, pady=5)

        email_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        address_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.address_entry.grid(row=5, column=1, padx=10, pady=5)

        self.photo_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.photo_button.grid(row=6, column=1, padx=10, pady=5)

        self.save_button.grid(row=7, columnspan=2, pady=10)

        frame.pack(padx=20, pady=20)

    def capture_photo(self):
        # Capture photo using camera when space bar is pressed
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Capture Photo")
        img_counter = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture photo")
                break
            cv2.imshow("Capture Photo", frame)
            k = cv2.waitKey(1)

            if k % 256 == 27:
                # ESC pressed
                messagebox.showinfo("Info", "Photo capture cancelled")
                break
            elif k % 256 == 32:
                # SPACE pressed
                self.captured_photo = frame  # Store captured photo
                messagebox.showinfo("Success", "Photo captured")
                break

        cam.release()
        cv2.destroyAllWindows()

    def save_registration(self):
        # Get registration information from entry fields
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        phone_no = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        # Define the dataset directory path
        dataset_dir = "dataset"
        # Create the dataset directory if it doesn't exist
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)

        # Check if all fields are filled and photo is captured
        if name and age and gender and phone_no and email and address and self.captured_photo is not None:
            # Define the path for saving the photo
            photo_path = os.path.join(dataset_dir, f"{name}.jpg")

            # Save the captured photo to the defined path
            cv2.imwrite(photo_path, self.captured_photo)

            # Prepare the photo path to be stored in the database
            # This is the relative path, adjust if necessary for your DB
            photo_path_for_db = photo_path

            # Save registration data and photo path to MySQL database
            cursor = self.db_connection.cursor()
            query = "INSERT INTO registrations (name, age, gender, phone_no, email, address, photo_path) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (name, age, gender, phone_no,
                        email, address, photo_path_for_db)

            cursor.execute(query, values)
            self.db_connection.commit()
            cursor.close()

            # Redirect to MedicalRegistrationsPage upon successful registration
            self.destroy()
            MedicalRegistrations(self.master, self.db_connection)

        else:
            messagebox.showerror(
                "Error", "Please fill in all fields and capture a photo.")


class MedicalRegistrationsPage(tk.Toplevel):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.title("Medical Registrations")
        self.geometry("400x300")

        # Add your UI elements for displaying medical registrations here
        self.label = tk.Label(self, text="Medical Registrations")
        self.label.pack(pady=10)

        self.close_button = ttk.Button(
            self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)


# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="clinic"
)
