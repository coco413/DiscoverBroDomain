@PUSHD "%~dp0"
@del Result.txt
@del K8scanPort.log
@cls
@title K8 SideNote Scan Port
@color A
::@ping -n 3 127.0.1>nul
@echo.
@echo ScanTime %date% %time%
@echo.

@for /f "tokens=1,2 delims= " %%p in (ScanPort.ini) DO (
@for /f "tokens=1,2 delims= " %%a in (K8ip.txt) DO @echo Scaning... %%a&@K8ScanPort.dat tcp %%a %%b %%p 512 /Banner /save
)
@del K8ip.txt