import sys
import os
from PyQt6.QtWidgets import QApplication

# Force Python to see the root directory for imports
root_path = os.path.dirname(os.path.abspath(__file__))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

try:
    from Database.match_logic import MatchEngine
    from Database.settings_store import SettingsStore
    from ControlBoard.main_hub import MainControlBoard
    from AudienceView.manager import AudienceManager
except ImportError as e:
    print(f"Critical Import Error: {e}")
    sys.exit(1)

def main():
    app = QApplication(sys.argv)

    # 1. Initialize the Brain
    engine = MatchEngine()
    settings = SettingsStore(engine)

    # 2. Initialize the Audience View
    audience = AudienceManager(engine)

    # 3. Define the Triggers (The Glue)
    triggers = {
        'sync': audience.update_display,
        'live': lambda: audience.switch_to(1),
        'standby': lambda: audience.switch_to(0),
        'swap': audience.swap_sides, # ADD THIS FOR ITEM 5
        'winner': lambda is_game_winner: audience.switch_to(
            2, 
            winner_text=f"CHAMPION: {engine.p1_name if engine.g1 > engine.g2 else engine.p2_name}" 
            if is_game_winner else "SET COMPLETE"
        )
    }

    # 4. Launch the Control Board
    control_board = MainControlBoard(engine, settings, triggers)
    
    control_board.show()
    audience.show()
    
    audience.update_display()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()