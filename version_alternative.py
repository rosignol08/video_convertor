import tkinter as tk
from tkinter import ttk, filedialog
import subprocess
import json
import os
import threading

# ==========================================
# FENÊTRE PRINCIPALE (ROOT)
# ==========================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Convertisseur de Vidéo')
        self.geometry('300x200')
        self.center_window(300, 200)
        self.minsize(200, 200)

        # Remplacement de tes 18 lignes par deux boucles pour configurer la grille
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(11):
            self.grid_columnconfigure(i, weight=1)

        # CORRECTION : Création PUIS placement (pour ne pas casser les variables)
        self.message = tk.Label(self, text="Compression de vidéo", font=("Helvetica", 14))
        self.message.grid(column=3, row=1, columnspan=5, rowspan=2, sticky='nsew')

        self.download_button = ttk.Button(self, text='Ouvrir Convertisseur', command=self.ouvrir_fenetre2)
        self.download_button.grid(column=3, row=3, columnspan=5, rowspan=2, sticky='nsew')

        self.exit_button = ttk.Button(self, text='Exit', command=self.quit)
        self.exit_button.grid(column=1, row=7, columnspan=3, sticky='nsew')

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def ouvrir_fenetre2(self):
        self.download_button.state(['disabled'])
        # On crée l'objet FenetreConversion et on lui passe la fenêtre principale (self)
        FenetreConversion(self)


# ==========================================
# SECONDE FENÊTRE (CONVERTISSEUR)
# ==========================================
class FenetreConversion(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title('Conversion Vidéo')
        self.geometry('800x600')
        self.center_window(800, 600)
        self.minsize(600, 400)
        
        # Réactive le bouton "Download" quand on ferme la fenêtre 2
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # ==============================================================
        # VARIABLES D'ÉTAT (Ceci remplace tous tes "global video_source")
        # ==============================================================
        self.video_source = None
        self.variable_format_fixe = tk.BooleanVar(value=False)
        self.font = ("Helvetica", 14)

        self.setup_ui()

    def on_close(self):
        self.parent.download_button.state(['!disabled'])
        self.destroy()

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - width / 2)
        center_y = int(screen_height / 2 - height / 2)
        self.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def setup_ui(self):
        # Grille
        for i in range(8):
            self.grid_rowconfigure(i, weight=1)
        for i in range(11):
            self.grid_columnconfigure(i, weight=1)

        # Ligne 2 : Fichier source et infos
        self.open_button = tk.Button(self, text="Open File", command=self.open_file)
        self.open_button.grid(column=1, row=2, columnspan=2, sticky='nsew', padx=5, pady=5)

        self.info_video_var = tk.StringVar(value="Aucune vidéo sélectionnée\nEn attente...\n\n")
        self.info_label = tk.Label(self, textvariable=self.info_video_var, justify="left", font=("Helvetica", 10), bg="#f0f0f0", relief="sunken")
        self.info_label.grid(column=4, row=2, columnspan=4, sticky='nsew', padx=10, pady=5)

        self.btn_demarrer = tk.Button(self, text="Démarrer la conversion", command=self.preparer_conversion, bg="green", fg="white")
        self.btn_demarrer.grid(column=8, row=2, columnspan=2, sticky='nsew', padx=5, pady=5)

        # Lignes 4 & 5 : Paramètres (Entrées)
        self.nom_sortie_var = tk.StringVar()
        self.nom_sortie_entre = tk.Entry(self, textvariable=self.nom_sortie_var)
        self.nom_sortie_entre.insert(0, "nom_fichier_sortie")
        self.nom_sortie_entre.grid(column=1, row=4, columnspan=2, sticky='nsew')

        self.garde_ratio = ttk.Checkbutton(self, text='Garder ratio (-2)', variable=self.variable_format_fixe)
        self.garde_ratio.grid(column=1, row=5, columnspan=2, sticky='nsew')

        self.desc_qualite = tk.Label(self, text="Largeur / Hauteur", font=self.font)
        self.desc_qualite.grid(column=5, row=3, columnspan=2, sticky='s')

        self.qualite_sortie_X = ttk.Combobox(self, values=('480', '720', '1080', '1440', '1920', '2160'))
        self.qualite_sortie_X.set('1920')
        self.qualite_sortie_X.grid(column=6, row=4, sticky='nsew', pady=2)

        self.qualite_sortie_Y = ttk.Combobox(self, values=('640', '1280', '1920', '2560', '3840'))
        self.qualite_sortie_Y.set('1080')
        self.qualite_sortie_Y.grid(column=6, row=5, sticky='nsew', pady=2)

        self.desc_debit = tk.Label(self, text="Débit Vidéo / Audio", font=self.font)
        self.desc_debit.grid(column=8, row=3, columnspan=2, sticky='s')

        self.choix_debit_voulu = ttk.Combobox(self, values=('1.5M', '4M', '7.5M', '12M', '24M'))
        self.choix_debit_voulu.set('4M')
        self.choix_debit_voulu.grid(column=9, row=4, sticky='nsew', pady=2)

        self.choix_debit_audio = ttk.Combobox(self, values=('64k', '128k', '192k', '256k', '320k'))
        self.choix_debit_audio.set('192k')
        self.choix_debit_audio.grid(column=9, row=5, sticky='nsew', pady=2)

        # Lignes 6 & 7 : Vitesse et Terminal
        self.vitesse_liste = ('ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow')
        self.list_variable = tk.Variable(value=self.vitesse_liste)
        self.listbox_vitesse = tk.Listbox(self, listvariable=self.list_variable, height=6)
        self.listbox_vitesse.grid(column=1, row=6, columnspan=2, sticky='nsew', pady=10)
        self.listbox_vitesse.selection_set(6) # Sélectionne 'slow' par défaut

        self.terminal = tk.Text(self, bg="black", fg="#00FF00", font=("Consolas", 9), wrap="word")
        self.terminal.grid(column=4, row=6, columnspan=6, rowspan=2, sticky='nsew', padx=10, pady=10)
        self.print_terminal("Terminal prêt. En attente de fichier...")

    # ==========================================
    # LOGIQUE APPLICATIVE
    # ==========================================
    def print_terminal(self, message):
        """Affiche un message dans le terminal textuel de Tkinter de façon Thread-Safe"""
        self.terminal.insert(tk.END, str(message) + "\n")
        self.terminal.see(tk.END)
        self.update_idletasks()

    def open_file(self):
        file_path = filedialog.askopenfilename(title="Choix du fichier", filetypes=[("Vidéo", "*.mp4 *.mkv *.mov *.avi"), ("Autre", "*.*")])
        if file_path:
            self.video_source = file_path
            self.print_terminal(f"Fichier sélectionné : {os.path.basename(file_path)}")
            self.calculer_metadonnees(file_path)

    def calculer_metadonnees(self, chemin):
        # Utilisation d'une liste pour plus de sécurité avec subprocess
        commande = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "format=duration,size:stream=width,height",
            "-of", "json", chemin
        ]
        
        try:
            # capture_output=True évite d'avoir à créer un metadata.json sur le disque
            resultat = subprocess.run(commande, capture_output=True, text=True, check=True)
            analyse = json.loads(resultat.stdout)

            duree = float(analyse.get("format", {}).get("duration", 0))
            taille_mo = int(analyse.get("format", {}).get("size", 0)) / (1024 * 1024)
            streams = analyse.get("streams", [{}])
            largeur = streams[0].get("width", "N/A") if streams else "N/A"
            hauteur = streams[0].get("height", "N/A") if streams else "N/A"

            info_texte = f"Nom : {os.path.basename(chemin)}\nRésolution : {largeur}x{hauteur}\nTaille : {taille_mo:.2f} Mo\nDurée : {duree:.2f} s"
            self.info_video_var.set(info_texte)
            self.print_terminal("Métadonnées récupérées en mémoire avec succès.")

        except Exception as e:
            self.info_video_var.set("Erreur lors de la lecture des métadonnées.")
            self.print_terminal(f"Erreur FFprobe : {e}")

    def preparer_conversion(self):
        if not self.video_source:
            self.print_terminal("Erreur: Aucun fichier sélectionné.")
            return

        nom_sortie_val = self.nom_sortie_var.get().strip()
        if not nom_sortie_val or nom_sortie_val == "nom_fichier_sortie":
            self.print_terminal("Erreur: Spécifiez un nom de fichier valide.")
            return

        # Récupération sécurisée des paramètres
        try:
            res_x_int = int(self.qualite_sortie_X.get())
            if res_x_int % 2 != 0: res_x_int += 1 # FFmpeg a besoin de nombres pairs
        except ValueError:
            res_x_int = 1920

        # Si le ratio est gardé, FFmpeg demande -2 sur la hauteur
        res_y_str = "-2" if self.variable_format_fixe.get() else self.qualite_sortie_Y.get()

        selection_vitesse = self.listbox_vitesse.curselection()
        vitesse = self.vitesse_liste[selection_vitesse[0]] if selection_vitesse else "slow"

        # Note : On donne la lettre "M" ou "k" directement à FFmpeg, pas besoin de multiplier par 1_000_000
        debit_v = self.choix_debit_voulu.get()
        debit_a = self.choix_debit_audio.get()

        chemin_sortie = os.path.join(os.path.dirname(self.video_source), f"{nom_sortie_val}.mp4")

        commande_ffmpeg = [
            "ffmpeg", "-i", self.video_source,
            "-vf", f"scale={res_x_int}:{res_y_str},setsar=1/1",
            "-c:v", "libx264", "-preset", vitesse,
            "-b:v", debit_v,
            "-c:a", "aac", "-b:a", debit_a,
            "-y", chemin_sortie
        ]

        # Bloque le bouton pour éviter de lancer plusieurs encodages
        self.btn_demarrer.config(state="disabled")
        
        # Lance la conversion DANS UN THREAD SÉPARÉ (Empêche l'interface de geler)
        thread = threading.Thread(target=self.executer_ffmpeg_thread, args=(commande_ffmpeg,))
        thread.daemon = True # Le thread se ferme si on quitte le programme
        thread.start()

    def executer_ffmpeg_thread(self, commande):
        self.terminal.after(0, self.print_terminal, "=== CONVERSION DÉMARRÉE ===")
        self.terminal.after(0, self.print_terminal, f"Commande : {' '.join(commande)}")

        # Redirection de stdout et stderr pour lire la progression
        process = subprocess.Popen(
            commande,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, # FFmpeg crache ses logs dans stderr, on le redirige dans stdout
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0 # Cache la console noire sous Windows
        )

        # Lit chaque ligne de sortie en direct
        for ligne in process.stdout:
            # Utilisation de .after() indispensable pour qu'un thread secondaire modifie un widget Tkinter !
            self.terminal.after(0, self.print_terminal, ligne.strip())

        process.wait()

        if process.returncode == 0:
            self.terminal.after(0, self.print_terminal, "\n=== CONVERSION TERMINÉE AVEC SUCCÈS ===")
        else:
            self.terminal.after(0, self.print_terminal, "\n=== ERREUR LORS DE LA CONVERSION ===")

        # Réactive le bouton à la fin
        self.btn_demarrer.after(0, lambda: self.btn_demarrer.config(state="normal"))


if __name__ == '__main__':
    app = App()
    app.mainloop()