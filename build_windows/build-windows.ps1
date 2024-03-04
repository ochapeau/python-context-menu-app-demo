## Building the App
python.exe -m venv venv
pip install -r ../windows.txt
.\venv\Scripts\activate
pyinstaller.exe .\build.spec
deactivate
Copy-Item -Path .\dist\DAMThemesScript.exe -Destination ..\builds\DAMThemesScript.exe
Remove-Item .\build .\dist -Recurse
Remove-Item .\venv -Recurse