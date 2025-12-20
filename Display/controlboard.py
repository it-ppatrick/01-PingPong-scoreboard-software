from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from Database.usernames import load_data, save_data

class ControlBoard(QMainWindow):
    def __init__(self, public_display):
        super().__init__()
        self.display = public_display
        self.setWindowTitle("Match Controller")
        self.setFixedSize(400, 400)

        # Load initial data from your app_data.json
        self.data = load_data()
        
        layout = QVBoxLayout()

        # Inputs for the "Daniel Petrean" look
        self.p1_first = QLineEdit()
        self.p1_first.setPlaceholderText("Firstname (DANIEL)")
        self.p1_last = QLineEdit()
        self.p1_last.setPlaceholderText("Surname (PETREAN)")

        # Scores
        self.s1 = 0
        self.s2 = 0

        # Score Buttons
        score_btn = QPushButton("P1 SCORES (+1)")
        score_btn.setMinimumHeight(60)
        score_btn.clicked.connect(self.add_score)

        # Connect signals for instant updates
        self.p1_first.textChanged.connect(self.sync)
        self.p1_last.textChanged.connect(self.sync)

        layout.addWidget(QLabel("PLAYER 1 DETAILS"))
        layout.addWidget(self.p1_first)
        layout.addWidget(self.p1_last)
        layout.addSpacing(20)
        layout.addWidget(score_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def add_score(self):
        self.s1 += 1
        self.sync()

    def sync(self):
        self.display.update_match(
            self.p1_first.text() or "DANIEL", 
            self.p1_last.text() or "PETREAN", 
            self.s1, 
            self.s2
        )