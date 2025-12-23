class SwapSidesAction:
    def __init__(self, ui, triggers, sync_hub_callback):
        self.ui = ui
        self.triggers = triggers
        self.sync_hub = sync_hub_callback

    def execute(self, current_flipped_state, match_started):
        """Item 5: Swaps logic and labels while respecting deactivated colors."""
        p1_label = self.ui.p1_name_display.text()
        p2_label = self.ui.p2_name_display.text()
        self.ui.p1_name_display.setText(p2_label)
        self.ui.p2_name_display.setText(p1_label)
        
        new_flipped_state = not current_flipped_state
        
        # Apply visual states via UI helper
        if match_started:
            p1_col = "#3498DB" if new_flipped_state else "#2ECC71"
            p2_col = "#2ECC71" if new_flipped_state else "#3498DB"
            self.ui.set_scoring_enabled(True, p1_col, p2_col)
        else:
            self.ui.set_scoring_enabled(False) 
        
        self.sync_hub(new_flipped_state)
        if 'swap' in self.triggers:
            self.triggers['swap'](new_flipped_state)
            
        self.ui.flash_status("SIDES SWAPPED")
        return new_flipped_state