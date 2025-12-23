from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout
from GUI_Design.AudienceScreens.welcome_screen import WelcomeScreen
from GUI_Design.AudienceScreens.score_screen import ScoreScreen
from GUI_Design.AudienceScreens.winner_screen import WinnerScreen
# ADD THESE TWO IMPORTS TO RESOLVE THE NAMEERROR
from GUI_Design.AudienceScreens.hype_screen import HypeScreen
from GUI_Design.AudienceScreens.set_winner_screen import SetWinnerScreen

class AudienceUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Public Scoreboard")
        self.setMinimumSize(800, 480)
        self.setStyleSheet("background-color: black; color: white;")
        
        self.main_layout = QVBoxLayout(self)
        self.stack = QStackedWidget() 
        
        # Initialize separate screen files
        self.welcome_page = WelcomeScreen()
        self.score_page = ScoreScreen()
        self.winner_page = WinnerScreen()
        self.hype_page = HypeScreen()         # Now defined via import
        self.set_winner_page = SetWinnerScreen() # Now defined via import
        
        self.stack.addWidget(self.welcome_page)    # Index 0
        self.stack.addWidget(self.score_page)      # Index 1
        self.stack.addWidget(self.winner_page)     # Index 2 (Champion)
        self.stack.addWidget(self.hype_page)       # Index 3
        self.stack.addWidget(self.set_winner_page) # Index 4
        
        self.main_layout.addWidget(self.stack)

    def set_visual_flip(self, is_flipped):
        """Item 5: Swaps player positions on the score page."""
        direction = QHBoxLayout.Direction.RightToLeft if is_flipped else QHBoxLayout.Direction.LeftToRight
        self.score_page.name_row.setDirection(direction)
        self.score_page.games_row.setDirection(direction)
        self.score_page.points_row.setDirection(direction)