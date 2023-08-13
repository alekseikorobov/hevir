RMDIR dist_windows /S /Q
RMDIR build /S /Q
DEL hevir.spec
pyinstaller hevir.py --hidden-import='PIL._tkinter_finder' --noconsole --onefile

MOVE dist dist_windows