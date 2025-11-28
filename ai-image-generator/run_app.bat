@echo off
REM Activate virtual environment
call .venv\Scripts\activate

REM Navigate to project root
cd /d E:\ai-image-generator

REM Launch Streamlit app
streamlit run ui_streamlit.py

REM Keep window open after exit
pause