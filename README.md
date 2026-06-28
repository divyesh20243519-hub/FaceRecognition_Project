# Face Recognition Attendance System

This project is an automated attendance system for classrooms that uses face recognition to identify students and record their attendance. The system captures facial data, trains a K-Nearest Neighbors (KNN) classifier, recognizes students in real time through a webcam, and stores attendance records in CSV format.

A simple Streamlit dashboard is also included to view attendance records for a particular day.

---

## Features

* Register new students by capturing face images
* Train a face recognition model using KNN
* Real-time face recognition through a webcam
* Automatically record attendance with date and time
* Store attendance in CSV files
* View attendance records using a Streamlit interface
* Voice confirmation when attendance is marked

---

## Technologies Used

* Python
* OpenCV
* Scikit-learn
* NumPy
* Pandas
* Streamlit
* Pickle
* Haar Cascade Classifier

---

## Project Structure

```text
.
├── Attendance/
│   └── Attendance_YYYY-MM-DD.csv
├── Data/
│   ├── Faces/
│   ├── faces_data.pkl
│   ├── names.pkl
│   └── haarcascade_frontalface_default.xml
├── app.py
├── add_faces.py
├── attendance.py
└── background.png
```

---

## Installation

Clone the repository.

```bash
git clone https://github.com/yourusername/face-recognition-attendance.git

cd face-recognition-attendance
```

Install the required packages.

```bash
pip install -r requirements.txt
```

---

## How the System Works

### 1. Register a Student

The system captures 100 images of a student's face through the webcam. These images are resized, flattened, and stored for training.

### 2. Train the Model

The collected face data and corresponding names are used to train a K-Nearest Neighbors (KNN) classifier.

### 3. Mark Attendance

When the attendance program starts, the webcam detects faces in real time. If a registered student is recognized, their name is displayed on the screen. Pressing **O** records their attendance along with the current date and time.

### 4. View Attendance

Attendance records are saved as CSV files and can be viewed through the Streamlit dashboard.

---

## Attendance Format

Each attendance file contains:

| Name  | Date       | Time     |
| ----- | ---------- | -------- |
| Alice | 2026-06-28 | 09:05:13 |
| Bob   | 2026-06-28 | 09:06:42 |

---

## Running the Project

### Register a Student

```bash
python add_faces.py
```

### Start Attendance

```bash
python attendance.py
```

### Open the Dashboard

```bash
streamlit run app.py
```

---

## Notes

This project was built to explore computer vision and machine learning by solving a practical classroom problem. It combines OpenCV for face detection, a KNN classifier for face recognition, and Streamlit for displaying attendance records in a simple interface.
