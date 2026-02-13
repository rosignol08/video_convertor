import tkinter as tk
from tkinter import ttk

#fenetre 2 si on clique sur le bouton
def cree_fenetre_conversion():
    
    fenetre2 = tk.Toplevel()
    fenetre2.title('conversion')


    window_width = 300
    window_height = 200

    # get the screen dimension
    screen_width = fenetre2.winfo_screenwidth()
    screen_height = fenetre2.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    fenetre2.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    fenetre2.resizable(True, True)
    min_width = 200
    min_height = 200
    max_width = 600
    max_height = 600

    fenetre2.minsize(min_width, min_height)
    #root.maxsize(max_width, max_height)

    fenetre2.attributes('-topmost', 1)

    #fenetre2.attributes('-alpha',1) #si je veut mettre en transparent
    
    return fenetre2
