# Video Convertor

<div align="center">

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![tkinter](https://img.shields.io/badge/GUI-tkinter-green.svg)
![ffmpeg](https://img.shields.io/badge/powered%20by-FFmpeg-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**Une interface graphique intuitive pour FFmpeg | An intuitive GUI for FFmpeg**

[Français](#français) • [English](#english)

</div>

---

## Français

### Description

**Video Convertor** est une interface graphique moderne et professionnelle pour FFmpeg, conçue pour simplifier la conversion et le traitement vidéo. Cette application permet aux utilisateurs de bénéficier de toute la puissance de FFmpeg sans avoir à mémoriser des lignes de commande complexes.

FFmpeg est un outil en ligne de commande extrêmement puissant mais difficile d'accès pour les utilisateurs non techniques. Video Convertor comble cette lacune en offrant une interface intuitive qui génère automatiquement les commandes FFmpeg appropriées en fonction de vos besoins.

### Fonctionnalités

- **Interface utilisateur intuitive** : Interface tkinter moderne et facile à utiliser
- **Conversion vidéo professionnelle** : Contrôle total sur les paramètres de conversion
- **Gestion de la résolution** : 
  - Sélection de résolution personnalisée (X et Y)
  - Option de maintien du ratio d'aspect
  - Résolutions prédéfinies (144p à 8K)
- **Contrôle du débit binaire** :
  - Débit vidéo réglable (1.5 Mbps à 100 Mbps)
  - Débit audio configurable (8k à 320k)
- **Presets de vitesse** : Du plus rapide (ultrafast) au plus lent (veryslow) pour optimiser qualité/temps
- **Support des codecs modernes** :
  - Vidéo : libx264 (H.264)
  - Audio : AAC
- **Export MP4** : Format de sortie optimisé pour une compatibilité maximale

### Prérequis

- Python 3.x
- FFmpeg installé sur votre système
- Bibliothèques Python :
  - tkinter (généralement inclus avec Python)
  - subprocess (bibliothèque standard)
  - json (bibliothèque standard)

### Installation

1. **Installer FFmpeg** :
   
   **Linux (Ubuntu/Debian)** :
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   **Linux (Fedora)** :
   ```bash
   sudo dnf install ffmpeg
   ```
   **Linux (Arch)** :
   ```bash
   sudo pacman -S ffmpeg
   ```
   **macOS** :
   ```bash
   brew install ffmpeg
   ```
   
   **Windows** :
   Téléchargez depuis [ffmpeg.org](https://ffmpeg.org/download.html) et ajoutez-le au PATH

3. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/rosignol08/video_convertor.git
   cd video_convertor
   ```
   ou telecharger le bianaire en release

4. **Vérifier l'installation de Python** :
   ```bash
   python --version
   # ou
   python3 --version
   ```

### Utilisation

1. **Lancer l'application** :
   ```bash
   python main.py
   # ou
   python3 main.py
   ```

2. **Convertir une vidéo** :
   - Cliquez sur le bouton "Download" (Conversion) dans la fenêtre principale
   - Une nouvelle fenêtre s'ouvrira avec les options de conversion
   - Cliquez sur "Open File" pour sélectionner votre vidéo source
   - Configurez les paramètres :
     - **Résolution X** : Largeur de la vidéo
     - **Résolution Y** : Hauteur de la vidéo (ou cochez "garder ratio" pour maintenir les proportions)
     - **Débit vidéo** : Qualité de la vidéo (plus élevé = meilleure qualité)
     - **Débit audio** : Qualité de l'audio
     - **Vitesse de compression** : Équilibre entre temps de traitement et qualité
     - **Nom de sortie** : Nom du fichier de sortie (sans extension)
   - Cliquez sur "Démarrer la conversion"

3. **Récupérer votre vidéo** :
   - La vidéo convertie sera enregistrée dans le même répertoire que l'application
   - Le nom du fichier sera celui que vous avez spécifié avec l'extension .mp4

### Commandes FFmpeg générées

L'application génère des commandes FFmpeg de la forme :
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=1920:1080,setsar=1/1" \
  -c:v libx264 \
  -preset slow \
  -b:v 4000000 \
  -c:a aac \
  -b:a 192k \
  "output.mp4"
```

Cette commande :
- Redimensionne la vidéo à la résolution spécifiée
- Utilise le codec H.264 pour la vidéo
- Applique le preset de vitesse choisi
- Configure le débit binaire vidéo et audio
- Encode l'audio en AAC

### Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

### Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

---

## English

### Description

**Video Convertor** is a modern and professional graphical user interface for FFmpeg, designed to simplify video conversion and processing. This application allows users to harness the full power of FFmpeg without having to memorize complex command-line syntax.

FFmpeg is an extremely powerful command-line tool but difficult to access for non-technical users. Video Convertor bridges this gap by providing an intuitive interface that automatically generates the appropriate FFmpeg commands based on your needs.

### Features

- **Intuitive user interface**: Modern and easy-to-use tkinter interface
- **Professional video conversion**: Full control over conversion parameters
- **Resolution management**:
  - Custom resolution selection (X and Y)
  - Aspect ratio preservation option
  - Predefined resolutions (144p to 8K)
- **Bitrate control**:
  - Adjustable video bitrate (1.5 Mbps to 100 Mbps)
  - Configurable audio bitrate (8k to 320k)
- **Speed presets**: From fastest (ultrafast) to slowest (veryslow) to optimize quality/time
- **Modern codec support**:
  - Video: libx264 (H.264)
  - Audio: AAC
- **MP4 export**: Optimized output format for maximum compatibility

### Prerequisites

- Python 3.x
- FFmpeg installed on your system
- Python libraries:
  - tkinter (usually included with Python)
  - subprocess (standard library)
  - json (standard library)

### Installation

1. **Install FFmpeg**:
   
   **Linux (Ubuntu/Debian)**:
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **macOS**:
   ```bash
   brew install ffmpeg
   ```
   
   **Windows**:
   Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to PATH

2. **Clone the repository**:
   ```bash
   git clone https://github.com/rosignol08/video_convertor.git
   cd video_convertor
   ```

3. **Verify Python installation**:
   ```bash
   python --version
   # or
   python3 --version
   ```

### Usage

1. **Launch the application**:
   ```bash
   python main.py
   # or
   python3 main.py
   ```

2. **Convert a video**:
   - Click on the "Download" (Conversion) button in the main window
   - A new window will open with conversion options
   - Click on "Open File" to select your source video
   - Configure the parameters:
     - **X Resolution**: Video width
     - **Y Resolution**: Video height (or check "keep ratio" to maintain proportions)
     - **Video bitrate**: Video quality (higher = better quality)
     - **Audio bitrate**: Audio quality
     - **Compression speed**: Balance between processing time and quality
     - **Output name**: Output file name (without extension)
   - Click on "Start conversion"

3. **Retrieve your video**:
   - The converted video will be saved in the same directory as the application
   - The file name will be what you specified with a .mp4 extension

### Generated FFmpeg commands

The application generates FFmpeg commands in this form:
```bash
ffmpeg -i "input.mp4" \
  -vf "scale=1920:1080,setsar=1/1" \
  -c:v libx264 \
  -preset slow \
  -b:v 4000000 \
  -c:a aac \
  -b:a 192k \
  "output.mp4"
```

This command:
- Resizes the video to the specified resolution
- Uses H.264 codec for video
- Applies the chosen speed preset
- Configures video and audio bitrate
- Encodes audio to AAC

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing

Contributions are welcome! Feel free to open an issue or pull request.

---

<div align="center">

**Made with ❤️ FFmpeg and python**

[Report Bug](https://github.com/rosignol08/video_convertor/issues) • [Request Feature](https://github.com/rosignol08/video_convertor/issues)

</div>
