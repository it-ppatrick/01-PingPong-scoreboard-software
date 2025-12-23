from Database.serve_logic import ServeManager

class MatchEngine:
    def __init__(self):
        self.s1, self.s2 = 0, 0
        self.g1, self.g2 = 0, 0
        
        # ADD THESE TWO LINES
        self.p1_name = "PLAYER 1"
        self.p2_name = "PLAYER 2"
        
        self.starting_server = 1 
        self.server = 1
        self.pts_limit = 21 
        self.points_per_side = 5

    def add_point(self, player):
        """Adds point and updates server based on total score."""
        if player == 1: self.s1 += 1
        else: self.s2 += 1
        self.update_server()

    def undo_point(self, player):
        """Subtracts point and updates server based on total score."""
        if player == 1: self.s1 = max(0, self.s1 - 1)
        else: self.s2 = max(0, self.s2 - 1)
        self.update_server()

    def update_server(self):
        """
        Asks ServeManager for the correct server based on total score.
        If you manually swapped the server, we adjust the logic here.
        """
        calculated = ServeManager.calculate_server(self.s1, self.s2, self.points_per_side)
        
        # If the match started with Player 2 serving, we flip the result
        if self.starting_server == 1:
            self.server = calculated
        else:
            self.server = 1 if calculated == 2 else 2

    def manual_server_swap(self):
        """
        Management: If the operator forces a server change, we flip 
        the 'Starting Server' so the rotation stays correct.
        """
        self.starting_server = 1 if self.starting_server == 2 else 2
        self.update_server()