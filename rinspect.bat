@echo off
REM Rasa Inspect Alias - automatically uses port 5006

cd /d "C:\Users\YOGA\fp_nlp\demo_chatbot"
call "C:\Users\YOGA\fp_nlp\.venv\Scripts\Activate.bat"
rasa inspect --port 5006 %*