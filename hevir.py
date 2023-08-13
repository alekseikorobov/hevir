import tkinter as tk
from MyApp import MyApp
import sys
import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog as fd
from StatusBar import StatusBar

import functools
fp = functools.partial

if __name__ == '__main__':    
    full_path=None
    # for test sys.argv.append('doc/example/2023-03-18 15-44-05.HEIC')
    if len(sys.argv)>1:
        full_path = sys.argv[1]
        print('-'*40)
        print(f'{os.getcwd()=}')
                
        if not os.path.exists(full_path):
            print(f'not exists file - {full_path}')
            full_path = os.path.join(os.getcwd(),full_path)
        else:
            dir_path, file_name = os.path.split(full_path)
            if dir_path is None or dir_path == '':
                full_path = os.path.join(os.getcwd(),full_path)
                    
        if not os.path.exists(full_path):
            print(f'not exists file - {full_path}')
            full_path=None
    
    print(f'{full_path=}')
    app = MyApp(tk.Tk(),full_path=full_path)
    app.mainloop()