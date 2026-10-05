@echo off
TITLE Employee Performance and Attrition Analytics - B.Tech Project
COLOR 0A

echo ======================================================================
echo    EMPLOYEE PERFORMANCE AND ATTRITION ANALYTICS USING DATA ANALYTICS
echo              B.Tech Computer Science Engineering Project
echo ======================================================================
echo.

:MENU
echo Select an option to execute:
echo  [1] Run Complete Pipeline (Modules 1 to 6: Dataset, Preprocessing, EDA, ML)
echo  [2] Launch Streamlit Interactive Web Dashboard (Module 7)
echo  [3] Run Full Pipeline AND Launch Dashboard
echo  [4] Run Individual Prediction Test (Module 6 Inference)
echo  [5] Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto PIPELINE
if "%choice%"=="2" goto DASHBOARD
if "%choice%"=="3" goto RUNALL
if "%choice%"=="4" goto PREDICT
if "%choice%"=="5" goto EXIT

echo Invalid selection. Please enter a number between 1 and 5.
echo.
goto MENU

:PIPELINE
echo.
echo Running automated data analytics and ML training pipeline...
python run_pipeline.py
echo.
pause
goto MENU

:DASHBOARD
echo.
echo Starting Streamlit Interactive Dashboard on http://localhost:8501 ...
streamlit run dashboard/app.py
pause
goto MENU

:RUNALL
echo.
echo [Step 1/2] Executing Analytics Pipeline...
python run_pipeline.py
echo.
echo [Step 2/2] Launching Interactive Dashboard...
streamlit run dashboard/app.py
pause
goto MENU

:PREDICT
echo.
echo Running real-time inference prediction engine test...
python src/prediction.py
echo.
pause
goto MENU

:EXIT
echo Exiting project launcher. Goodbye!
exit
