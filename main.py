from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QFileDialog, QSlider, QProgressBar, QHBoxLayout, QCheckBox, QComboBox
)
from PyQt5.QtCore import Qt, QProcess
import sys
import re
import subprocess

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

        # Checkbox garder ratio
        self.keep_ratio_checkbox = QCheckBox("Garder le ratio de la vidéo originale")
        self.keep_ratio_checkbox.setChecked(True)
        self.layout.addWidget(self.keep_ratio_checkbox)

        # Sliders + labels
        self.width_label = QLabel("Largeur: 640")
        self.width_slider = self.create_slider(100, 1920, 640, self.on_width_changed)
        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_slider)

        self.height_label = QLabel("Hauteur: 480")
        self.height_slider = self.create_slider(100, 1080, 480, self.on_height_changed)
        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_slider)

        self.resize_button = QPushButton("Redimensionner la vidéo")
        self.resize_button.clicked.connect(self.resize_video)
        self.layout.addWidget(self.resize_button)

        self.progress_bar = QProgressBar()
        
        self.progress_layout = QHBoxLayout()
        self.progress_layout.addWidget(self.progress_bar)
        
        self.speed_label = QLabel("Vitesse : 0x")
        self.speed_label.setFixedWidth(80)
        self.progress_layout.addWidget(self.speed_label)
        
        self.layout.addLayout(self.progress_layout)

        #self.layout.addWidget(self.progress_bar)

        self.log_label = QLabel("")
        self.layout.addWidget(self.log_label)

        self.setLayout(self.layout)
        self.video_path = None
        self.output_folder = None
        self.video_duration = 0.0  # secondes
        self.ratio = 4/3  # ratio par défaut

        self.process = None

        # Pour éviter boucle infinie lors des updates automatiques
        self.updating_slider = False

        self.gpu_accel_combo = QComboBox()
        self.gpu_accel_combo.addItems(["Aucune", "NVIDIA (NVENC)", "AMD (AMF)"])
        self.layout.insertWidget(self.layout.indexOf(self.resize_button), self.gpu_accel_combo)


    def create_slider(self, min_val, max_val, default, slot):
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(default)
        slider.valueChanged.connect(slot)
        return slider

    def select_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choisir une vidéo", "", "Vidéo (*.mp4 *.mov *.avi)")
        if path:
            self.video_path = path
            self.file_label.setText(f"Fichier sélectionné : {path}")
            self.video_duration = self.get_video_duration(path)
            self.log_label.setText(f"Durée vidéo : {self.video_duration:.2f} secondes")

            # Récupérer résolution originale pour ratio
            w, h = self.get_video_resolution(path)
            if w and h:
                self.ratio = w / h
                # Initialiser sliders en fonction de la vidéo
                self.updating_slider = True
                self.width_slider.setValue(w if w <= 1920 else 1920)
                self.height_slider.setValue(h if h <= 1080 else 1080)
                self.width_label.setText(f"Largeur: {self.width_slider.value()}")
                self.height_label.setText(f"Hauteur: {self.height_slider.value()}")
                self.updating_slider = False

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choisir dossier de sortie")
        if folder:
            self.output_folder = folder
            self.output_folder_label.setText(f"Dossier de sortie : {folder}")

    def get_video_duration(self, path):
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

    def get_video_resolution(self, path):
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-select_streams", "v:0",
                 "-show_entries", "stream=width,height",
                 "-of", "csv=s=x:p=0", path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT)
            res = result.stdout.decode().strip()
            w, h = res.split('x')
            return int(w), int(h)
        except Exception:
            return None, None

    def on_width_changed(self, value):
        if self.updating_slider:
            return
        self.width_label.setText(f"Largeur: {value}")
        if self.keep_ratio_checkbox.isChecked():
            self.updating_slider = True
            new_height = int(value / self.ratio)
            new_height = new_height if new_height % 2 == 0 else new_height - 1
            new_height = max(100, min(new_height, 1080))
            self.height_slider.setValue(new_height)
            self.height_label.setText(f"Hauteur: {new_height}")
            self.updating_slider = False

    def on_height_changed(self, value):
        if self.updating_slider:
            return
        self.height_label.setText(f"Hauteur: {value}")
        if self.keep_ratio_checkbox.isChecked():
            self.updating_slider = True
            new_width = int(value * self.ratio)
            new_width = new_width if new_width % 2 == 0 else new_width - 1
            new_width = max(100, min(new_width, 1920))
            self.width_slider.setValue(new_width)
            self.width_label.setText(f"Largeur: {new_width}")
            self.updating_slider = False

    def resize_video(self):
        if not self.video_path:
            self.log_label.setText("❌ Aucun fichier vidéo sélectionné.")
            return
        if not self.output_folder:
            self.log_label.setText("❌ Aucun dossier de sortie sélectionné.")
            return

        w = self.width_slider.value()
        h = self.height_slider.value()

        w = w if w % 2 == 0 else w - 1
        h = h if h % 2 == 0 else h - 1

        output_path = f"{self.output_folder}/output_resized.mp4"

        gpu_choice = self.gpu_accel_combo.currentText()
        cmd = ["ffmpeg", "-y"]

        if gpu_choice == "NVIDIA (NVENC)":
            cmd += ["-hwaccel", "cuda", "-i", self.video_path, "-vf", f"scale={w}:{h}", "-c:v", "h264_nvenc", "-c:a", "copy", output_path]
        elif gpu_choice == "AMD (AMF)":
            cmd += ["-hwaccel", "dxva2", "-i", self.video_path, "-vf", f"scale={w}:{h}", "-c:v", "h264_amf", "-c:a", "copy", output_path]
        else:
            cmd += ["-i", self.video_path, "-vf", f"scale={w}:{h}", "-c:a", "copy", output_path]

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.on_ready_read)
        self.process.finished.connect(self.on_finished)
        self.progress_bar.setValue(0)
        self.log_label.setText("🔄 Traitement en cours...")

        self.process.start(cmd[0], cmd[1:])

    def on_ready_read(self):
        output = self.process.readAllStandardOutput().data().decode()

        # Mise à jour du log
        self.log_label.setText(output)

        # Extraction temps
        match = re.search(r'time=(\d+):(\d+):(\d+)[\.,](\d+)', output)
        if not match:
            match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', output)
        if match:
            hours = int(match.group(1))
            minutes = int(match.group(2))
            seconds = float(match.group(3) + '.' + (match.group(4) if len(match.groups()) > 3 else '0'))
            current_time = hours * 3600 + minutes * 60 + seconds
            if self.video_duration > 0:
                percent = int((current_time / self.video_duration) * 100)
                self.progress_bar.setValue(percent)

        # Extraction vitesse
        speed_match = re.search(r"speed=([\d\.]+)x", output)
        if speed_match:
            speed = speed_match.group(1)
            self.speed_label.setText(f"Vitesse : {speed}x")

    def on_finished(self):
        self.progress_bar.setValue(100)
        self.log_label.setText("✅ Traitement terminé ! Vidéo sauvegardée.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoResizer()
    window.show()
    sys.exit(app.exec())
