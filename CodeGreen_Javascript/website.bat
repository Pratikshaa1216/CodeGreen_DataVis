@echo off

set "HTML_FILE=C:\Users\49176\Desktop\JS\index.html"  REM Replace this path with the actual path to your HTML file
set "LOG_FILE=C:\Users\49176\Desktop\JS\emissions.csv"  REM Specify the path and filename for the emissions log

REM Start the web server in the background
start "WebServer" cmd /c http-server -p 8006 >nul

REM Open the Dash application in the default web browser
echo Opening the website...
start http://127.0.0.1:8006

REM Import the necessary modules and initialize the EmissionsTracker
echo Initializing CodeCarbon...
start /B "PythonScript" "C:\Users\49176\python.exe" -c "from codecarbon import EmissionsTracker; import time; tracker = EmissionsTracker(); tracker.start(); time.sleep(90); tracker.stop(); tracker.save(r'C:\Users\49176\Desktop\Greenar AI\emissions.csv')"

REM Wait for the Python script to finish executing
ping 127.0.0.1 -n 90 >nul

REM Stop the web server by killing the HTTP server process
echo Stopping the web server...
taskkill /f /fi "WINDOWTITLE eq WebServer"

REM Wait for 90 seconds before closing the website
ping 127.0.0.1 -n 90 >nul

REM Close the website by running a JavaScript code snippet
echo ^<script^>window.close();^</script^> > close.html
start "" close.html
ping 127.0.0.1 -n  1 >nul
del close.html

echo Script execution completed.

REM Close the command prompt window after 5 seconds
timeout /t 5 >nul

exit
