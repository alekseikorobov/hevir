rm dist -r
rm build -r
rm hevir.spec
pyinstaller hevir.py --hidden-import='PIL._tkinter_finder'

mv dist dist_linux
