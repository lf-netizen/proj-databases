@echo off

REM Run this file to initialize all docker containers developed for this project.
REM This script will run until the container 'databases-startup' initializes all crucial data and shuts down.

REM IMPORTANT: Only Windows can run this file!
REM            If on UNIX based system see: start_compose.sh

REM Stop containers if busy
call stop_compose.bat

:port_checking
REM Check if port 5432 is in use
netstat -ano | find "5432" > nul

IF %ERRORLEVEL% EQU 0 (
    echo Port 5432 is currently in use. Docker Compose will not start.
    GOTO process_display
) ELSE (
    echo Port 5432 is free. Starting Docker Compose.
    call start_compose.bat
    echo Waiting for database startup to complete. This might take a few minutes...
    :loop
    docker ps -f status=exited | findstr /i "databases-startup-1"
    if %errorlevel% EQU 0 (
        echo Everything is ready!
        GOTO EOF
    )
    timeout /nobreak /t 5 > nul
    GOTO loop
)

:process_display
netstat -ano | findstr :5432
echo Enter the process ID. This is the number on the rightmost column.
set /p pid=
GOTO process_action

:process_action
echo Process details.
tasklist /FI "PID eq %pid%"
echo Would you like to kill the process (y/n)?
set /p action=
IF /i %action% == y (
    GOTO taskkill
) ELSE IF /i %action% == n (
    echo Unable to continue setup.
    GOTO EOF
) ELSE (
    echo Incorrect value.
    GOTO process_action
)

:taskkill
echo Entered pid %pid%
taskkill /PID %pid% /F
GOTO port_checking

:EOF
