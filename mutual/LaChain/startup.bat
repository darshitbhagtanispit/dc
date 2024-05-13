@echo off
setlocal

REM Determine the directory containing the script
SET "BASEDIR=%~dp0"
CD /D "%BASEDIR%"

IF "%1"=="server" (
    echo Starting bank server...
    python bankserver.py
)

IF "%1"=="client" (
    echo Starting client %2...
    python client.py %2
)
