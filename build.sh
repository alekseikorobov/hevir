rm dist -r
rm build -r
rm hevir.spec
pyinstaller hevir.py --hidden-import='PIL._tkinter_finder'
mkdir dist/hevir/pyheif/data -p
echo 0.7.1 > dist/hevir/pyheif/data/version.txt

mv dist dist_linux
