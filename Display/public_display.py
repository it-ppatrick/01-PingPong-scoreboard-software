from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from GUI_Design.General import PUBLIC_STYLE
from Display.states import ScoreboardView, WinnerView, StandbyView, WelcomeView

class PublicDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scoreboard Output")
        self.setStyleSheet(PUBLIC_STYLE)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        self.stack = QStackedWidget()
        self.view_score = ScoreboardView()
        self.view_winner = WinnerView()
        self.view_standby = StandbyView()
        self.view_welcome = WelcomeView()
        
        self.stack.addWidget(self.view_score)   # 0
        self.stack.addWidget(self.view_winner)  # 1
        self.stack.addWidget(self.view_standby) # 2
        self.stack.addWidget(self.view_welcome) # 3
        
        layout = QVBoxLayout(); layout.addWidget(self.stack); self.setLayout(layout)
        self.stack.setCurrentIndex(3) # Start on Welcome Screen

    def set_view(self, index): self.stack.setCurrentIndex(index)

    def update_match(self, f1, f2, s1, s2, g1, g2, target, server):
        v = self.view_score
        v.p1_name.setText(f1.upper()); v.p2_name.setText(f2.upper())
        v.score_label.setText(f"{s1} - {s2}")
        v.game_wins.setText(f"{g1+g2} / {target}")

    def show_winner(self, name, is_game_winner=False):
        self.view_winner.title.setText("GAME WINNER" if is_game_winner else "MATCH WINNER")
        self.view_winner.name.setText(name.upper())
        self.set_view(1)