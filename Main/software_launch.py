import sys
import os

# Ensure Python can find the subfolders
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt6.QtWidgets import QApplication
from Display.public_display import PublicDisplay
from Display.ControlBoard.controlboard_launch import ControlBoard

def main():
    app = QApplication(sys.argv)
    
    # Create the windows, but DO NOT show the public_win yet
    public_win = PublicDisplay()
    controller = ControlBoard(public_win)
    
    # Only show the controller at start
    controller.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()