from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel

class SettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Player 1 Name:"))
        self.p1_input = QLineEdit("PLAYER 1")
        layout.addWidget(self.p1_input)
        
        layout.addWidget(QLabel("Player 2 Name:"))
        self.p2_input = QLineEdit("PLAYER 2")
        layout.addWidget(self.p2_input)
        
        layout.addWidget(QLabel("Points per Set:"))
        self.pts_limit = QComboBox()
        self.pts_limit.addItems(["11", "21"])
        layout.addWidget(self.pts_limit)
        
        self.apply_btn = QPushButton("APPLY SETTINGS")
        self.apply_btn.setStyleSheet("background-color: orange; font-weight: bold; height: 40px;")
        layout.addWidget(self.apply_btn)

        self.setLayout(layout)