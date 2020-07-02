:Grab working directory
set WD= %cd%
:Move to save directory
cd %HOMEDRIVE%%HOMEPATH%
echo Working Directory: %WD%
py %WD%/main.py
pause