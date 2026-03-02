import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import os

import subprocess

global pret
pret = False

global format_fixe
format_fixe = False

global video_choisie
video_choisie = None # pour que ça ai un scope 

global video_source
video_source = None

global vitesse
vitesse = "slow"

global debit_voulu
debit_voulu = "4M"

global debit_audio_voulu
debit_audio_voulu = "192k"

global nom_sortie
nom_sortie = None

global res_X
res_X = None

global res_Y
res_Y = None

global qualite_calcul, debit_video_calcul, longueur_calcul, taille;
qualite_calcul = None
debit_video_calcul = None
longueur_calcul = None
taille = None

def calcul_taille_initiale(chemin_video_complet):
    #chemin_video_complet avec extention et chemin complet
    commande_recuperation = f'ffprobe -v error -select_streams v:0 -show_entries format=duration,bit_rate,size:stream=width,height -of json "{chemin_video_complet}" > metadata.json'
    print(f"\nCommande: {commande_recuperation}\n")
    subprocess.run(commande_recuperation, shell=True)
    with open('config.json', 'r') as f:
        analyse = json.load(f)
        longueur_calcul = analyse["format"]["duration"]
        qualite_calcul = analyse["streams"]["width"]
        

#fenetre 2 si on clique sur le bouton
def cree_fenetre_conversion():
    #les call back
    
    def prepare():
        global pret, res_X, res_Y, debit_voulu, debit_audio_voulu, nom_sortie, vitesse, format_fixe, video_source
        pret = True
        
        print("=== CONVERSION DÉMARRÉE ===")
        
        # Validation
        if video_source is None:
            print("Erreur: Aucun fichier vidéo sélectionné")
            return
        if nom_sortie_var.get() == "":
            print("Erreur: Nom de fichier de sortie vide")
            return
        if not res_X or res_X == "":
            print("Erreur: Résolution X non définie")
            return
        if not res_Y or res_Y == "":
            print("Erreur: Résolution Y non définie")
            return
        if not debit_voulu or debit_voulu == "":
            print("Erreur: Débit vidéo non sélectionné")
            return
        if not debit_audio_voulu or debit_audio_voulu == "":
            print("Erreur: Débit audio non sélectionné")
            return
        
        # Récupérer valeurs actuelles
        res_X_val = int(res_X)
        res_Y_val = int(res_Y) if not variable_format_fixe.get() else -2
        
        # Ajuster res_X si impair
        if res_X_val % 2 != 0:
            res_X_val = res_X_val + 1
            print(f"Résolution X ajustée de {res_X} à {res_X_val} (doit être pair)")
        
        # Convertir le débit vidéo (de "1.5 Mbps" à bits/s)
        if "Mbps" in debit_voulu or "mbps" in debit_voulu:
            debit_voulu_float = float(debit_voulu.split()[0])
            debit_voulu_bps = int(debit_voulu_float * 1000000)
        else:
            print("Erreur: Format de débit vidéo invalide")
            return
        
        # Valider format débit audio
        if "k" not in debit_audio_voulu:
            print("Erreur: Format de débit audio invalide")
            return
        debit_audio_num = debit_audio_voulu  # Garder le format "Xk" pour FFmpeg
        
        nom_sortie_final = nom_sortie_var.get()
        
        print(f"Configuration:")
        print(f"  Fichier source: {video_source}")
        print(f"  Résolution: {res_X_val}x{res_Y_val}")
        print(f"  Débit vidéo: {debit_voulu_bps} bps")
        print(f"  Débit audio: {debit_audio_num}k")
        print(f"  Vitesse: {vitesse}")
        print(f"  Fichier sortie: {nom_sortie_final}.mp4")
        
        #parser ici
        
        #calcul poid final
        #P = (debit_voulu_bps + debit_audio_num * T)
        
        command = f"ffmpeg -i \"{video_source}\" -vf \"scale={res_X_val}:{res_Y_val},setsar=1/1\" -c:v libx264 -preset {vitesse} -b:v {debit_voulu_bps} -c:a aac -b:a {debit_audio_num} \"{nom_sortie_final}.mp4\""
        print(f"\nCommande: {command}\n")
        subprocess.run(command, shell=True)
        print("=== CONVERSION TERMINÉE ===")

    def update_vitesse(event):
        global vitesse
        selection = listbox_debit.curselection()
        vitesse = vitesse_liste[6]  #valeur par defaut
        if selection:
            vitesse = vitesse_liste[selection[0]]  #pour choper la valeur
    
        print("vitesse : ", vitesse)

    def update_debit(event):
        global debit_voulu
        debit_voulu = debit_voulu_var.get()
        print("debit : ", debit_voulu)

    def update_debit_audio(event):
        global debit_audio_voulu
        debit_audio_voulu = debit_audio_voulu_var.get()
        print("debit audio : ", debit_audio_voulu)

    def update_X(event):
        global res_X
        print("=== CALLBACK DÉCLENCHÉ ===")  # Pour vérifier l'exécution
        res_X = current_var_qualite_X.get()
        print("X :", res_X)
        print("Valeur globale res_X:", res_X)


    def update_Y(event):
        global res_Y
        res_Y = current_var_qualite_Y.get()
        print("Y :", res_Y)

    def update_ratio(variable_format_fixe):
        if (variable_format_fixe.get()):
            format_fixe = True
            print("format fixé")
        else:
            format_fixe = False
            print("format pas fixé")

    global video_source
    
    fenetre2 = tk.Toplevel()
    fenetre2.title('conversion')

    window_width = 600
    window_height = 500

    # get the screen dimension
    screen_width = fenetre2.winfo_screenwidth()
    screen_height = fenetre2.winfo_screenheight()

    # find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    #8 lignes
    fenetre2.grid_rowconfigure(0, weight=1)
    fenetre2.grid_rowconfigure(1, weight=1)
    fenetre2.grid_rowconfigure(2, weight=1)
    fenetre2.grid_rowconfigure(3, weight=1)
    fenetre2.grid_rowconfigure(4, weight=1)
    fenetre2.grid_rowconfigure(5, weight=1)
    fenetre2.grid_rowconfigure(6, weight=1)
    fenetre2.grid_rowconfigure(7, weight=1)
    
    #11 collones
    fenetre2.grid_columnconfigure(0, weight=1)
    fenetre2.grid_columnconfigure(1, weight=1)
    fenetre2.grid_columnconfigure(2, weight=1)
    fenetre2.grid_columnconfigure(3, weight=1)
    fenetre2.grid_columnconfigure(4, weight=1)
    fenetre2.grid_columnconfigure(5, weight=1)
    fenetre2.grid_columnconfigure(6, weight=1)
    fenetre2.grid_columnconfigure(7, weight=1)
    fenetre2.grid_columnconfigure(8, weight=1)
    fenetre2.grid_columnconfigure(9, weight=1)
    fenetre2.grid_columnconfigure(10, weight=1)
    
    # set the position of the window to the center of the screen
    fenetre2.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    fenetre2.resizable(True, True)
    min_width = 200
    min_height = 200
    max_width = 600
    max_height = 600

    fenetre2.minsize(min_width, min_height)
    #root.maxsize(max_width, max_height)

    font=("Helvetica", 14)
    #fenetre2.attributes('-topmost', 1)

    #fenetre2.attributes('-alpha',1) #si je veut mettre en transparent

    variable_format_fixe = tk.BooleanVar()

    def open_file():
        global video_choisie, video_source
        file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Video Files", "*.mp4"), ("All Files", "*.*")]
        )
        if file_path:
            print("Selected File:", file_path)
            video_choisie = open(file_path)
            video_source = file_path
            nom_video = os.path.basename(video_source)
            print("choix:", nom_video)
            calcul_taille_initiale(video_source)#ça renseigne les info de la video de base
            #faire un bool true ici pour dire qu'on peut extraire les info de la video
            #ffprobe -v error -select_streams v:0 -show_entries format=duration,bit_rate,size:stream=width,height -of json input.mp4 > metadata.json
    
    
    #res X
    current_var_qualite_X = tk.StringVar()
    qualite_sortie_X = ttk.Combobox(fenetre2, textvariable=current_var_qualite_X)
    res_X = current_var_qualite_X.get()
    qualite_sortie_X['values'] = ('144', '360', '480', '540', '720', '1080', '1440', '2160', '4320')
    qualite_sortie_X.bind('<KeyRelease>', update_X)#si on sort de la boite d'ecriture
    qualite_sortie_X.bind('<FocusOut>', update_X)
    qualite_sortie_X.bind('<<ComboboxSelected>>', update_X)
    
    def on_qualite_sortie_X_focus_in(event):
        if qualite_sortie_X.get() == "taper ou choisir":
           qualite_sortie_X.delete(0, tk.END)

    def on_qualite_sortie_X_focus_out(event):
        if qualite_sortie_X.get() == "":
            qualite_sortie_X.insert(0, "taper ou choisir")

    qualite_sortie_X.insert(0, "taper ou choisir")
    qualite_sortie_X.bind('<FocusIn>', on_qualite_sortie_X_focus_in)
    qualite_sortie_X.bind('<FocusOut>',on_qualite_sortie_X_focus_out)
    qualite_sortie_X.grid(column=6, row=4, sticky='nsew')

    description_qualite = tk.Label(fenetre2, text="largeur/hauteur image", font=font).grid(column=5, row=3, columnspan=2, sticky='nsew')
    
    
    #res Y
    current_var_qualite_Y = tk.StringVar()
    qualite_sortie_Y = ttk.Combobox(fenetre2, textvariable=current_var_qualite_Y)
    res_Y = current_var_qualite_Y.get()
    qualite_sortie_Y['values'] = ('256', '640', '848', '960', '1280', '1920', '2560', '3840', '7680')
    qualite_sortie_Y.bind('<KeyRelease>', update_Y)#si on sort de la boite d'ecriture
    qualite_sortie_Y.bind('<FocusOut>', update_Y)
    qualite_sortie_Y.bind('<<ComboboxSelected>>', update_Y)# la fonction callback s'excecute si la valeur change par exemple
    
    def on_qualite_sortie_Y_focus_in(event):
        if qualite_sortie_Y.get() == "taper ou choisir":
           qualite_sortie_Y.delete(0, tk.END)

    def on_qualite_sortie_Y_focus_out(event):
        if qualite_sortie_Y.get() == "":
            qualite_sortie_Y.insert(0, "taper ou choisir")

    qualite_sortie_Y.insert(0, "taper ou choisir")
    qualite_sortie_Y.bind('<FocusIn>', on_qualite_sortie_Y_focus_in)
    qualite_sortie_Y.bind('<FocusOut>',on_qualite_sortie_Y_focus_out)
    qualite_sortie_Y.grid(column=6, row=5, sticky='nsew')
    
    #ratio ou pas
    garde_ratio = ttk.Checkbutton(
        fenetre2,
        command=lambda: update_ratio(variable_format_fixe),
        text='garder ratio',
        variable=variable_format_fixe
    )
    garde_ratio.grid(column=2, row=5, sticky='nsew')
    
    
    
    #debit
    debit_voulu_var = tk.StringVar()
    choix_debit_voulu = ttk.Combobox(fenetre2, textvariable=debit_voulu_var)
    debit_voulu = debit_voulu_var.get()
    choix_debit_voulu['values'] = ('1.5 Mbps', '4 Mbps', '7.5 Mbps', '12 Mbps', '24 Mbps', '35 Mbps', '100 Mbps')
    choix_debit_voulu.bind('<KeyRelease>', update_debit)#si on sort de la boite d'ecriture
    choix_debit_voulu.bind('<FocusOut>', update_debit)
    choix_debit_voulu.bind('<<ComboboxSelected>>', update_debit)# la fonction callback s'excecute si la valeur change par exemple
    def on_debit_focus_in(event):
        if choix_debit_voulu.get() == "taper ou choisir":
            choix_debit_voulu.delete(0, tk.END)

    def on_debit_focus_out(event):
        if choix_debit_voulu.get() == "":
            choix_debit_voulu.insert(0, "taper ou choisir")

    choix_debit_voulu.insert(0, "taper ou choisir")
    choix_debit_voulu.bind('<FocusIn>', on_debit_focus_in)
    choix_debit_voulu.bind('<FocusOut>', on_debit_focus_out)
    choix_debit_voulu.grid(column=9, row=4, sticky='nsew')
    
    
    
    #debit audio
    debit_audio_voulu_var = tk.StringVar()
    choix_debit_audio_voulu = ttk.Combobox(fenetre2, textvariable=debit_audio_voulu_var)
    debit_audio_voulu = debit_audio_voulu_var.get()
    choix_debit_audio_voulu['values'] = ('8k', '64k', '128k', '192k', '256k', '320k', '1k')
    choix_debit_audio_voulu.bind('<KeyRelease>', update_debit_audio)#si on sort de la boite d'ecriture
    choix_debit_audio_voulu.bind('<FocusOut>', update_debit_audio) 
    choix_debit_audio_voulu.bind('<<ComboboxSelected>>', update_debit_audio)# la fonction callback s'excecute si la valeur change par exemple
    
    def on_debit_audio_focus_in(event):
        if choix_debit_audio_voulu.get() == "taper ou choisir":
            choix_debit_audio_voulu.delete(0, tk.END)

    def on_debit_audio_focus_out(event):
        if choix_debit_audio_voulu.get() == "":
            choix_debit_audio_voulu.insert(0, "taper ou choisir")

    choix_debit_audio_voulu.insert(0, "taper ou choisir")
    choix_debit_audio_voulu.bind('<FocusIn>', on_debit_audio_focus_in)
    choix_debit_audio_voulu.bind('<FocusOut>', on_debit_audio_focus_out)
    
    choix_debit_audio_voulu.grid(column=9, row=5, sticky='nsew')
    
    #description texte des nom des combox
    description_debit = tk.Label(fenetre2, text="debit audio/video", font=font).grid(column=8, row=3, columnspan=2, sticky='nsew')
    
    #choix vitesse compression
    vitesse_liste = ('ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow')
    list_variable = tk.Variable(value=vitesse_liste)
    listbox_debit = tk.Listbox(
        fenetre2,
        listvariable=list_variable,
        height=6
    )
    listbox_debit.grid(column=1, row=6, columnspan=2, sticky='nsew')#pack(padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT)
    listbox_debit.bind('<KeyRelease>', update_vitesse)#si on sort de la boite d'ecriture
    listbox_debit.bind('<FocusOut>', update_vitesse) 
    listbox_debit.bind('<<ListboxSelect>>', update_vitesse)
    
    selection = listbox_debit.curselection()
    #TODO implementer acceleration gpu
    vitesse = vitesse_liste[6]  #valeur par defaut
    if selection:
        vitesse = vitesse_liste[selection[0]]  #pour choper la valeur
    
    
    def update_nom_sortie(event):
        global nom_sortie
        nom_sortie = nom_sortie_var.get()
        print("nom sortie :", nom_sortie)
    #chat gpt wrote that###########
    def on_focus_in(event):
        if nom_sortie_entre.get() == "Nom du fichier de sortie":
            nom_sortie_entre.delete(0, tk.END)
            nom_sortie_entre.config(fg='black')

    def on_focus_out(event):
        if nom_sortie_entre.get() == "":
            nom_sortie_entre.insert(0, "Nom du fichier de sortie")
            nom_sortie_entre.config(fg='gray')
    ###############################
    
    nom_sortie_var = tk.StringVar() # Entry liée à la variable 
    nom_sortie_entre = tk.Entry(fenetre2, textvariable=nom_sortie_var)
    nom_sortie_entre.insert(0, "Nom du fichier de sortie")
    nom_sortie_entre.config(fg='gray')
    nom_sortie = nom_sortie_var
    nom_sortie_entre.bind('<FocusIn>', on_focus_in)
    nom_sortie_entre.bind('<KeyRelease>', update_nom_sortie)
    nom_sortie_entre.bind('<FocusOut>', on_focus_out)
    nom_sortie_entre.grid(column=1, row=4, columnspan=2, sticky='nsew')
    
    open_button = tk.Button(fenetre2, text="Open File", command=open_file)
    open_button.grid(column=1, row=2, columnspan=2, sticky='nsew')
    
    btn = tk.Button(fenetre2, text="Démarrer la conversion", command=prepare, bg="green", fg="white")
    btn.grid(column=5, row=7, columnspan=2, sticky='nsew')
    
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
pour le debit
ffprobe -v error -show_entries format=duration,bit_rate,size -of json input.mp4

pour la qualite
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=p=0 input.mp4
ou alors 

ffprobe -v error -select_streams v:0 -show_entries format=duration,bit_rate,size:stream=width,height -of json input.mp4 > metadata.json
ça cree un parser du style :
{
    "programs": [],
    "streams": [
        {
            "width": 1920,
            "height": 1080
        }
    ],
    "format": {
        "duration": "120.450000",
        "size": "15728640",
        "bit_rate": "1044747"
    }
}
TODO faire un parser pour recuperer les données
with open('config.json', 'r') as f:
    analyse = json.load(f)
    duree = analyse["format"]["duration"]
'''