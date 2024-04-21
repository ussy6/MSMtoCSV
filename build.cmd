rem このファイルの位置を作業ディレクトリに
call C:\ProgramData\miniconda3\Scripts\activate.bat
call C:\Users\%USERNAME%\miniconda3\Scripts\activate.bat

conda env create -n MSMtoCSV -f MSMtoCSV.yaml
pause

