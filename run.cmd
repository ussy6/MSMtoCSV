rem このファイルの位置を作業ディレクトリに
cd code
set here=%CD%
echo %here%

call C:\ProgramData\miniconda3\Scripts\activate.bat
call C:\Users\%USERNAME%\miniconda3\Scripts\activate.bat
call conda activate MSMtoCSV
call conda info -e

set HENSU=%USERNAME%
echo %HENSU%

C:\Users\%USERNAME%\.conda\envs\MSMtoCSV\python.exe %here%\main.py
C:\Users\takah\miniconda3\envs\MSMtoCSV\python.exe %here%\main.py
echo C:\Users\%USERNAME%\.conda\envs\MSMtoCSV\python.exe %here%\main.py
echo C:\Users\takah\miniconda3\envs\MSMtoCSV\python.exe %here%\main.py

pause