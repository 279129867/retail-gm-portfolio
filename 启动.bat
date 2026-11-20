@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo 启动三模型页面，浏览器打开 http://localhost:8501
"I:\python311\python.exe" -m streamlit run app.py
pause
