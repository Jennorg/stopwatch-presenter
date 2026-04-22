import os
import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QComboBox, QGroupBox)
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtCore import QTimer, Qt, QUrl, QSize
from PyQt6.QtMultimedia import QSoundEffect

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ControllerWindow(QWidget):
    def __init__(self, logic, presenter):
        super().__init__()
        self.logic = logic
        self.presenter = presenter
        self.init_ui()
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_displays)
        
        # --- SONIDO ---
        self.sound_enabled = True
        self.beep_sound = QSoundEffect()
        self.beep_sound.setSource(QUrl.fromLocalFile(resource_path("assets/beep.wav")))
        self.end_sound = QSoundEffect()
        self.end_sound.setSource(QUrl.fromLocalFile(resource_path("assets/end.wav")))
        
        self.update_displays()

    def create_time_inputs(self, title):
        group = QGroupBox(title)
        layout = QHBoxLayout()
        h = QSpinBox(); h.setRange(0, 23); h.setSuffix("h")
        m = QSpinBox(); m.setRange(0, 59); m.setSuffix("m")
        s = QSpinBox(); s.setRange(0, 59); s.setSuffix("s")
        layout.addWidget(h); layout.addWidget(m); layout.addWidget(s)
        group.setLayout(layout)
        return group, h, m, s

    def init_ui(self):
        self.setWindowTitle("Cronómetro Presenter Pro")
        self.setWindowIcon(QIcon(resource_path("assets/icon.png")))
        self.setMinimumWidth(700)
        
        # Paleta de colores mejorada
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1c2c;
                color: #e0e6ed;
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            }
            QGroupBox {
                border: 1px solid #3d4466;
                border-radius: 12px;
                margin-top: 20px;
                font-weight: bold;
                font-size: 13px;
                color: #00d2ff;
                background-color: #25283d;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px;
            }
            QSpinBox {
                background-color: #1a1c2c;
                border: 1px solid #3d4466;
                border-radius: 6px;
                padding: 6px;
                min-width: 70px;
                font-size: 15px;
                color: white;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border-left: 1px solid #3d4466;
            }
            QPushButton {
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QComboBox {
                background-color: #25283d;
                border: 1px solid #3d4466;
                border-radius: 6px;
                padding: 8px;
                color: #00d2ff;
                font-weight: bold;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: #25283d;
                selection-background-color: #3d4466;
                selection-color: #00d2ff;
                border: 1px solid #3d4466;
                outline: none;
            }
            QLabel#timerDisplay {
                background-color: #0d0e17;
                border-radius: 20px;
                border: 2px solid #25283d;
                margin: 15px 0px;
                padding: 25px;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(25, 25, 25, 25)

        # --- 1. CONFIGURACIÓN DE TIEMPOS ---
        config_layout = QHBoxLayout()
        self.group_main, self.h_in, self.m_in, self.s_in = self.create_time_inputs("TIEMPO TOTAL")
        self.group_y, self.yh_in, self.ym_in, self.ys_in = self.create_time_inputs("LÍMITE AMARILLO")
        self.group_r, self.rh_in, self.rm_in, self.rs_in = self.create_time_inputs("LÍMITE ROJO")
        
        config_layout.addWidget(self.group_main)
        config_layout.addWidget(self.group_y)
        config_layout.addWidget(self.group_r)
        main_layout.addLayout(config_layout)

        # --- 1.5 TIEMPOS RÁPIDOS ---
        quick_times_group = QGroupBox("TIEMPOS RÁPIDOS")
        quick_times_layout = QHBoxLayout()
        for mins in [10, 15, 20, 30, 45]:
            btn = QPushButton(f"{mins}m")
            btn.clicked.connect(lambda checked, m=mins: self.set_quick_time(m))
            btn.setStyleSheet("""
                QPushButton { background-color: #3d4466; color: #e0e6ed; }
                QPushButton:hover { background-color: #4b5585; }
            """)
            quick_times_layout.addWidget(btn)
        quick_times_group.setLayout(quick_times_layout)
        main_layout.addWidget(quick_times_group)

        # --- 2. PANTALLAS Y PROYECCIÓN ---
        screen_group = QGroupBox("PANTALLA DE PROYECCIÓN")
        screen_layout = QHBoxLayout()
        self.screen_combo = QComboBox()
        self.screens = QGuiApplication.screens()
        for i, s in enumerate(self.screens):
            name = "Principal" if s == QGuiApplication.primaryScreen() else f"Monitor {i+1}"
            self.screen_combo.addItem(f"{name} ({s.name()})")
        
        self.btn_launch = QPushButton("   PROYECTAR E INICIAR")
        self.btn_launch.setIcon(QIcon(resource_path("assets/launch.svg")))
        self.btn_launch.setIconSize(QSize(20, 20))
        self.btn_launch.setStyleSheet("""
            QPushButton { background-color: #00d2ff; color: #1a1c2c; }
            QPushButton:hover { background-color: #00b8e6; }
        """)
        self.btn_launch.clicked.connect(self.launch_and_start)

        self.btn_stop_projection = QPushButton("   DETENER")
        self.btn_stop_projection.setIcon(QIcon(resource_path("assets/stop.svg")))
        self.btn_stop_projection.setIconSize(QSize(20, 20))
        self.btn_stop_projection.setStyleSheet("""
            QPushButton { background-color: #3d4466; color: #e0e6ed; }
            QPushButton:hover { background-color: #4b5585; }
            QPushButton:disabled { background-color: #25283d; color: #5a5f7d; }
        """)
        self.btn_stop_projection.clicked.connect(self.stop_presenting)
        self.btn_stop_projection.setEnabled(False)
        
        screen_layout.addWidget(self.screen_combo)
        screen_layout.addWidget(self.btn_launch)
        screen_layout.addWidget(self.btn_stop_projection)
        screen_group.setLayout(screen_layout)
        main_layout.addWidget(screen_group)

        # --- 3. DISPLAY DEL MODERADOR ---
        self.time_label = QLabel("00:00:00")
        self.time_label.setObjectName("timerDisplay")
        self.time_label.setStyleSheet("font-size: 90px; font-family: 'Consolas', 'Courier New'; font-weight: bold; color: white;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.time_label)

        # --- 4. CONTROLES MANUALES ---
        ctrl_layout = QHBoxLayout()
        
        self.play_pause_btn = QPushButton("   PLAY")
        self.play_pause_btn.setIcon(QIcon(resource_path("assets/play.svg")))
        self.play_pause_btn.setIconSize(QSize(24, 24))
        self.play_pause_btn.setStyleSheet("""
            QPushButton { background-color: #00d2ff; color: #1a1c2c; height: 55px; font-size: 18px; }
            QPushButton:hover { background-color: #00b8e6; }
        """)
        self.play_pause_btn.clicked.connect(self.handle_play_pause)

        self.reset_btn = QPushButton("   REINICIAR")
        self.reset_btn.setIcon(QIcon(resource_path("assets/reset.svg")))
        self.reset_btn.setIconSize(QSize(24, 24))
        self.reset_btn.setStyleSheet("""
            QPushButton { background-color: #ff9d00; color: #1a1c2c; height: 55px; font-size: 18px; }
            QPushButton:hover { background-color: #e68e00; }
        """)
        self.reset_btn.clicked.connect(self.handle_reset)

        self.sound_btn = QPushButton("   SONIDO")
        self.sound_btn.setIcon(QIcon(resource_path("assets/volume-high.svg")))
        self.sound_btn.setIconSize(QSize(24, 24))
        self.sound_btn.setStyleSheet("""
            QPushButton { background-color: #9d50bb; color: white; height: 55px; font-size: 18px; }
            QPushButton:hover { background-color: #8a46a5; }
        """)
        self.sound_btn.clicked.connect(self.toggle_sound)

        ctrl_layout.addWidget(self.play_pause_btn)
        ctrl_layout.addWidget(self.reset_btn)
        ctrl_layout.addWidget(self.sound_btn)
        main_layout.addLayout(ctrl_layout)

        self.setLayout(main_layout)
        
        # Valores por defecto
        self.m_in.setValue(5); self.ym_in.setValue(1); self.rs_in.setValue(10)

    # --- FUNCIONES DE LÓGICA Y SINCRONIZACIÓN ---

    def launch_and_start(self):
        """Proyecta la ventana y arranca el cronómetro de inmediato."""
        idx = self.screen_combo.currentIndex()
        target_screen = self.screens[idx]
        
        if self.presenter:
            self.presenter.show()  # Necesario para crear windowHandle antes de cambiar de pantalla
            self.presenter.windowHandle().setScreen(target_screen)
            geom = target_screen.geometry()
            self.presenter.move(geom.left(), geom.top())
            self.presenter.showFullScreen()

        if not self.logic.is_running and self.logic.elapsed_before_pause == 0:
            self.apply_inputs_to_logic()

        if not self.logic.is_running:
            self.logic.toggle_running()
            self.ui_timer.start(100)

        if self.presenter:
            self.btn_stop_projection.setEnabled(True)

        self.update_btn_ui()
        self.update_displays()

    def stop_presenting(self):
        """Detiene la proyección y oculta la pantalla del presentador."""
        if self.presenter:
            self.presenter.stop_presenting()
            self.btn_stop_projection.setEnabled(False)

    def handle_play_pause(self):
        """Maneja el inicio manual o la pausa."""
        if not self.logic.is_running and self.logic.elapsed_before_pause == 0:
            self.apply_inputs_to_logic()

        self.logic.toggle_running()
        self.update_btn_ui()

        if self.logic.is_running:
            self.ui_timer.start(100)
        else:
            self.ui_timer.stop()

        self.update_displays()

    def handle_reset(self):
        """Detiene todo y limpia los contadores."""
        self.logic.reset()
        self.ui_timer.stop()
        self.update_btn_ui()
        self.stop_presenting()
        self.update_displays() # Fuerza a que la pantalla vuelva a su estado original

    def set_quick_time(self, minutes):
        """Establece un tiempo rápido y lo aplica a la lógica."""
        self.h_in.setValue(0)
        self.m_in.setValue(minutes)
        self.s_in.setValue(0)
        
        # Ajustar límites automáticamente (ej. amarillo al 20% y rojo al 10%)
        y_mins = max(1, minutes // 5)
        r_secs = 30 if minutes >= 5 else 10
        
        self.yh_in.setValue(0); self.ym_in.setValue(y_mins); self.ys_in.setValue(0)
        self.rh_in.setValue(0); self.rm_in.setValue(0); self.rs_in.setValue(r_secs)
        
        if not self.logic.is_running:
            self.apply_inputs_to_logic()
            self.update_displays()

    def apply_inputs_to_logic(self):
        """Pasa los valores de los QSpinBox a la lógica interna."""
        self.logic.set_countdown(
            self.h_in.value(), self.m_in.value(), self.s_in.value(),
            self.yh_in.value(), self.ym_in.value(), self.ys_in.value(),
            self.rh_in.value(), self.rm_in.value(), self.rs_in.value()
        )

    def update_btn_ui(self):
        """Cambia el aspecto del botón Play/Pausa según el estado."""
        if self.logic.is_running:
            self.play_pause_btn.setText("   PAUSA")
            self.play_pause_btn.setIcon(QIcon(resource_path("assets/pause.svg")))
            self.play_pause_btn.setStyleSheet("""
                QPushButton { background-color: #ff9d00; color: #1a1c2c; height: 55px; font-size: 18px; }
                QPushButton:hover { background-color: #e68e00; }
            """)
        else:
            self.play_pause_btn.setText("   PLAY")
            self.play_pause_btn.setIcon(QIcon(resource_path("assets/play.svg")))
            self.play_pause_btn.setStyleSheet("""
                QPushButton { background-color: #00d2ff; color: #1a1c2c; height: 55px; font-size: 18px; }
                QPushButton:hover { background-color: #00b8e6; }
            """)

    def update_displays(self):
        """Sincroniza la lógica con las etiquetas de texto visuales."""
        t = self.logic.get_format_time()
        color, blink = self.logic.get_status()
        
        # --- Gestión de Sonido ---
        if self.sound_enabled:
            trigger = self.logic.check_sound_trigger()
            if trigger == "end":
                self.end_sound.play()
            elif trigger in ["yellow", "red"]:
                self.beep_sound.play()

        # Actualiza el reloj del moderador
        mod_color = "white" if color == "#ecf0f1" else color
        self.time_label.setText(t)
        self.time_label.setStyleSheet(f"font-size: 90px; font-family: 'Consolas'; font-weight: bold; color: {mod_color};")
        
        # Actualiza el reloj del público
        if self.presenter and self.presenter.isVisible():
            self.presenter.update_display(t, color, blink and self.logic.is_running)
            
        # Si llega a cero, detener el timer UI automáticamente
        if t == "00:00:00" and self.logic.is_countdown and self.logic.elapsed_before_pause > 0:
            self.ui_timer.stop()
            self.logic.is_running = False
            self.update_btn_ui()

    def toggle_sound(self):
        """Alterna el estado del sonido."""
        self.sound_enabled = not self.sound_enabled
        if self.sound_enabled:
            self.sound_btn.setText("   SONIDO")
            self.sound_btn.setIcon(QIcon(resource_path("assets/volume-high.svg")))
            self.sound_btn.setStyleSheet("""
                QPushButton { background-color: #9d50bb; color: white; height: 55px; font-size: 18px; }
                QPushButton:hover { background-color: #8a46a5; }
            """)
        else:
            self.sound_btn.setText("   SILENCIO")
            self.sound_btn.setIcon(QIcon(resource_path("assets/volume-mute.svg")))
            self.sound_btn.setStyleSheet("""
                QPushButton { background-color: #3d4466; color: #e0e6ed; height: 55px; font-size: 18px; }
                QPushButton:hover { background-color: #4b5585; }
            """)