import tkinter as tk
from tkinter import ttk
import fenetre2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title('convertisseur de video')


window_width = 300
window_height = 200

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

#8 lignes
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)
root.grid_rowconfigure(7, weight=1)

#11 collones
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)
root.grid_columnconfigure(7, weight=1)
root.grid_columnconfigure(8, weight=1)
root.grid_columnconfigure(9, weight=1)
root.grid_columnconfigure(10, weight=1)

#exemple :
#button.grid(column=0, row=0, columnspan=3, rowspan=3)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.resizable(True, True)
min_width = 200
min_height = 200
max_width = 600
max_height = 600

root.minsize(min_width, min_height)

root.attributes('-alpha',1) #si je veut mettre en transparent

#icone
try:
    # Use iconphoto on Linux and macOS
    photo = tk.PhotoImage(file='./assets/python_icon.png') #.png or .gif
    root.iconphoto(False, photo)
except tk.TclError:
    print("icon file not found.")

# exit button
exit_button = ttk.Button(
    root,
    text='Exit',
    command=lambda: root.quit()
)
exit_button.grid(column=1, row=7, columnspan=3, sticky='nsew')

def button_clicked():
    print('Button clicked')


#la deuxième fenetre
download_icon = tk.PhotoImage(file='./assets/vdo.png')
download_button = ttk.Button(
    root,
    image=download_icon,
    text='Download',
    compound=tk.LEFT
)

def gen_fenetre2():
    download_button.state(['disabled'])
    nouvelle_fenetre = fenetre2.cree_fenetre_conversion()
    root.wait_window(nouvelle_fenetre)
    download_button.state(['!disabled'])

download_button.config(command=gen_fenetre2)

# set the disabled flag
download_button.state(['disabled'])

# remove the disabled flag
download_button.state(['!disabled'])

download_button.grid(column=3, row=3, columnspan=5, rowspan=2, sticky='nsew')



def select(truc):
    print(truc)

font=("Helvetica", 14)


message = tk.Label(root, text="compression de video", font=font).grid(column=3, row=1, columnspan=5, rowspan=2, sticky='nsew')
root.mainloop()