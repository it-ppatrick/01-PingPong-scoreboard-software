from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class SetWinnerScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.header = QLabel("SET COMPLETE")
        self.header.setStyleSheet("font-size: 30pt; color: #2ECC71; font-weight: bold;")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.result_label = QLabel("PLAYER 1 wins the set")
        self.result_label.setStyleSheet("font-size: 40pt; font-weight: bold; color: white;")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.score_label = QLabel("21 - 15")
        self.score_label.setStyleSheet("font-size: 60pt; font-weight: bold; color: yellow;")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(self.header)
        layout.addWidget(self.result_label)
        layout.addWidget(self.score_label)
        layout.addStretch()