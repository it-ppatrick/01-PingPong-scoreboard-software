from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class HypeScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.match_title = QLabel("MATCH PREVIEW")
        self.match_title.setStyleSheet("font-size: 25pt; color: #F1C40F; font-weight: bold;")
        self.match_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.players_label = QLabel("PLAYER 1 vs PLAYER 2")
        self.players_label.setStyleSheet("font-size: 50pt; font-weight: bold; color: white;")
        self.players_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.details_label = QLabel("Best of 3 - 21 Points")
        self.details_label.setStyleSheet("font-size: 30pt; color: #BDC3C7;")
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
        layout.addWidget(self.match_title)
        layout.addWidget(self.players_label)
        layout.addWidget(self.details_label)
        layout.addStretch()