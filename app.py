import streamlit as st
import pandas as pd
import datetime
import time

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

df = pd.read_csv('../Attendance/Attendance_' + date + '.csv')

st.dataframe(df.style.highlight_max(axis=0))

# streamlit run app.py

# RUN THIS IN TERMINAL TO LAUNCH THE APP.
