import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import subprocess

subprocess.run(["ls", "-l"]) #pour appeler notre commande custom


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

    video_choisie : None # pour que ça ai un scope 

    def open_file():
        file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            print("Selected File:", file_path)
            video_choisie = open(file_path)
            print(video_choisie) #a traiter plus tard
    #a mettre dans un wrapeur pour que ça soit en haut à gauche
    open_button = tk.Button(fenetre2, text="Open File", command=open_file)
    open_button.pack(pady=10)
    
    
    return fenetre2
