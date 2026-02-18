import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

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

global bitrate_audio_voulu
bitrate_audio_voulu = "192k"

global nom_sortie
nom_sortie = None

global res_X
res_X = None

global res_Y
res_Y = None



#fenetre 2 si on clique sur le bouton
def cree_fenetre_conversion():
    #les call back
    
    def prepare():
        global pret, res_X, res_Y, debit_voulu, bitrate_audio_voulu, nom_sortie, vitesse, format_fixe, video_source
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
        if not bitrate_audio_voulu or bitrate_audio_voulu == "":
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
        
        # Convertir débit audio (de "192k" à nombre)
        if "k" in bitrate_audio_voulu:
            bitrate_audio_num = bitrate_audio_voulu.replace('k', '')
        else:
            print("Erreur: Format de débit audio invalide")
            return
        
        nom_sortie_final = nom_sortie_var.get()
        
        print(f"Configuration:")
        print(f"  Fichier source: {video_source}")
        print(f"  Résolution: {res_X_val}x{res_Y_val}")
        print(f"  Débit vidéo: {debit_voulu_bps} bps")
        print(f"  Débit audio: {bitrate_audio_num}k")
        print(f"  Vitesse: {vitesse}")
        print(f"  Fichier sortie: {nom_sortie_final}.mp4")
        
        command = f"ffmpeg -i \"{video_source}\" -vf \"scale={res_X_val}:{res_Y_val},setsar=1/1\" -c:v libx264 -preset {vitesse} -b:v {debit_voulu_bps} -c:a aac -b:a {bitrate_audio_num} \"{nom_sortie_final}.mp4\""
        print(f"\nCommande: {command}\n")
        subprocess.run(command, shell=True)
        print("=== CONVERSION TERMINÉE ===")

    def update_vitesse(event):
        global vitesse
        selection = listbox_bitrate.curselection()
        vitesse = vitesse_liste[6]  #valeur par defaut
        if selection:
            vitesse = vitesse_liste[selection[0]]  #pour choper la valeur
    
        print("vitesse : ", vitesse)

    def update_bitrate(event):
        global debit_voulu
        debit_voulu = debit_voulu_var.get()
        print("bitrate : ", debit_voulu)

    def update_bitrate_audio(event):
        global bitrate_audio_voulu
        bitrate_audio_voulu = bitrate_audio_voulu_var.get()
        print("bitrate audio : ", bitrate_audio_voulu)

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

    variable_format_fixe = tk.BooleanVar()

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
    
    
    #res X
    current_var_qualite_X = tk.StringVar()
    qualite_sortie_X = ttk.Combobox(fenetre2, textvariable=current_var_qualite_X)
    res_X = current_var_qualite_X.get()
    qualite_sortie_X['values'] = ('144', '360', '480', '540', '720', '1080', '1440', '2160', '4320')
    qualite_sortie_X.bind('<KeyRelease>', update_X)#si on sort de la boite d'ecriture
    qualite_sortie_X.bind('<FocusOut>', update_X)
    qualite_sortie_X.bind('<<ComboboxSelected>>', update_X)
    qualite_sortie_X.pack()
    
    
    
    #res Y
    current_var_qualite_Y = tk.StringVar()
    qualite_sortie_Y = ttk.Combobox(fenetre2, textvariable=current_var_qualite_Y)
    res_Y = current_var_qualite_Y.get()
    qualite_sortie_Y['values'] = ('256', '640', '848', '960', '1280', '1920', '2560', '3840', '7680')
    qualite_sortie_Y.bind('<KeyRelease>', update_Y)#si on sort de la boite d'ecriture
    qualite_sortie_Y.bind('<FocusOut>', update_Y)
    qualite_sortie_Y.bind('<<ComboboxSelected>>', update_Y)# la fonction callback s'excecute si la valeur change par exemple
    qualite_sortie_Y.pack()
    
    
    #ratio ou pas
    garde_ratio = ttk.Checkbutton(
        fenetre2,
        command=lambda: update_ratio(variable_format_fixe),
        text='<garder ratio>',
        variable=variable_format_fixe
    )
    garde_ratio.pack()
    
    
    
    #bitrate
    debit_voulu_var = tk.StringVar()
    choix_debit_voulu = ttk.Combobox(fenetre2, textvariable=debit_voulu_var)
    debit_voulu = debit_voulu_var.get()
    choix_debit_voulu['values'] = ('1.5 Mbps', '4 Mbps', '7.5 Mbps', '12 Mbps', '24 Mbps', '35 Mbps', '100 Mbps')
    choix_debit_voulu.bind('<KeyRelease>', update_bitrate)#si on sort de la boite d'ecriture
    choix_debit_voulu.bind('<FocusOut>', update_bitrate)
    choix_debit_voulu.bind('<<ComboboxSelected>>', update_bitrate)# la fonction callback s'excecute si la valeur change par exemple
    choix_debit_voulu.pack()
    
    
    
    #bitrate audio
    bitrate_audio_voulu_var = tk.StringVar()
    choix_bitrate_audio_voulu = ttk.Combobox(fenetre2, textvariable=bitrate_audio_voulu_var)
    bitrate_audio_voulu = bitrate_audio_voulu_var.get()
    choix_bitrate_audio_voulu['values'] = ('8k', '64k', '128k', '192k', '256k', '320k', '1k')
    choix_bitrate_audio_voulu.bind('<KeyRelease>', update_bitrate_audio)#si on sort de la boite d'ecriture
    choix_bitrate_audio_voulu.bind('<FocusOut>', update_bitrate_audio) 
    choix_bitrate_audio_voulu.bind('<<ComboboxSelected>>', update_bitrate_audio)# la fonction callback s'excecute si la valeur change par exemple
    choix_bitrate_audio_voulu.pack()
    
    
    #choix vitesse compression
    vitesse_liste = ('ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow')
    list_variable = tk.Variable(value=vitesse_liste)
    listbox_bitrate = tk.Listbox(
        fenetre2,
        listvariable=list_variable,
        height=6
    )
    listbox_bitrate.pack(padx=10, pady=10, expand=True, fill=tk.BOTH, side=tk.LEFT)
    listbox_bitrate.bind('<KeyRelease>', update_vitesse)#si on sort de la boite d'ecriture
    listbox_bitrate.bind('<FocusOut>', update_vitesse) 
    listbox_bitrate.bind('<<ListboxSelect>>', update_vitesse)
    
    selection = listbox_bitrate.curselection()
    
    vitesse = vitesse_liste[6]  #valeur par defaut
    if selection:
        vitesse = vitesse_liste[selection[0]]  #pour choper la valeur
    
    
    def update_nom_sortie(event):
        global nom_sortie
        nom_sortie = nom_sortie_var.get()
        print("nom sortie :", nom_sortie)
    
    nom_sortie_var = tk.StringVar() # Entry liée à la variable 
    nom_sortie_entre = tk.Entry(fenetre2, textvariable=nom_sortie_var)
    nom_sortie = nom_sortie_var
    nom_sortie_entre.bind('<KeyRelease>', update_nom_sortie)
    nom_sortie_entre.bind('<FocusOut>', update_nom_sortie)
    nom_sortie_entre.pack()
    
    #a mettre dans un wrapeur pour que ça soit en haut à gauche
    open_button = tk.Button(fenetre2, text="Open File", command=open_file)
    open_button.pack(pady=10)
    
    btn = tk.Button(fenetre2, text="Démarrer la conversion", command=prepare, bg="green", fg="white")
    btn.pack()
    
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