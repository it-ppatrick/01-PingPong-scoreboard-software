from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QStackedWidget, QHBoxLayout
from PyQt6.QtCore import Qt

class AudienceUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Public Scoreboard")
        self.setMinimumSize(800, 480)
        self.setStyleSheet("background-color: black; color: white;")
        
        self.main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget() 
        
        # --- 1. SCREEN: WELCOME (Index 0) ---
        self.welcome_screen = QLabel("WELCOME TO THE MATCH")
        self.welcome_screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_screen.setStyleSheet("font-size: 40pt; font-weight: bold; color: #7B2CBF;")
        
        # --- 2. SCREEN: LIVE SCOREBOARD (Index 1) ---
        self.score_screen = QWidget()
        score_layout = QVBoxLayout(self.score_screen)
        
        # Names Row - FIXED: Added self.
        self.name_row = QHBoxLayout()
        self.p1_name_lbl = QLabel("PLAYER 1")
        self.p2_name_lbl = QLabel("PLAYER 2")
        for lbl in [self.p1_name_lbl, self.p2_name_lbl]:
            lbl.setStyleSheet("font-size: 30pt; font-weight: bold;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_row.addWidget(self.p1_name_lbl)
        self.name_row.addWidget(self.p2_name_lbl)
        
        # Games/Sets Row - FIXED: Added self.
        self.games_row = QHBoxLayout()
        self.p1_games_lbl = QLabel("GAMES: 0")
        self.p2_games_lbl = QLabel("GAMES: 0")
        for lbl in [self.p1_games_lbl, self.p2_games_lbl]:
            lbl.setStyleSheet("font-size: 22pt; color: #BBB; font-weight: normal;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.games_row.addWidget(self.p1_games_lbl)
        self.games_row.addWidget(self.p2_games_lbl)
        
        # Points Row - FIXED: Added self.
        self.points_row = QHBoxLayout()
        self.p1_score_lbl = QLabel("0")
        self.p2_score_lbl = QLabel("0")
        for lbl in [self.p1_score_lbl, self.p2_score_lbl]:
            lbl.setStyleSheet("font-size: 120pt; font-weight: bold; color: yellow;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.points_row.addWidget(self.p1_score_lbl)
        self.points_row.addWidget(self.p2_score_lbl)
        
        # Assemble the Score Screen
        score_layout.addLayout(self.name_row)
        score_layout.addLayout(self.games_row)
        score_layout.addLayout(self.points_row)
        
        # --- 3. SCREEN: WINNER (Index 2) ---
        self.winner_screen = QLabel("WINNER: PLAYER 1")
        self.winner_screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.winner_screen.setStyleSheet("font-size: 50pt; font-weight: bold; color: gold;")

        # Add all to stack
        self.stack.addWidget(self.welcome_screen)
        self.stack.addWidget(self.score_screen)
        self.stack.addWidget(self.winner_screen)
        
        self.main_layout.addWidget(self.stack)

    def set_visual_flip(self, is_flipped):
        """Item 5: Swaps the player positions on screen by reversing layout direction."""
        direction = QHBoxLayout.Direction.RightToLeft if is_flipped else QHBoxLayout.Direction.LeftToRight
        
        self.name_row.setDirection(direction)
        self.games_row.setDirection(direction)
        self.points_row.setDirection(direction)