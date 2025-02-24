python -m venv venv

.\venv\Scripts\activate

pip install colorama

pyinstaller --onefile --icon=syringe.ico  main.py
