from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QApplication

class DisplaysTab(QWidget):
    def __init__(self, public_display):
        super().__init__()
        self.display = public_display
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("<b>SCREEN CONFIGURATION</b>"))
        self.screen_combo = QComboBox()
        self.refresh_screens()
        layout.addWidget(self.screen_combo)
        
        self.toggle_btn = QPushButton("LAUNCH SCREEN")
        self.toggle_btn.clicked.connect(self.handle_toggle)
        layout.addWidget(self.toggle_btn)
        
        layout.addStretch()
        self.setLayout(layout)
        self.update_style()

    def refresh_screens(self):
        self.screen_combo.clear()
        for i, scr in enumerate(QApplication.screens()):
            self.screen_combo.addItem(f"Monitor {i+1}")

    def handle_toggle(self):
        if self.display.isVisible():
            self.display.hide()
        else:
            idx = self.screen_combo.currentIndex()
            screens = QApplication.screens()
            if idx < len(screens):
                self.display.setGeometry(screens[idx].geometry())
                self.display.showFullScreen()
                self.display.set_view(0)
        self.update_style()

    def update_style(self):
        if self.display.isVisible():
            self.toggle_btn.setText("CLOSE SCREEN")
            self.toggle_btn.setStyleSheet("background-color: #f44336; color: white; height: 50px; font-weight: bold;")
        else:
            self.toggle_btn.setText("LAUNCH SCREEN")
            self.toggle_btn.setStyleSheet("background-color: #4CAF50; color: white; height: 50px; font-weight: bold;")