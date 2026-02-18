import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import subprocess

pret = False
format_fixe = False
variable_format_fixe = tk.BooleanVar()

video_choisie = None # pour que ça ai un scope 
video_source = None
vitesse = "slow"
debit_voulu = "4M"
bitrate_audio_voulu = "192k"
nom_sortie = None
res_X = None
res_Y = None

def prepare():
    pret = True

def update_vitesse(event):
    print("vitesse : ", vitesse)

def update_bitrate(event):
    print("bitrate : ", vitesse)


def update_X(event):
    print("X :", res_X)

def update_Y(event):
    print("Y :", res_Y)

def update_ratio():
    if (variable_format_fixe.get()):
        format_fixe = True
        print("format fixé")
    else:
        format_fixe = False
        print("format pas fixé")

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

    

    def open_file():
        global video_choisie, video_source
        file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            print("Selected File:", file_path)
            video_choisie = open(file_path)
            video_source = file_path
            print(video_choisie) #a traiter plus tard
            
    current_var_qualite_X = tk.StringVar()
    qualite_sortie_X = ttk.Combobox(fenetre2, textvariable=current_var_qualite_X)
    res_X = current_var_qualite_X.get()
    #res X
    qualite_sortie_X['values'] = ('144', '360', '480', '540', '720', '1080', '1440', '2160', '4320')
    qualite_sortie_X.bind('<<ComboboxSelected>>', update_X)# la fonction callback s'excecute si la valeur change par exemple
    qualite_sortie_X.pack()
    
    current_var_qualite_Y = tk.StringVar()
    qualite_sortie_Y = ttk.Combobox(fenetre2, textvariable=current_var_qualite_Y)
    res_Y = current_var_qualite_Y.get()
    #res Y
    qualite_sortie_Y['values'] = ('256', '640', '848', '960', '1280', '1920', '2560', '3840', '7680')
    qualite_sortie_Y.bind('<<ComboboxSelected>>', update_Y)# la fonction callback s'excecute si la valeur change par exemple
    qualite_sortie_Y.pack()
    
    
    #ratio ou pas
    garde_ratio = ttk.Checkbutton(
        fenetre2,
        command=update_ratio,
        text='<garder ratio>',
        variable=variable_format_fixe
    )
    garde_ratio.pack()
    
    
    
    #bitrate
    debit_voulu_var = tk.StringVar()
    choix_debit_voulu = ttk.Combobox(fenetre2, textvariable=current_var_qualite_Y)
    debit_voulu = debit_voulu_var.get()
    choix_debit_voulu['values'] = ('1.5 Mbps', '4 Mbps', '7.5 Mbps', '12 Mbps', '24 Mbps', '35 Mbps', '100 Mbps')
    choix_debit_voulu.bind('<<ComboboxSelected>>', update_Y)# la fonction callback s'excecute si la valeur change par exemple
    choix_debit_voulu.pack()
    
    
    #choix vitesse compression
    vitesse_liste = ('ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow')
    list_variable = tk.Variable(value=vitesse_liste)
    listbox_bitrate = tk.Listbox(
        fenetre2,
        listvariable=list_variable,
        height=6
    )
    listbox_bitrate.pack(padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT)
    listbox_bitrate.bind('<<ListboxSelect>>', update_bitrate)
    
    selection = listbox_bitrate.curselection()
    
    if selection:
        vitesse = vitesse_liste[selection[0]]  #pour choper la valeur
    
    
    
    
    #a mettre dans un wrapeur pour que ça soit en haut à gauche
    open_button = tk.Button(fenetre2, text="Open File", command=open_file)
    open_button.pack(pady=10)
    
    btn = tk.Button(fenetre2, text="pret", command=prepare)
    
    if((video_source != None) and (debit_voulu != None) and (nom_sortie != None)):
        btn.config(state='normal')
    else:
        btn.config(state='disabled')
    
    res_X = int(res_X)
    if (pret):
        #aac codec audio de base on peut changer comme libx264 changer res_Y en -2 si il connais pas bien setsar=1/1 pour pas que le codec la reforme si on la deforme
        if(res_X %2 != 0):
            res_X = res_X + 1 if res_X % 2 != 0 else res_X
        if (garde_ratio):
            res_Y = -2 # si on veut garde le ratio faut faire ça
        command = f"ffmpeg -i {video_source} -vf \"scale={res_X}:{res_Y}setsar=1/1\" -c:v libx264 -preset {vitesse} -b:v {debit_voulu} -c:a aac -b:a {bitrate_audio_voulu} {nom_sortie}.mp4"
        subprocess.run(command, shell=True) #pour appeler notre commande custom

    
    return fenetre2


'''
Format (Extension)	Codec Vidéo suggéré (-c:v)	Codec Audio suggéré (-c:a)
.mp4	libx264 ou libx265	aac
.mkv	libx264 ou vp9	opus ou flac
.webm	libvpx-vp9	libopus
.avi	mpeg4	mp3
exemple ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -crf 23 output.mkv

Sélecteur de Codec	-c:v	libx264, libx265, vp9
Curseur Qualité	-crf	18 (Haut) à 28 (Bas)
Vitesse de traitement	-preset	ultrafast à veryslow
Limite de débit	-b:v	2M, 5M, 10M
Qualité Audio	-b:a	128k, 192k, 320k
exemple ffmpeg -i video_source.mov -c:v libx264 -preset slow -crf 20 -b:v 4M -c:a aac -b:a 192k sortie.mp4

pour choisir la qualitée -vf "scale=1280:720"
et ou -vf "scale=1280:-2" si on veut qu'elle soit tjr fixe

P = (R video + R audio * T)8 on met R et T donnné par l'utilisateur
P: Poids du fichier en MegaOctets (Mo).
R : Débit binaire total (Vidéo + Audio) en kilobits par seconde (kbps).
T : Durée de la vidéo en secondes.
Le chiffre 8 sert à convertir les bits en octets.

1k = 1000 bits/s

ffprobe
pour le bitrate
ffprobe -v error -show_entries format=duration,bit_rate,size -of json input.mp4

pour la qualite
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input.mp4

'''