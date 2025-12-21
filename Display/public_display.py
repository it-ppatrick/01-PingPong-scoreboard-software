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
        
        for view in [self.view_score, self.view_winner, self.view_standby, self.view_welcome]:
            self.stack.addWidget(view)
        
        layout = QVBoxLayout(); layout.addWidget(self.stack); self.setLayout(layout)
        self.stack.setCurrentIndex(3) 

    def set_view(self, index): self.stack.setCurrentIndex(index)

    def update_match(self, f1, f2, s1, s2, g1, g2, target, server):
        v = self.view_score
        v.p1_name.setText(f1.upper()); v.p2_name.setText(f2.upper())
        v.score_label.setText(f"{s1} - {s2}")
        v.game_wins.setText(f"Games: {g1+g2} / {target}")

        # Overtime Detection (11pt game: 10-10, 21pt game: 20-20)
        limit = 11 if "11" in v.game_wins.text() else 21 # Simple detection for now
        if s1 >= limit-1 and s2 >= limit-1:
            v.ot_label.show()
        else:
            v.ot_label.hide()

    def show_winner(self, name, is_game_winner=False):
        self.view_winner.set_mode(is_game_winner)
        self.view_winner.name.setText(name.upper())
        self.set_view(1)