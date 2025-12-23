from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class ScoreScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        # Names Row
        self.name_row = QHBoxLayout()
        self.p1_name_lbl = QLabel("PLAYER 1")
        self.p2_name_lbl = QLabel("PLAYER 2")
        for lbl in [self.p1_name_lbl, self.p2_name_lbl]:
            lbl.setStyleSheet("font-size: 30pt; font-weight: bold;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_row.addWidget(self.p1_name_lbl)
        self.name_row.addWidget(self.p2_name_lbl)
        
        # Games Row
        self.games_row = QHBoxLayout()
        self.p1_games_lbl = QLabel("GAMES: 0")
        self.p2_games_lbl = QLabel("GAMES: 0")
        for lbl in [self.p1_games_lbl, self.p2_games_lbl]:
            lbl.setStyleSheet("font-size: 22pt; color: #BBB; font-weight: normal;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.games_row.addWidget(self.p1_games_lbl)
        self.games_row.addWidget(self.p2_games_lbl)
        
        # Points Row
        self.points_row = QHBoxLayout()
        self.p1_score_lbl = QLabel("0")
        self.p2_score_lbl = QLabel("0")
        for lbl in [self.p1_score_lbl, self.p2_score_lbl]:
            lbl.setStyleSheet("font-size: 120pt; font-weight: bold; color: yellow;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.points_row.addWidget(self.p1_score_lbl)
        self.points_row.addWidget(self.p2_score_lbl)
        
        layout.addLayout(self.name_row)
        layout.addLayout(self.games_row)
        layout.addLayout(self.points_row)