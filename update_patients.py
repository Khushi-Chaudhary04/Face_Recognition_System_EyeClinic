import tkinter as tk
from tkinter import messagebox
import mysql.connector


class UpdatePatientDetailsWindow:
    def __init__(self, db_connection, patient_id):
        self.db_connection = db_connection
        self.patient_id = patient_id

        self.window = tk.Toplevel()
        self.window.title("Update Patient Details")
        self.window.geometry("400x300")
        self.window.configure(bg='#333333')

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.window, bg='#333333')

        # Labels
        labels = ["Name", "Age", "Gender", "Phone Number", "Email", "Address"]
        self.entry_vars = []
        for i, label in enumerate(labels):
            tk.Label(frame, text=label, bg='#333333', fg="#FFFFFF", font=(
                "Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry_var = tk.StringVar()
            entry = tk.Entry(frame, textvariable=entry_var, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.entry_vars.append(entry_var)

        # Fetch and fill existing details
        existing_details = self.fetch_existing_details()
        if existing_details:
            for entry_var, detail in zip(self.entry_vars, existing_details):
                entry_var.set(detail)

        # Submit Button
        submit_button = tk.Button(frame, text="Update", bg="#FF3399", fg="#FFFFFF", font=(
            "Arial", 12), command=self.update_details)
        submit_button.grid(row=len(labels), columnspan=2, pady=10)

        frame.pack(padx=20, pady=20)

    def fetch_existing_details(self):
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT name, age, gender, phone_no , email, address FROM registrations WHERE id = %s"
            cursor.execute(query, (self.patient_id,))
            existing_details = cursor.fetchone()
            cursor.close()
            return existing_details
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error", f"Error fetching existing details: {err}")
            return None

    def update_details(self):
        name, age, gender, phone_number, email, address = [
            entry_var.get() for entry_var in self.entry_vars]
        try:
            cursor = self.db_connection.cursor()
            query = "UPDATE registrations SET name = %s, age = %s, gender = %s, phone_no = %s, email = %s, address = %s WHERE id = %s"
            cursor.execute(query, (name, age, gender, phone_number,
                                    email, address, self.patient_id))
            self.db_connection.commit()
            cursor.close()
            messagebox.showinfo(
                "Success", "Patient details updated successfully.")
            self.window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror(
                "Error", f"Error updating patient details: {err}")


# # Example usage:
# # Replace 'localhost', 'root', 'root', 'clinic' with your actual database connection details
# db_connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="clinic"
# )