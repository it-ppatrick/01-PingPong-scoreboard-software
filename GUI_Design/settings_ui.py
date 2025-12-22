from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton, QLabel

class SettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Player Names
        layout.addWidget(QLabel("Player 1 Name:"))
        self.p1_input = QLineEdit("DANIEL")
        layout.addWidget(self.p1_input)
        
        layout.addWidget(QLabel("Player 2 Name:"))
        self.p2_input = QLineEdit("GUEST")
        layout.addWidget(self.p2_input)
        
        # Match Rules
        layout.addWidget(QLabel("Points per Set:"))
        self.pts_limit = QComboBox()
        self.pts_limit.addItems(["11", "21"])
        self.pts_limit.setCurrentText("21")
        layout.addWidget(self.pts_limit)
        
        # Update Button
        self.apply_btn = QPushButton("APPLY SETTINGS")
        self.apply_btn.setStyleSheet("background-color: #FFA500; color: black; font-weight: bold; height: 40px;")
        layout.addWidget(self.apply_btn)

        self.setLayout(layout)