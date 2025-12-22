class ServeManager:
    """Manages server rotation based on total points played."""
    
    @staticmethod
    def calculate_server(score1, score2, points_per_side=5):
        """
        Determines who should serve based on total points.
        Standard: 5 serves each. 
        Overtime/Deuce: 1 serve each.
        """
        total_points = score1 + score2
        
        # Deuce/Overtime Logic: If both players reach 20 (for 21pt game), 
        # rotation usually shifts to 1 serve each.
        # For simplicity in this engine, we stick to the 5-point block:
        
        # total // 5 gives us the 'block' number. 
        # Even blocks = Initial Server, Odd blocks = Second Player.
        current_block = total_points // points_per_side
        
        if current_block % 2 == 0:
            return 1 # Player 1
        else:
            return 2 # Player 2