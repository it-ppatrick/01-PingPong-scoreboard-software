from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class WelcomeView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        welcome = QLabel("WELCOME")
        welcome.setStyleSheet("color: white; font-size: 100pt; font-weight: bold;")
        subtext = QLabel("Match starting soon")
        subtext.setStyleSheet("color: #7B2CBF; font-size: 40pt;")
        
        layout.addStretch()
        layout.addWidget(welcome, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtext, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

class StandbyView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("MATCH STARTING SOON")
        label.setStyleSheet("color: #7B2CBF; font-size: 60pt; font-weight: bold;")
        layout.addStretch()
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.setLayout(layout)

class ScoreboardView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        top = QHBoxLayout()
        self.p1_name = QLabel(); self.p1_name.setObjectName("NameBox")
        self.p2_name = QLabel(); self.p2_name.setObjectName("NameBox")
        top.addWidget(self.p1_name, alignment=Qt.AlignmentFlag.AlignLeft)
        top.addStretch()
        top.addWidget(self.p2_name, alignment=Qt.AlignmentFlag.AlignRight)

        score_v = QVBoxLayout()
        self.score_label = QLabel(); self.score_label.setObjectName("ScoreLabel")
        self.game_wins = QLabel(); self.game_wins.setObjectName("GameWinLabel")
        score_v.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)
        score_v.addWidget(self.game_wins, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(top); layout.addStretch(); layout.addLayout(score_v); layout.addStretch()
        self.setLayout(layout)

class WinnerView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.title = QLabel("MATCH WINNER")
        self.title.setStyleSheet("color: #FFD700; font-size: 40pt; font-weight: bold;")
        self.name = QLabel("PLAYER")
        self.name.setStyleSheet("color: white; font-size: 100pt; font-weight: bold;")
        layout.addStretch(); layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignCenter); layout.addStretch()
        self.setLayout(layout)