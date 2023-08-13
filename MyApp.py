#Import tkinter
import tkinter as tk
from pillow_heif import register_heif_opener
import os
#from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk     # подключаем пакет ttk
from tkinter import filedialog as fd
from StatusBar import StatusBar

import traceback

import functools
fp = functools.partial

class MyApp:

    def __init__(self, root:tk.Tk,form_width=800,form_height=650,full_path = None) -> None:
        register_heif_opener()
        self.root = root
        self.images_list = []
        self.root.title("View image list")
        #TODO: выбрать иконку
        #root.iconbitmap(default="favicon.ico")
        #icon = PhotoImage(file = "icon2.png")
        #root.iconphoto(False, icon)

        # for theme in ttk.Style().theme_names():
        #     print(theme)
        s = ttk.Style()
        s.configure(".",  font="helvetica 13", padding=8, foreground="#AAAAAA", background="black",activebackground='#444444',selectcolor='#999999') #, foreground="#004D40"
              
        self.statusBar = StatusBar(self.root)
        
        #s.configure( 'SeletectedItem.TFrame' )
        #s.theme_use("default")
        #s.configure('my black', background='red')
        
        # Create a photoimage object of the image in the path        
        self.photoImage:ImageTk.PhotoImage = None
        self.image = None
        
        
        self.panel_1 = tk.PanedWindow(bd=2,relief='raised',bg='black',borderwidth=0,border=0,handlepad=0,opaqueresize=0,proxyborderwidth=0,proxybackground='black',sashwidth=2,handlesize=0)
        self.panel_1.pack(fill=tk.BOTH,expand=True)        
        
        self.frame_list_images = ttk.Frame(borderwidth=0, relief=tk.SOLID,border=0)
        
        self.panel_1.add(self.frame_list_images)
        
        
        self.panel_2 = tk.PanedWindow(self.panel_1,orient=tk.VERTICAL,bd=2,relief='raised',bg='black',borderwidth=0,border=0,handlepad=0,opaqueresize=0,proxyborderwidth=0,proxybackground='black',sashwidth=2,handlesize=0)
        self.panel_1.add(self.panel_2)
        
        #self.frame_image = ttk.Frame(borderwidth=0, relief=tk.SOLID, padding=[8, 10])
        #self.frame_image.configure(border=0)
        
        #panel_2.add(self.frame_image)

        self.label1:tk.Label = tk.Label(master=self.panel_2,wraplength=500)
        
        self.canvas = tk.Canvas(self.panel_2,bg="black",border=0,borderwidth=0
                                  ,background='#222222'
                                  ,highlightbackground='black'
                                  ,highlightthickness=1)
        
        self.panel_2.add(self.canvas)

        self.last_index = -1
        self.now_index = -1
        self.form_width = form_width
        self.form_height = form_height

        self.start_position()

        self.images = []
        self.images_var = tk.Variable(value=self.images)
        
        #photo = tk.PhotoImage(file = 'image/Close.png')
        
        # Resizing image to fit on button
        #self.photoimage = photo.subsample(10, 10)
        
        #self.button = tk.Button(self.frame_list_images,text='Close',image=self.photoimage,command=self.hidden_image_list_button)
        #self.button.pack(anchor=tk.NE)        

        self.listbox = tk.Listbox(self.frame_list_images, listvariable=self.images_var
                                  ,background='#222222'
                                  ,foreground='#ffffff'
                                  ,border=0
                                  ,borderwidth=0
                                  ,highlightbackground='black'
                                  ,highlightthickness=1
                                  )

        self.listbox.pack(fill=tk.BOTH,expand=True)

        #self.frame_image.pack(expand=True,fill=tk.BOTH,side=tk.LEFT)
        
        self.is_show_image_list_var = tk.BooleanVar(root,True)
        self.frame_list_images_width = 100
        self.toggle_show_image_list()        

        self.image_width,self.image_height = -1,-1


        self.listbox.bind("<<ListboxSelect>>", self.listBoxSelect)
        self.root.bind("<Configure>", self.on_window_resize)
        
        self.root.bind_all("<Left>", self.on_previes_show_image)
        self.root.bind_all("<Right>", self.on_next_show_image)

        #self.label1.bind("<MouseWheel>", self._on_mousewheel)
        
        #root.bind("<MouseWheel>", self._on_mousewheel)
        self.shared_scale = 1
        #self.label1.bind("<Button-4>", fp(self._on_mousewheel, scroll=1))
        #self.label1.bind("<Button-5>", fp(self._on_mousewheel, scroll=-1))        
        
        self.is_moving_image = False
        #self.label1.bind('<B1-Motion>', self.handler1)
        #self.label1.bind('<ButtonRelease-1>', self.handler2)
        #self.label1.bind('<ButtonPress-1>', self.handler3)
        
        #self.label1.bind_all('<KP_Up>', self.handler4)

        #self.show_image(self.frame1,index=1)
        
        # Bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_image)
        self.canvas.bind("<ButtonRelease-1>", self.stop_move)
        # self.canvas.bind("<Button-4>", self.scale_image)
        # self.canvas.bind("<Button-4>", self.scale_image)
        
        self.canvas.bind("<Button-4>", fp(self._on_mousewheel, scroll=1))
        self.canvas.bind("<Button-5>", fp(self._on_mousewheel, scroll=-1))
        
        
        # Variables to track mouse movement
        self.is_moving = False
        self.start_x = 0
        self.start_y = 0
        self.dx, self.dy = 0,0
        self.scale_factor = 1.0
        self.new_width, self.new_height = 0,0
        
        #menu
        root.option_add("*tearOff", False)
        main_menu = tk.Menu(background='#222222',border=0,activebackground='#444444',foreground='#AAAAAA',selectcolor='#999999')
        file_menu = tk.Menu(background='#444444',selectcolor='#999999',activebackground='#888888')
        file_menu.add_command(label="Open", command=self.dialog_open_one_file)
        file_menu.add_command(label="Load from file", command=self.load_from_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        main_menu.add_cascade(label="File", menu=file_menu)
        
        view_menu = tk.Menu(background='#444444',selectcolor='#999999',activebackground='#888888')
        view_menu.add_checkbutton(label="Show list images", command=self.toggle_show_image_list, variable=self.is_show_image_list_var)        
        main_menu.add_cascade(label="View", menu=view_menu)
        
        self.root.config(menu=main_menu)
        
        self.full_path = full_path
        if self.full_path is not None:
            self.is_show_image_list_var.set(0)
            self.toggle_show_image_list()            
            self.open_one_file(self.full_path)
        
        
        # self.panel_1.
        # self.panel_1.update()
        
        #self.stylename_elements_options('TFrame')
    def after_open_one_file(self):
        self.open_one_file(self.full_path)
        
    def on_previes_show_image(self,event):
        if self.now_index == -1:
            return
        
        if self.now_index == 0:
            return
        
        self.now_index -= 1
        self.show_image()
            
        
    def on_next_show_image(self,event):        
        if self.now_index == -1 and len(self.images_list) == 0:
            return        
        if self.now_index == len(self.images_list)-1:
            return
        
        self.now_index += 1        
        self.show_image()
        
    def hidden_image_list_button(self):
        self.is_show_image_list_var.set(False)
        self.toggle_show_image_list()
    
    def toggle_show_image_list(self):
        if not self.is_show_image_list_var.get():
            
            frame_list_images_width_new = self.frame_list_images.winfo_width()
            if frame_list_images_width_new < 2:
                frame_list_images_width_new = self.frame_list_images_width                
            self.frame_list_images_width = frame_list_images_width_new
            
            self.panel_1.sash_place(0,2,0)
        else:
            self.panel_1.sash_place(0,self.frame_list_images_width,0)
        
    
    def get_files_from_file(self,full_path):
        with open(full_path,'r') as f:
            return [line.replace('\n','') for line in f.readlines()]

    def stylename_elements_options(self, stylename):
        '''Function to expose the options of every element associated to a widget
        stylename.'''
        try:
            # Get widget elements
            style = ttk.Style()
            layout = str(style.layout(stylename))
            print('Stylename = {}'.format(stylename))
            print('Layout    = {}'.format(layout))
            elements=[]
            for n, x in enumerate(layout):
                if x=='(':
                    element=""
                    for y in layout[n+2:]:
                        if y != ',':
                            element=element+str(y)
                        else:
                            elements.append(element[:-1])
                            break
            print('\nElement(s) = {}\n'.format(elements))

            # Get options of widget elements
            for element in elements:
                print('{0:30} options: {1}'.format(
                    element, style.element_options(element)))

        except tk.TclError:
            print('_tkinter.TclError: "{0}" in function'
                'widget_elements_options({0}) is not a regonised stylename.'
                .format(stylename))



    
    def load_from_file(self):
        full_path= fd.askopenfilename(filetypes=[
            ("text", "*.txt"),
            ("all", "*.*")
            ])
        self.images_list = self.get_files_from_file(full_path)        
        self.images = [os.path.split(l)[1] for l in self.images_list]
        self.images_var.set(self.images)
        if len(self.images) > 0:
            self.now_index = 0
            self.show_image()
    
    
    def dialog_open_one_file(self):
        full_path= fd.askopenfilename()
        self.open_one_file(full_path)
    
    def open_one_file(self, full_path):
        if full_path is None or full_path == '':
            return
        
        if not os.path.isfile(full_path):
            raise(f'file not exits - {full_path}')
        
        dir_path, file_name = os.path.split(full_path)
        
        list_files = os.listdir(dir_path)
        
        
        self.images_list = [dir_path + '/'+ f for f in list_files]
        self.images = list_files
        self.images_var.set(self.images)
        self.now_index = self.images.index(file_name)
        self.show_image()
        
        # fd.asksaveasfilename()
        # fd.asksaveasfile()
        # fd.askopenfilename()
        # fd.askopenfile()
        # fd.askdirectory()
        # fd.askopenfilenames()
        # fd.askopenfiles()        
        
        
    def start_move(self, event):
        # Store the starting position of the mouse
        self.start_x = event.x
        self.start_y = event.y
        self.is_moving = True
    
    def move_image(self, event):
        if self.is_moving:
            # Calculate the movement distance
            self.dx = event.x - self.start_x
            self.dy = event.y - self.start_y
            
            # Move the image by the calculated distance
            self.canvas.move(self.image_item, self.dx, self.dy)
            
            # Update the starting position
            self.start_x = event.x
            self.start_y = event.y
            
    def stop_move(self, event):
        self.is_moving = False
    
    def _on_mousewheel(self, event,scroll):
        #print(f'{event}, {scroll=}')
        #self.shared_scale+=scroll*0.1
        if scroll > 0:
            self.scale_factor *= 1.1
        else:
            self.scale_factor /= 1.1
        self.scale_image()
        
        #self.update_image_size()
    
    def show_image(self):
        print(f'show_image {self.now_index=}')
        if self.last_index == self.now_index:
            return
        try:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.now_index)
            
            self.statusBar.set(f'{self.now_index+1} / {len(self.images_list)}')
            
            self.last_index = self.now_index
            self.shared_scale = 1
            self.start_x,self.start_y = 0,0
            self.new_width, self.new_height = 0,0
            self.scale_factor = 1

            path = self.images_list[self.now_index]
            if not os.path.isfile(path):            
                self.label1.configure(text=f'file not exists - {path}',image='')
                self.label1.pack(fill=tk.BOTH,expand=True)
                self.image = None
                self.photoImage = None
                return
            
            self.label1.pack_forget()
            
            self.image = Image.open(path)

            self.image_width, self.image_height = self.image.width,self.image.height

            self.update_image_size()
        except Exception as ex:
            print(f'[ERROR] {ex}')
            traceback.print_exc()

    def start_position(self):
        #w = 800 # width for the Tk root
        #h = 650 # height for the Tk root

        # get screen width and height
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen

        # calculate x and y coordinates for the Tk root window
        x = (ws/2) - (self.form_width/2)
        y = (hs/2) - (self.form_height/2)

        # set the dimensions of the screen
        # and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (self.form_width, self.form_height, x, y))


    def listBoxSelect(self, event):
        selected_indices = self.listbox.curselection()
        if len(selected_indices) == 0:
            return
        
        i = selected_indices[0]
        #print(f'{selected_indices=}')
        #code = listbox.get(i)
        #print(f'{code=}')
        self.now_index = i
        self.show_image()

        #, fill=tk.X
        #show_image(frame1,'2023-02-19 14-59-54.HEIC')

    ###DEBGU
    #получим информацию о всех виджетах в окне:
    def print_info(self,widget, depth=0):
        widget_class = widget.winfo_class()
        widget_width = widget.winfo_width()
        widget_height = widget.winfo_height()
        widget_x = widget.winfo_x()
        widget_y = widget.winfo_y()
        print("   "*depth + f"{widget_class} width={widget_width} height={widget_height}  x={widget_x} y={widget_y}")
        for child in widget.winfo_children():
            self.print_info(child, depth+1)

    #root.update()     # обновляем информацию о виджетах
    #print_info(root)

    def scale_image(self):
        # Calculate the new scale factor based on the scroll direction
        # if event.delta > 0:
        #     self.scale_factor *= 1.1
        # else:
        #     self.scale_factor /= 1.1
        
        # Resize the image and update the canvas item
        new_width = int(self.new_width * self.scale_factor)
        new_height = int(self.new_height * self.scale_factor)
        resized_image = self.image.resize((new_width, new_height)) #, Image.ANTIALIAS
        self.photoImage = ImageTk.PhotoImage(resized_image)
        
        self.canvas.itemconfig(self.image_item, image=self.photoImage)

    def update_image_size(self):

        if self.image is None:
            print('image is empty')
            return
        try:
            frame_width = self.panel_2.winfo_width()
            frame_height = self.panel_2.winfo_height()
            image_resize = self.image
            #if self.image_width > frame_width or self.image_height > frame_height:
            aspect_ratio = min(frame_width / self.image_width, frame_height / self.image_height) * self.shared_scale
            self.new_width = int(self.image_width * aspect_ratio)
            self.new_height = int(self.image_height * aspect_ratio)
            if self.new_width== 0 or self.new_height==0:
                return            
            image_resize = image_resize.resize((self.new_width, self.new_height)) #, Image.ANTIALIAS

            self.photoImage = ImageTk.PhotoImage(image_resize)
            #self.label1.configure(image=self.photoImage)
            #self.label1.pack(fill=tk.BOTH,expand=True)
            
            self.canvas.pack(fill=tk.BOTH,expand=True)
            
            # Display the image on the canvas
            self.image_item = self.canvas.create_image((frame_width / 2), frame_height / 2, image=self.photoImage)
        except Exception as ex:
            print(f'[ERROR] {ex}')
            traceback.print_exc()

        #pass


    def on_window_resize(self,event):
        width = event.width
        height = event.height
        is_change = False
        if self.form_width != event.width:
            is_change = True
            self.form_width = event.width

        if self.form_height != event.height:
            is_change = True
            self.form_height = event.height

        if is_change:
            #print(f"Window resized to {width}x{height}")
            self.update_image_size()


    def mainloop(self):
        self.root.mainloop()