@echo off
title Lead-Dashboard
cd /d "%~dp0"
python dashboard_starten.py
if errorlevel 1 pause
