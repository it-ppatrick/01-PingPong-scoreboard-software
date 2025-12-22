from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel

class ScoreDeckUI(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        
        # Player 1 Column (Purple)
        self.p1_col = QVBoxLayout()
        self.p1_plus = QPushButton("+1")
        self.p1_plus.setStyleSheet("background-color: #7B2CBF; color: white; font-size: 30pt; height: 120px; border-radius: 10px;")
        self.p1_minus = QPushButton("-1")
        self.p1_minus.setStyleSheet("background-color: #333; color: white; height: 40px;")
        self.p1_col.addWidget(self.p1_plus); self.p1_col.addWidget(self.p1_minus)
        
        # Player 2 Column (Gold)
        self.p2_col = QVBoxLayout()
        self.p2_plus = QPushButton("+1")
        self.p2_plus.setStyleSheet("background-color: #FFD700; color: black; font-size: 30pt; height: 120px; border-radius: 10px;")
        self.p2_minus = QPushButton("-1")
        self.p2_minus.setStyleSheet("background-color: #333; color: white; height: 40px;")
        self.p2_col.addWidget(self.p2_plus); self.p2_col.addWidget(self.p2_minus)

        layout.addLayout(self.p1_col); layout.addLayout(self.p2_col)
        self.setLayout(layout)