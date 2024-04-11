### How to recreate the exe file


create venv # python -m venv/venv

python source venv/bin/activate

pip install -r requirements.txt



run this command to recreate the app (EXE)
pyinstaller caxbuilder.spec
pyinstaller --onefile caxapp.py

Test partial maps using the 12644094-test-csv-new2.csv file
Test all maps using this 22110708_csv_bobby.csv

#TODO need to add the header back on the cax file when printing out
