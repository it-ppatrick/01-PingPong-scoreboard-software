from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QApplication

class DisplaysTab(QWidget):
    def __init__(self, public_display):
        super().__init__()
        self.display = public_display
        layout = QVBoxLayout()
        self.screen_combo = QComboBox()
        for i in range(len(QApplication.screens())): self.screen_combo.addItem(f"Monitor {i+1}")
        layout.addWidget(QLabel("Select Monitor:")); layout.addWidget(self.screen_combo)
        
        self.toggle_btn = QPushButton("LAUNCH SCREEN")
        self.toggle_btn.clicked.connect(self.handle_toggle)
        layout.addWidget(self.toggle_btn)
        self.setLayout(layout)
        self.update_style()

    def handle_toggle(self):
        if self.display.isVisible():
            self.display.hide()
        else:
            self.display.setGeometry(QApplication.screens()[self.screen_combo.currentIndex()].geometry())
            self.display.showFullScreen()
            # V01.03-IL: Explicitly show Welcome Screen on first launch
            self.display.set_view(3) 
        self.update_style()

    def update_style(self):
        visible = self.display.isVisible()
        self.toggle_btn.setText("CLOSE SCREEN" if visible else "LAUNCH SCREEN")
        color = "#f44336" if visible else "#4CAF50"
        self.toggle_btn.setStyleSheet(f"background-color: {color}; color: white; height: 50px; font-weight: bold;")