from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

class WinnerScreen(QLabel):
    def __init__(self):
        super().__init__("WINNER: PLAYER 1")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("font-size: 50pt; font-weight: bold; color: gold;")