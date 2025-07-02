import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QFileDialog, QSlider, QProgressBar, QHBoxLayout
)
from PyQt5.QtCore import Qt, QProcess

class VideoResizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Redimensionneur de vidéo")
        self.setMinimumWidth(450)

        self.layout = QVBoxLayout()

        self.file_label = QLabel("Aucune vidéo sélectionnée")
        self.layout.addWidget(self.file_label)

        self.browse_button = QPushButton("Choisir une vidéo")
        self.browse_button.clicked.connect(self.select_video)
        self.layout.addWidget(self.browse_button)

        self.output_folder_label = QLabel("Dossier de sortie non sélectionné")
        self.layout.addWidget(self.output_folder_label)

        self.output_folder_button = QPushButton("Choisir dossier de sortie")
        self.output_folder_button.clicked.connect(self.select_output_folder)
        self.layout.addWidget(self.output_folder_button)

        self.width_slider = self.create_slider("Largeur", 100, 1920, 640)
        self.height_slider = self.create_slider("Hauteur", 100, 1080, 480)

        self.resize_button = QPushButton("Redimensionner la vidéo")
        self.resize_button.clicked.connect(self.resize_video)
        self.layout.addWidget(self.resize_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.log_label = QLabel("")
        self.layout.addWidget(self.log_label)

        self.setLayout(self.layout)
        self.video_path = None
        self.output_folder = None
        self.video_duration = 0.0  # en secondes

        self.process = None

    def create_slider(self, label_text, min_val, max_val, default):
        label = QLabel(f"{label_text}: {default}")
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.valueChanged.connect(lambda value: label.setText(f"{label_text}: {value}"))

        self.layout.addWidget(label)
        self.layout.addWidget(slider)

        return slider

    def select_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir une vidéo", "", "Vidéo (*.mp4 *.mov *.avi)")
        if path:
            self.video_path = path
            self.file_label.setText(f"Fichier sélectionné : {path}")
            self.video_duration = self.get_video_duration(path)
            self.log_label.setText(f"Durée vidéo : {self.video_duration:.2f} secondes")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choisir dossier de sortie")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Dossier de sortie : {folder}")

    def get_video_duration(self, path):
        # Utilise ffprobe pour obtenir la durée
        import subprocess
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format=duration", "-of",
                 "default=noprint_wrappers=1:nokey=1", path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            duration_str = result.stdout.decode().strip()
            return float(duration_str)
        except Exception:
            return 0.0

    def resize_video(self):
        if not self.video_path:
            self.log_label.setText("❌ Aucun fichier vidéo sélectionné.")
            return
        if not self.output_folder:
            self.log_label.setText("❌ Aucun dossier de sortie sélectionné.")
            return

        w = self.width_slider.value()
        h = self.height_slider.value()

        # Corriger pour être pair
        w = w if w % 2 == 0 else w - 1
        h = h if h % 2 == 0 else h - 1

        output_path = f"{self.output_folder}/output_resized.mp4"

        cmd = [
            "ffmpeg",
            "-i", self.video_path,
            "-vf", f"scale={w}:{h}",
            "-c:a", "copy",
            "-y",  # overwrite
            output_path
        ]

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.on_ready_read)
        self.process.finished.connect(self.on_finished)
        self.progress_bar.setValue(0)
        self.log_label.setText("🔄 Traitement en cours...")

        self.process.start(cmd[0], cmd[1:])

    def on_ready_read(self):
        output = self.process.readAllStandardOutput().data().decode()
        # Recherche dans la sortie ffmpeg la progression (time=00:00:xx.xx)
        match = re.search(r'time=(\d+):(\d+):(\d+).(\d+)', output)
        if not match:
            # Essayer une autre regex plus simple
            match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', output)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3) + '.' + match.group(4) if len(match.groups()) > 3 else match.group(3))
            current_time = hours * 3600 + minutes * 60 + seconds
            if self.video_duration > 0:
                percent = int((current_time / self.video_duration) * 100)
                self.progress_bar.setValue(percent)

    def on_finished(self):
        self.progress_bar.setValue(100)
        self.log_label.setText("✅ Traitement terminé ! Vidéo sauvegardée.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoResizer()
    window.show()
    sys.exit(app.exec())
