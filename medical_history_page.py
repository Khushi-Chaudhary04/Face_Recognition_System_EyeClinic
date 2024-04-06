import mysql.connector
from display_details import PatientDetailsGUI
import tkinter as tk
class DatabaseHandler:
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()

    def fetch_data(self, registrations_id):
        # Fetch details from registrations table
        self.cursor.execute(
            "SELECT * FROM registrations WHERE id =%s", (registrations_id,))
        # Assuming there's only one record with the given registrations_id
        registration_data = self.cursor.fetchone()

        # Fetch details from medical_history table based on registrations_id
        self.cursor.execute(
            "SELECT * FROM medical_history WHERE id =%s", (registrations_id,))
        medical_history_data = self.cursor.fetchall()

        return registration_data, medical_history_data

    def close_connection(self):
        if self.conn:
            self.conn.close()


# if __name__ == "__main__":
#     # Assuming you pass global_name from another Python file
#     global_name = "chirag dulera"  # Example name

#     # Initialize and connect to the database
#     db_handler = DatabaseHandler(
#         host="localhost", user="root", password="root", database="clinic")
#     db_handler.connect()

#     # Fetch data based on global_name
#     if global_name:
#         db_handler.cursor.execute(
#             "SELECT id FROM registrations WHERE name=%s", (global_name,))
#         # Assuming there's only one record with the given name
#         registrations_id = db_handler.cursor.fetchone()[0]
#         registration_data, medical_history_data = db_handler.fetch_data(
#             registrations_id)
        
#         root = tk.Tk()
#         PatientDetailsGUI(root,registration_data,medical_history_data)
#     # Close connection
#     db_handler.close_connection()
#     root.mainloop()
