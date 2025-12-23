from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import Qt

class SettingsUI(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # --- Player Names Section ---
        layout.addWidget(QLabel("<b>Player Names</b>"))
        self.p1_input = QLineEdit(); self.p1_input.setPlaceholderText("Player 1 Name")
        self.p2_input = QLineEdit(); self.p2_input.setPlaceholderText("Player 2 Name")
        layout.addWidget(self.p1_input); layout.addWidget(self.p2_input)

        # --- Match Configuration Section ---
        layout.addWidget(QLabel("<b>Match Settings</b>"))
        
        # Best of X Dropdown
        limit_layout = QHBoxLayout()
        limit_layout.addWidget(QLabel("Match Format:"))
        self.match_limit_box = QComboBox()
        self.match_limit_box.addItems(["Best of 1", "Best of 3", "Best of 5"])
        # Set default to Best of 3 (Index 1)
        self.match_limit_box.setCurrentIndex(1) 
        limit_layout.addWidget(self.match_limit_box)
        layout.addLayout(limit_layout)

        # --- Apply Button ---
        self.apply_btn = QPushButton("Apply Settings")
        self.apply_btn.setStyleSheet("background-color: #7B2CBF; color: white; font-weight: bold; padding: 10px;")
        layout.addWidget(self.apply_btn)
        
        layout.addStretch()