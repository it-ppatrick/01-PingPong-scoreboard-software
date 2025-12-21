from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class WelcomeView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        welcome = QLabel("WELCOME")
        welcome.setStyleSheet("color: white; font-size: 100pt; font-weight: bold;")
        subtext = QLabel("Game starting soon")
        subtext.setStyleSheet("color: #7B2CBF; font-size: 40pt;")
        layout.addStretch(); layout.addWidget(welcome, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtext, alignment=Qt.AlignmentFlag.AlignCenter); layout.addStretch()
        self.setLayout(layout)

class StandbyView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("GAME STARTING SOON")
        label.setStyleSheet("color: #7B2CBF; font-size: 60pt; font-weight: bold;")
        layout.addStretch(); layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter); layout.addStretch()
        self.setLayout(layout)

class ScoreboardView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        top = QHBoxLayout()
        
        # Names with Ball Indicators
        self.p1_container = QVBoxLayout()
        self.p1_name = QLabel(); self.p1_name.setObjectName("NameBox")
        self.p1_ball = QLabel("⚪"); self.p1_ball.setStyleSheet("font-size: 30pt; color: yellow;")
        self.p1_ball.hide()
        self.p1_container.addWidget(self.p1_name); self.p1_container.addWidget(self.p1_ball, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.p2_container = QVBoxLayout()
        self.p2_name = QLabel(); self.p2_name.setObjectName("NameBox")
        self.p2_ball = QLabel("⚪"); self.p2_ball.setStyleSheet("font-size: 30pt; color: yellow;")
        self.p2_ball.hide()
        self.p2_container.addWidget(self.p2_name); self.p2_container.addWidget(self.p2_ball, alignment=Qt.AlignmentFlag.AlignRight)

        top.addLayout(self.p1_container)
        top.addStretch()
        top.addLayout(self.p2_container)

        score_v = QVBoxLayout()
        self.ot_label = QLabel("OVERTIME")
        self.ot_label.setStyleSheet("color: #FF4500; font-size: 40pt; font-weight: bold;")
        self.ot_label.hide() 
        self.score_label = QLabel(); self.score_label.setObjectName("ScoreLabel")
        self.game_wins = QLabel(); self.game_wins.setObjectName("GameWinLabel")
        score_v.addWidget(self.ot_label, alignment=Qt.AlignmentFlag.AlignCenter)
        score_v.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)
        score_v.addWidget(self.game_wins, alignment=Qt.AlignmentFlag.AlignRight)

        layout.addLayout(top); layout.addStretch(); layout.addLayout(score_v); layout.addStretch()
        self.setLayout(layout)

class WinnerView(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        # Trophy Row for Game Winners
        self.trophy_label = QLabel("🏆  🏆  🏆")
        self.trophy_label.setStyleSheet("font-size: 80pt;")
        self.trophy_label.hide()

        self.title = QLabel("MATCH WINNER")
        self.title.setStyleSheet("color: #FFD700; font-size: 40pt; font-weight: bold;")
        
        self.name = QLabel("PLAYER")
        self.name.setStyleSheet("color: white; font-size: 110pt; font-weight: bold;")
        
        self.layout.addStretch()
        self.layout.addWidget(self.trophy_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.name, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_mode(self, is_game_winner):
        if is_game_winner:
            self.title.setText("🏆 GAME CHAMPION 🏆")
            self.title.setStyleSheet("color: #FFD700; font-size: 60pt; font-weight: bold; text-shadow: 2px 2px #000;")
            self.trophy_label.show()
            self.setStyleSheet("background-color: #1a1a1a; border: 10px solid #FFD700;") # Added golden border
        else:
            self.title.setText("MATCH WINNER")
            self.title.setStyleSheet("color: #C0C0C0; font-size: 40pt; font-weight: bold;") # Silver for matches
            self.trophy_label.hide()
            self.setStyleSheet("background-color: #0a0a0a; border: none;")