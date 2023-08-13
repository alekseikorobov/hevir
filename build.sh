rm dist_linux -r
rm build -r
rm hevir.spec
pyinstaller hevir.py --hidden-import='PIL._tkinter_finder' --onefile

mv dist dist_linux
