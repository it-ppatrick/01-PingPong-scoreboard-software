from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class LiveStatusMonitor(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.status_lbl = QLabel("SCREEN: WELCOME")
        self.status_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_lbl.setStyleSheet("""
            background-color: #7B2CBF; 
            color: white; 
            font-weight: bold; 
            padding: 5px; 
            border-radius: 5px;
        """)
        layout.addWidget(self.status_lbl)
        self.setLayout(layout)

    def update_status(self, state_name, color="#7B2CBF"):
        self.status_lbl.setText(f"SCREEN: {state_name.upper()}")
        self.status_lbl.setStyleSheet(f"""
            background-color: {color}; 
            color: white; 
            font-weight: bold; 
            padding: 5px; 
            border-radius: 5px;
        """)