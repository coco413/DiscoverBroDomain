@PUSHD "%~dp0"
@del Result.txt
@del K8banner.log
@cls
@title K8 SideNote ScanBanner
@color A
@echo.
@echo ScanTime %date% %time%
@echo.
@for /f "tokens=1,2 delims= " %%a in (K8ip.txt) DO @echo Scaning... %%a&@K8ScanPort.dat tcp %%a %%b 80 2 /HBanner /save
@for /f "eol= tokens=*" %%i in (Result.txt) DO (

)
@del K8ip.txt
@del Result.txt
