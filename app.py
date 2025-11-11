import streamlit as st
import pandas as pd
import datetime
import time

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

df = pd.read_csv('C:/Users/divye/OneDrive/Desktop/FaceRecognitionProject/Attendance/Attendance_' + date + '.csv') # depending on the date

st.dataframe(df.style.highlight_max(axis=0))

# streamlit run c:/Users/divye/OneDrive/Desktop/FaceRecognitionProject/Data/app.py

# RUN THIS IN TERMINAL TO LAUNCH THE APP.
