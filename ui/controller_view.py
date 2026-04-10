from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QComboBox, QGroupBox)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QTimer, Qt

class ControllerWindow(QWidget):
    def __init__(self, logic, presenter):
        super().__init__()
        self.logic = logic
        self.presenter = presenter
        self.init_ui()
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_displays)

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
        self.setWindowTitle("Vista de Moderador")
        self.setMinimumWidth(500)
        main_layout = QVBoxLayout()

        # --- 1. CONFIGURACIÓN DE TIEMPOS Y LÍMITES ---
        self.group_main, self.h_in, self.m_in, self.s_in = self.create_time_inputs("Tiempo Total")
        self.group_y, self.yh_in, self.ym_in, self.ys_in = self.create_time_inputs("Límite Amarillo (Advertencia)")
        self.group_r, self.rh_in, self.rm_in, self.rs_in = self.create_time_inputs("Límite Rojo (Urgente)")
        
        # Valores por defecto para que no inicie en 0
        self.m_in.setValue(5); self.ym_in.setValue(1); self.rs_in.setValue(10)

        main_layout.addWidget(self.group_main)
        main_layout.addWidget(self.group_y)
        main_layout.addWidget(self.group_r)

        # --- 2. PANTALLAS Y PROYECCIÓN ---
        screen_layout = QHBoxLayout()
        self.screen_combo = QComboBox()
        self.screens = QGuiApplication.screens()
        for i, s in enumerate(self.screens):
            name = "Principal" if s == QGuiApplication.primaryScreen() else f"Monitor {i+1}"
            self.screen_combo.addItem(f"{name} ({s.name()})")
        
        self.btn_launch = QPushButton("PROYECTAR E INICIAR")
        self.btn_launch.setStyleSheet("background-color: #3498db; color: white; height: 35px; font-weight: bold;")
        self.btn_launch.clicked.connect(self.launch_and_start)

        self.btn_stop_projection = QPushButton("DETENER PROYECCIÓN")
        self.btn_stop_projection.setStyleSheet("background-color: #7f8c8d; color: white; height: 35px; font-weight: bold;")
        self.btn_stop_projection.clicked.connect(self.stop_presenting)
        self.btn_stop_projection.setEnabled(False)
        
        screen_layout.addWidget(self.screen_combo)
        screen_layout.addWidget(self.btn_launch)
        screen_layout.addWidget(self.btn_stop_projection)
        main_layout.addLayout(screen_layout)

        # --- 3. DISPLAY DEL MODERADOR ---
        self.time_label = QLabel("00:00:00")
        self.time_label.setStyleSheet("font-size: 70px; font-family: Consolas; font-weight: bold ; color: black;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.time_label)

        # --- 4. CONTROLES MANUALES (RESTABLECIDOS) ---
        ctrl_layout = QHBoxLayout()
        
        self.play_pause_btn = QPushButton("PLAY")
        self.play_pause_btn.setStyleSheet("background-color: #27ae60; color: white; height: 45px; font-weight: bold; font-size: 16px;")
        self.play_pause_btn.clicked.connect(self.handle_play_pause)

        self.reset_btn = QPushButton("REINICIAR")
        self.reset_btn.setStyleSheet("background-color: #c0392b; color: white; height: 45px; font-weight: bold; font-size: 16px;")
        self.reset_btn.clicked.connect(self.handle_reset)

        ctrl_layout.addWidget(self.play_pause_btn)
        ctrl_layout.addWidget(self.reset_btn)
        main_layout.addLayout(ctrl_layout)

        self.setLayout(main_layout)

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
            self.play_pause_btn.setText("PAUSA")
            self.play_pause_btn.setStyleSheet("background-color: #f39c12; color: white; height: 45px; font-weight: bold; font-size: 16px;")
        else:
            self.play_pause_btn.setText("PLAY")
            self.play_pause_btn.setStyleSheet("background-color: #27ae60; color: white; height: 45px; font-weight: bold; font-size: 16px;")

    def update_displays(self):
        """Sincroniza la lógica con las etiquetas de texto visuales."""
        t = self.logic.get_format_time()
        color, blink = self.logic.get_status()
        
        # Actualiza el reloj del moderador
        self.time_label.setText(t)
        self.time_label.setStyleSheet(f"font-size: 70px; font-family: Consolas; font-weight: bold; color: {color};")
        
        # Actualiza el reloj del público
        if self.presenter and self.presenter.isVisible():
            self.presenter.update_display(t, color, blink and self.logic.is_running)
            
        # Si llega a cero, detener el timer UI automáticamente
        if t == "00:00:00" and self.logic.is_countdown and self.logic.elapsed_before_pause > 0:
            self.ui_timer.stop()
            self.logic.is_running = False
            self.update_btn_ui()