from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QStackedWidget, QLineEdit, QRadioButton, 
                             QListWidget, QFrame, QButtonGroup)
from PyQt6.QtCore import Qt, QTimer

class ControlBoardUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Board - V02.20")
        self.setMinimumSize(450, 650)
        self.setStyleSheet("background-color: #F5F5F5;") # Light gray background like your sketch
        
        self.main_layout = QVBoxLayout(self)
        
        # --- 1. Top Navigation (Tabs) ---
        self.nav_layout = QHBoxLayout()
        self.btn_main = QPushButton("Main Scoring")
        self.btn_settings = QPushButton("Match Settings")
        self.btn_display = QPushButton("Display Settings")
        
        # Style the Nav Tabs
        tab_style = "padding: 8px; font-size: 10pt; border: 1px solid #CCC; background: white;"
        for btn in [self.btn_main, self.btn_settings, self.btn_display]:
            btn.setStyleSheet(tab_style)
            self.nav_layout.addWidget(btn)
        self.main_layout.addLayout(self.nav_layout)

        # --- 2. The Stack (The 3 Screens) ---
        self.stack = QStackedWidget()
        self.scoring_page = self._setup_scoring_page()
        self.settings_page = self._setup_settings_page()
        self.display_page = self._setup_display_page()
        
        self.stack.addWidget(self.scoring_page)
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.display_page)
        self.main_layout.addWidget(self.stack)

        # --- 3. Bottom Status Bar ---
        self.status_bar = QLabel("READY")
        self.status_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_bar.setStyleSheet("""
            background-color: #333; 
            color: white; 
            padding: 10px; 
            font-weight: bold;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)
        self.main_layout.addWidget(self.status_bar)

        # Tab Logic
        self.btn_main.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_settings.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_display.clicked.connect(lambda: self.stack.setCurrentIndex(2))

    def _setup_scoring_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        # Header: Names and Swap
        header = QHBoxLayout()
        self.p1_name_display = QLabel("PLAYER 1")
        self.swap_btn = QPushButton("⇄")
        self.swap_btn.setFixedWidth(40)
        self.p2_name_display = QLabel("PLAYER 2")
        
        for lbl in [self.p1_name_display, self.p2_name_display]:
            lbl.setStyleSheet("font-size: 14pt; font-weight: bold; color: #333;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        header.addWidget(self.p1_name_display); header.addWidget(self.swap_btn); header.addWidget(self.p2_name_display)
        
        # Big Scores
        scores = QHBoxLayout()
        self.s1_huge = QLabel("0"); self.s2_huge = QLabel("0")
        for lbl in [self.s1_huge, self.s2_huge]:
            lbl.setStyleSheet("font-size: 80pt; font-weight: bold; color: #222;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scores.addWidget(self.s1_huge); scores.addWidget(self.s2_huge)

        # Scoring Buttons
        grid = QHBoxLayout()
        # P1 Side
        p1_col = QVBoxLayout()
        self.p1_add = QPushButton("+ 1")
        self.p1_add.setObjectName("p1_add_btn") # For QSS
        self.p1_minus = QPushButton("- 1")
        self.p1_minus.setObjectName("minus_btn")
        p1_col.addWidget(self.p1_add); p1_col.addWidget(self.p1_minus)
        
        # P2 Side
        p2_col = QVBoxLayout()
        self.p2_add = QPushButton("+ 1")
        self.p2_add.setObjectName("p2_add_btn")
        self.p2_minus = QPushButton("- 1")
        p2_minus_style = ""
        self.p2_minus.setObjectName("minus_btn")
        p2_col.addWidget(self.p2_add); p2_col.addWidget(self.p2_minus)
        
        grid.addLayout(p1_col); grid.addLayout(p2_col)

        # Apply General Styling
        page.setStyleSheet("""
            QPushButton#p1_add_btn { background-color: #2ECC71; color: white; height: 80px; font-size: 20pt; border-radius: 10px; }
            QPushButton#p2_add_btn { background-color: #3498DB; color: white; height: 80px; font-size: 20pt; border-radius: 10px; }
            QPushButton#minus_btn { background-color: #2C3E50; color: white; height: 40px; font-size: 12pt; border-radius: 5px; margin-top: 5px;}
        """)

        layout.addLayout(header); layout.addLayout(scores); layout.addLayout(grid)
        
        self.match_status_label = QLabel("START GAME")
        self.match_status_label.setStyleSheet("background-color: #D5D8DC; padding: 15px; font-size: 14pt; border-radius: 5px;")
        self.match_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.match_status_label)
        
        return page

    def _setup_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("<b>PLAYER 1</b>"))
        self.p1_input = QLineEdit(); layout.addWidget(self.p1_input)
        
        layout.addWidget(QLabel("<b>PLAYER 2</b>"))
        self.p2_input = QLineEdit(); layout.addWidget(self.p2_input)
        
        # Points Limit
        layout.addWidget(QLabel("<b>Points per Set</b>"))
        self.pts_group = QButtonGroup(self)
        self.pts_11 = QRadioButton("11 Points"); self.pts_21 = QRadioButton("21 Points")
        self.pts_group.addButton(self.pts_11); self.pts_group.addButton(self.pts_21)
        self.pts_21.setChecked(True)
        layout.addWidget(self.pts_11); layout.addWidget(self.pts_21)

        # Series Length
        layout.addWidget(QLabel("<b>Series Length</b>"))
        self.series_group = QButtonGroup(self)
        self.best_1 = QRadioButton("Best of 1"); self.best_3 = QRadioButton("Best of 3"); self.best_5 = QRadioButton("Best of 5")
        self.series_group.addButton(self.best_1); self.series_group.addButton(self.best_3); self.series_group.addButton(self.best_5)
        self.best_3.setChecked(True)
        layout.addWidget(self.best_1); layout.addWidget(self.best_3); layout.addWidget(self.best_5)
        
        self.apply_settings_btn = QPushButton("Apply Settings")
        self.apply_settings_btn.setStyleSheet("background-color: #F1C40F; padding: 15px; font-weight: bold; border-radius: 5px;")
        layout.addWidget(self.apply_settings_btn)
        
        layout.addStretch()
        return page

    def _setup_display_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<b>Displays</b>"))
        self.display_list = QListWidget(); self.display_list.addItem("Main Display (Connected)")
        layout.addWidget(self.display_list)
        
        self.broadcast_btn = QPushButton("START BROADCAST")
        self.broadcast_btn.setStyleSheet("background-color: #E67E22; color: white; padding: 20px; font-weight: bold; border-radius: 10px;")
        layout.addWidget(self.broadcast_btn)
        
        layout.addStretch()
        return page

    def flash_status(self, message):
        """Standard 5-second green feedback."""
        self.status_bar.setText(message)
        self.status_bar.setStyleSheet("background-color: #2ECC71; color: white; padding: 10px; font-weight: bold;")
        QTimer.singleShot(5000, lambda: self.status_bar.setStyleSheet("background-color: #333; color: white; padding: 10px;"))
        QTimer.singleShot(5000, lambda: self.status_bar.setText("MATCH IN PROGRESS"))