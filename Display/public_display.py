from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from GUI_Design.General import PUBLIC_STYLE

class PublicDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ping Pong Scoreboard - Output")
        self.setStyleSheet(PUBLIC_STYLE)
        
        layout = QVBoxLayout()
        
        # Player 1 Labels with ObjectNames matching the Style Sheet
        self.p1_first = QLabel("DANIEL")
        self.p1_first.setObjectName("FirstNameLabel")
        
        self.p1_last = QLabel("PETREAN")
        self.p1_last.setObjectName("SurnameLabel")
        
        # Score Label
        self.score_label = QLabel("00 - 00")
        self.score_label.setObjectName("ScoreLabel")
        
        # Assemble with spacing
        layout.addStretch()
        layout.addWidget(self.p1_first, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.p1_last, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(40)
        layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)

    def update_match(self, first, last, s1, s2):
        self.p1_first.setText(first.upper())
        self.p1_last.setText(last.upper())
        self.score_label.setText(f"{s1:02d} - {s2:02d}")