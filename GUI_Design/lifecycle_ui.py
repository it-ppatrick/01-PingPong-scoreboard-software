from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout

class LifecycleUI(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.start_btn = QPushButton("START MATCH")
        self.start_btn.setStyleSheet("background-color: #4CAF50; color: white; height: 60px; font-weight: bold;")
        
        self.prep_btn = QPushButton("PREPARE NEXT MATCH")
        self.prep_btn.setStyleSheet("background-color: #2196F3; color: white; height: 60px; font-weight: bold;")
        self.prep_btn.hide()

        self.confirm_widget = QWidget()
        self.confirm_widget.hide()
        conf_layout = QVBoxLayout(self.confirm_widget)
        self.conf_label = QLabel("Confirm Winner?")
        
        btn_row = QHBoxLayout()
        self.yes_btn = QPushButton("Confirm Win")
        self.yes_btn.setStyleSheet("background-color: green; color: white; height: 40px;")
        self.no_btn = QPushButton("Cancel / Undo")
        self.no_btn.setStyleSheet("background-color: red; color: white; height: 40px;")
        
        btn_row.addWidget(self.yes_btn)
        btn_row.addWidget(self.no_btn)
        conf_layout.addWidget(self.conf_label)
        conf_layout.addLayout(btn_row)

        self.layout.addWidget(self.start_btn)
        self.layout.addWidget(self.prep_btn)
        self.layout.addWidget(self.confirm_widget)
        self.setLayout(self.layout)