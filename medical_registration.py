import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime


class MedicalRegistrations(tk.Toplevel):
    def __init__(self, parent, db_connection):
        super().__init__(parent)

        self.title("Medical History")
        self.geometry("400x350")
        self.configure(bg='#333333')

        self.db_connection = db_connection
        self.setup_ui()

    def setup_ui(self):
        frame = tk.Frame(self, bg='#333333')

        # Labels and Entry fields for medical history information
        diagnosis_label = tk.Label(
            frame, text="Diagnosis:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.diagnosis_entry = tk.Entry(frame, font=("Arial", 12))

        prescription_label = tk.Label(
            frame, text="Prescription:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.prescription_entry = tk.Entry(frame, font=("Arial", 12))

        visit_date_label = tk.Label(
            frame, text="Visit Date:", bg='#333333', fg="#FFFFFF", font=("Arial", 12))
        self.visit_date_entry = tk.Entry(frame, font=("Arial", 12))
        self.visit_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.save_button = ttk.Button(
            frame, text="Save", command=self.save_medical_history)

        # Placing widgets on the screen
        diagnosis_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.diagnosis_entry.grid(row=0, column=1, padx=10, pady=5)

        prescription_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.prescription_entry.grid(row=1, column=1, padx=10, pady=5)

        visit_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.visit_date_entry.grid(row=2, column=1, padx=10, pady=5)

        self.save_button.grid(row=4, columnspan=2, pady=10)

        frame.pack(padx=20, pady=20)

    def save_medical_history(self):
        # Retrieve medical history information from entry fields
        diagnosis = self.diagnosis_entry.get()
        prescription = self.prescription_entry.get()
        visit_date = self.visit_date_entry.get()

        # Check if all fields are filled
        if diagnosis and prescription and visit_date:
            try:
                # Insert patient into the database and retrieve the last inserted patient ID
                cursor = self.db_connection.cursor()

                # Fetch the last inserted ID from the registrations table
                cursor.execute(
                    "SELECT id FROM registrations ORDER BY id DESC LIMIT 1")
                # Fetch the last inserted ID from the registrations table
                last_inserted_id = cursor.fetchone()[0]

                history_query = "INSERT INTO medical_history (id, diagnosis, prescription, visit_date) VALUES (%s, %s, %s, %s)"
                history_values = (last_inserted_id, diagnosis,
                                  prescription, visit_date)
                cursor.execute(history_query, history_values)

                self.db_connection.commit()
                cursor.close()

                messagebox.showinfo(
                    "Success", "Medical history saved successfully!")
                self.destroy()  # Close the medical history window after saving
            except mysql.connector.Error as err:
                messagebox.showerror(
                    "Error", f"Error saving medical history: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")


# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="clinic"
)

