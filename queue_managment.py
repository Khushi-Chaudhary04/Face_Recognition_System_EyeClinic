import tkinter as tk
from tkinter import ttk
from collections import deque
from datetime import datetime, timedelta

class QueueManagement:
    def __init__(self):
        self.patient_queue = deque()
        self.doctor_assignments = {}  # Dictionary to track doctor-patient pairings
        self.appointment_times = {}  # Dictionary to track patient appointment times

    def add_patient(self, patient_name):
        appointment_time = datetime.now() + timedelta(minutes=len(self.patient_queue))
        self.patient_queue.append(patient_name)
        self.appointment_times[patient_name] = appointment_time
        print(f"{patient_name} added to queue. Current queue: {self.patient_queue}")

    def assign_doctor(self, doctor_name, specialty):
        if self.patient_queue:
            patient_name = self.patient_queue.popleft()  # FIFO dequeue
            self.doctor_assignments[patient_name] = (doctor_name, specialty)
            print(f"{patient_name} assigned to Dr. {doctor_name} ({specialty}).")
        else:
            print("No patients in queue.")

    def patient_leaving(self, patient_name):
        if patient_name in self.doctor_assignments:
            self.doctor_assignments.pop(patient_name)
            appointment_time = self.appointment_times.pop(patient_name)
            print(f"{patient_name} leaving. Appointment time: {appointment_time}.")
        else:
            print(f"{patient_name} not found in queue or already left.")

# Create an instance of the QueueManagement class
queue_manager = QueueManagement()

# Doctor and Specialty Data
doctors = {
    "Dr. Smith": ["Cataract", "Vision"],
    "Dr. Johnson": ["Glaucoma", "Retina"],
    "Dr. Williams": ["Cornea", "Pediatrics"]
}

# Function to update the specialty dropdown menu based on the selected doctor
def update_specialties(*args):
    selected_doctor = doctor_var.get()
    specialties = doctors[selected_doctor]
    specialty_dropdown['values'] = specialties
    specialty_dropdown.current(0)  # Set the default value

# Function to update the patient queue table
def update_queue_table():
    for row in queue_treeview.get_children():
        queue_treeview.delete(row)
    for patient, doctor_data in queue_manager.doctor_assignments.items():
        doctor_name, specialty = doctor_data
        appointment_time = queue_manager.appointment_times[patient]
        queue_treeview.insert('', 'end', values=(patient, doctor_name, specialty, appointment_time))

# Function to handle adding a patient
def add_patient():
    patient_name = patient_entry.get().strip()
    if patient_name:  # Check if the entry is not empty
        queue_manager.add_patient(patient_name)
        update_queue_table()
        patient_entry.delete(0, tk.END)  # Clear the entry field after adding patient

# Function to handle assigning a doctor
def assign_doctor():
    selected_doctor = doctor_var.get()
    selected_specialty = specialty_var.get()
    queue_manager.assign_doctor(selected_doctor, selected_specialty)
    update_queue_table()

# Function to handle patient leaving
def leave_patient():
    patient_name = patient_entry.get().strip()
    if patient_name:  # Check if the entry is not empty
        queue_manager.patient_leaving(patient_name)
        update_queue_table()
        patient_entry.delete(0, tk.END)  # Clear the entry field after patient leaves

# Create a Tkinter window
root = tk.Tk()
root.title("Queue Management System")

# Create labels and entry widgets for patient name input
patient_label = tk.Label(root, text="Patient Name:")
patient_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

patient_entry = tk.Entry(root, width=30)
patient_entry.grid(row=0, column=1, padx=10, pady=5)

# Create dropdown menus for selecting doctor and specialty
doctor_label = tk.Label(root, text="Doctor:")
doctor_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

doctor_var = tk.StringVar(root)
doctor_dropdown = ttk.Combobox(root, width=27, textvariable=doctor_var, state="readonly")
doctor_dropdown.grid(row=1, column=1, padx=10, pady=5)
doctor_dropdown['values'] = list(doctors.keys())
doctor_dropdown.current(0)
doctor_dropdown.bind("<<ComboboxSelected>>", update_specialties)  # Update specialties when doctor is selected

specialty_label = tk.Label(root, text="Specialty:")
specialty_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

specialty_var = tk.StringVar(root)
specialty_dropdown = ttk.Combobox(root, width=27, textvariable=specialty_var, state="readonly")
specialty_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Create buttons for adding patient, assigning doctor, and patient leaving
add_patient_button = tk.Button(root, text="Add Patient", command=add_patient)
add_patient_button.grid(row=0, column=2, padx=10, pady=5)

assign_doctor_button = tk.Button(root, text="Assign Doctor", command=assign_doctor)
assign_doctor_button.grid(row=3, column=0, columnspan=2, pady=5)

leave_patient_button = tk.Button(root, text="Leave Patient", command=leave_patient)
leave_patient_button.grid(row=3, column=2, padx=10, pady=5)

# Create a treeview for displaying the patient queue
queue_treeview = ttk.Treeview(root, columns=('Patient Name', 'Doctor', 'Specialty', 'Appointment Time'), show='headings')
queue_treeview.heading('Patient Name', text='Patient Name')
queue_treeview.heading('Doctor', text='Doctor')
queue_treeview.heading('Specialty', text='Specialty')
queue_treeview.heading('Appointment Time', text='Appointment Time')
queue_treeview.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

# Update the queue table initially
update_queue_table()

# Start the Tkinter event loop
root.mainloop()
