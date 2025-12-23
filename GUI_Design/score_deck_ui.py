from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton

class ScoreDeckUI(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        
        self.p1_col = QVBoxLayout()
        self.p1_plus = QPushButton("+1 P1")
        self.p1_minus = QPushButton("-1 P1")
        self.p1_col.addWidget(self.p1_plus)
        self.p1_col.addWidget(self.p1_minus)
        
        self.p2_col = QVBoxLayout()
        self.p2_plus = QPushButton("+1 P2")
        self.p2_minus = QPushButton("-1 P2")
        self.p2_col.addWidget(self.p2_plus)
        self.p2_col.addWidget(self.p2_minus)
        
        self.layout.addLayout(self.p1_col)
        self.layout.addLayout(self.p2_col)
        self.setLayout(self.layout)