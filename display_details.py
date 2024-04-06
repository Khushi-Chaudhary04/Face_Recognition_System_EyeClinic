import tkinter as tk
import mysql.connector
from update_patients import UpdatePatientDetailsWindow
from update_medical_history import UpdateMedicalHistoryWindow

class PatientDetailsGUI:
    def __init__(self, master, registration_data, medical_history_data):
        self.master = master
        self.master.title("Patient Details")
        self.master.configure(bg='#333333')
        self.master.geometry("900x800")  # Increased window size
        self.registration_data = registration_data
        self.medical_history_data = medical_history_data
        self.create_widgets()

    def create_widgets(self):
        # Registration Details Frame
        registration_frame = tk.Frame(
            self.master, bg='#333333', padx=20, pady=20)
        registration_frame.grid(row=0, column=0, padx=20, pady=20)

        tk.Label(registration_frame, text="Patient Details", font=(
            "Arial", 20, "bold"), bg='#333333', fg="#FFFFFF").grid(row=0, columnspan=2, pady=10)

        labels = ["ID", "Name", "Age", "Gender",
                    "Phone Number", "Email", "Address"]
        for i, label in enumerate(labels):
            tk.Label(registration_frame, text=label, bg='#333333', fg="#FFFFFF", font=(
                "Arial", 14)).grid(row=i+1, column=0, padx=10, sticky="w")
            tk.Label(registration_frame, text=self.registration_data[i], bg='#333333', fg="#FFFFFF", font=(
                "Arial", 14)).grid(row=i+1, column=1, padx=10, sticky="w")

        # Medical History Frame
        medical_history_frame = tk.Frame(
            self.master, bg='#333333', padx=20, pady=20)
        medical_history_frame.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(medical_history_frame, text="Medical History", font=(
            "Arial", 20, "bold"), bg='#333333', fg="#FFFFFF").grid(row=0, columnspan=2, pady=10)

        tk.Label(medical_history_frame, text="Diagnosis", bg='#333333', fg="#FFFFFF", font=(
            "Arial", 14)).grid(row=1, column=0, padx=10, sticky="w")
        tk.Label(medical_history_frame, text=self.medical_history_data[0], bg='#333333', fg="#FFFFFF", font=(
            "Arial", 14)).grid(row=1, column=1, padx=10, sticky="w")

        tk.Label(medical_history_frame, text="Prescription", bg='#333333', fg="#FFFFFF", font=(
            "Arial", 14)).grid(row=2, column=0, padx=10, sticky="w")
        tk.Label(medical_history_frame, text=self.medical_history_data[1], bg='#333333', fg="#FFFFFF", font=(
            "Arial", 14)).grid(row=2, column=1, padx=10, sticky="w")

        tk.Label(medical_history_frame, text="Visit Date", bg='#333333', fg="#FFFFFF", font=(
            "Arial", 14)).grid(row=3, column=0, padx=10, sticky="w")
        tk.Label(medical_history_frame, text=self.medical_history_data[2], bg='#333333', fg="#FFFFFF", font=(
            "Arial", 14)).grid(row=3, column=1, padx=10, sticky="w")

        # Buttons Frame
        buttons_frame = tk.Frame(self.master, bg='#333333')
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)

        # Update Patient Details Button
        update_patient_button = tk.Button(
            buttons_frame, text="Update Patient Details", font=("Arial", 12), command=self.update_patient_details)
        update_patient_button.pack(side="left", padx=10)

        # Update Medical History Button
        update_medical_button = tk.Button(
            buttons_frame, text="Update Medical History", font=("Arial", 12), command=self.update_medical_history)
        update_medical_button.pack(side="left", padx=10)

        # Add to Queue Button
        add_to_queue_button = tk.Button(
            buttons_frame, text="Add to Queue", font=("Arial", 12), command=self.add_to_queue)
        add_to_queue_button.pack(side="left", padx=10)

    def update_patient_details(self):
        # Print patient's ID
        patient_id = self.registration_data[0]
        print("Patient ID:", patient_id)
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="clinic"
        )
        update_window = UpdatePatientDetailsWindow(db_connection,patient_id)
        self.master.destroy()
        

        

    def update_medical_history(self):
        # Implement update medical history functionality
        patient_id = self.registration_data[0]
        print("Update Medical History button clicked")
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="clinic"
        )
        update_medical = UpdateMedicalHistoryWindow(db_connection,patient_id)
        
        self.master.destroy()

    def add_to_queue(self):
        # Implement add to queue functionality
        print("Add to Queue button clicked")

