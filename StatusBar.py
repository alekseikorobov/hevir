import tkinter as tk
 
class StatusBar(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(background='#222222',border=0)
        self.label = tk.Label(self, background="#222222", foreground="#AAAAAA") #
        self.label.pack(side=tk.LEFT)
        self.pack(side=tk.BOTTOM, fill=tk.X)
        
    def set(self, newText):
        self.label.config(text=newText)
 
    def clear(self):
        self.label.config(text="")