import face_recognition
import cv2
import os
import tkinter as tk
from medical_history_page import DatabaseHandler
from display_details import PatientDetailsGUI

global_name = None  # Global variable to store the recognized name


class FaceRecognizer:
    def __init__(self, dataset):
        self.dataset = dataset
        self.known_face_encodings = {}
        self.load_known_faces()
        self.root = tk.Tk()
        # self.root.title("Welcome")
        # self.label = tk.Label(self.root, text="")
        # self.label.pack()
        self.other_window = None

    def load_known_faces(self):
        def add_entries_from_directory(dataset):
            known_face_images = {}
            for root, dirs, files in os.walk(dataset):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')):
                        name = os.path.splitext(file)[0]
                        image_path = os.path.join(root, file)
                        known_face_images[name] = image_path
            return known_face_images

        known_face_images = add_entries_from_directory(self.dataset)

        for name, image_path in known_face_images.items():
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:
                self.known_face_encodings[name] = face_encodings
            else:
                print(f"No face detected in '{image_path}'")

    def create_other_window(self, name):
        global global_name
        global_name = name  # Store recognized name in the global variable

        

        # Fetch data from the database
        db_handler = DatabaseHandler(
            host="localhost", user="root", password="root", database="clinic")
        db_handler.connect()
        try:
            db_handler.cursor.execute(
                "SELECT * FROM registrations WHERE name=%s", (name,))
            registration_data = db_handler.cursor.fetchone()

            if registration_data:
                db_handler.cursor.execute(
                    "SELECT diagnosis,prescription,visit_date FROM medical_history WHERE id=%s", (registration_data[0],))
                medical_history_data = db_handler.cursor.fetchone()

                # Display patient details in the new window
                print("Registration Data:", registration_data)
                print("Medical History Data:", medical_history_data)

                app = PatientDetailsGUI(
                    self.root, registration_data, medical_history_data)
                
                
            else:
                print("No registration data found for the given name.")
        except Exception as e:
            print("Error fetching data from the database:", e)
        finally:
            db_handler.close_connection()

    def recognize_faces(self):
        global global_name 
        video_capture = cv2.VideoCapture(0)

        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(
                frame, face_locations)

            for face_encoding in face_encodings:
                match_name = "Match not Found Retry or Add New Data"

                for name, known_encodings in self.known_face_encodings.items():
                    for known_encoding in known_encodings:
                        match = face_recognition.compare_faces(
                            [known_encoding], face_encoding, tolerance=0.6)
                        if any(match):
                            match_name = name
                            break
                    if match_name != "Match not Found Retry or Add New Data":
                        break

                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top),
                                    (right, bottom), (0, 0, 255), 2)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, match_name, (left + 6,
                                                    bottom - 6), font, 0.5, (255, 255, 255), 1)

                if match_name != "Match not Found Retry or Add New Data":
                        global_name = match_name
                        self.create_other_window(match_name)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

    def run(self):
        pass
        print(global_name)
        


