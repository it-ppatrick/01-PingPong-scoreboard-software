from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class WelcomeScreen(QLabel):
    def __init__(self):
        super().__init__("WELCOME TO THE MATCH")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("font-size: 40pt; font-weight: bold; color: #7B2CBF;")