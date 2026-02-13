import tkinter as tk
from tkinter import ttk
import fenetre2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title('Tkinter Window Demo')


window_width = 300
window_height = 200

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

root.resizable(True, True)
min_width = 200
min_height = 200
max_width = 600
max_height = 600

root.minsize(min_width, min_height)
#root.maxsize(max_width, max_height)

root.attributes('-topmost', 2)

root.attributes('-alpha',1) #si je veut mettre en transparent

#icone
try:
    # Use iconphoto on Linux and macOS
    photo = tk.PhotoImage(file='./assets/python_icon.png') #.png or .gif
    root.iconphoto(False, photo)
except tk.TclError:
    print("icon file not found.")
    
    
    

'''
si on veut des flag pour desactiver ou pas le bouton
# set the disabled flag
button.state(['disabled'])

# remove the disabled flag
button.state(['!disabled'])
'''

# exit button
exit_button = ttk.Button(
    root,
    text='Exit',
    command=lambda: root.quit()
)

exit_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)

def button_clicked():
    print('Button clicked')


ttk.Button(root, text='Click Me',command=button_clicked)

button = ttk.Button(root, text='Click Me', command=button_clicked)
button.pack()

'''bouton avec image pour telechargre la video'''


#def handle_click():
#    showinfo(
#        title='Information',
#        message='Download button clicked!'
#    )

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

download_button.pack(
    ipadx=5,
    ipady=5,
    expand=True
)



def select(truc):
    print(truc)

boutton_fonction = ttk.Button(root, text='Rock', command=lambda: select('Rock')).pack()


font=("Helvetica", 14)


message = tk.Label(root, text="Hello, World!", font=font)
message.pack()

message1 = tk.Label(root, text='Classic Label')
message2 = ttk.Label(root, text='Themed Label')

#photo = tk.PhotoImage(file='./assets/MSI_MPG.png')
#image_label = ttk.Label(
#    root,
#    image=photo,
#    padding=5,
#    text='Python',
#    compound=tk.TOP
#)
#image_label.pack()

message1.pack()
message2.pack()


'''pour placer des widget a certain endroits

label1 = tk.Label(master=root, text="Place",bg='red',fg='white')
label1.place(x=0,y=0,width=120, height=60)

'''

#pour ouvrir un fichier file_path = filedialog.askopenfilename(title="Select a File")


root.mainloop()


#"./assets/269091_video-camera-icon.png"


