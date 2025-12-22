class ApplySettingsAction:
    def __init__(self, ui, settings_store, sync_callback):
        self.ui = ui
        self.store = settings_store
        self.sync_callback = sync_callback

    def execute(self):
        """Action: Captures UI values and updates the 'Brain'."""
        p1 = self.ui.p1_input.text()
        p2 = self.ui.p2_input.text()
        limit = int(self.ui.pts_limit.currentText())
        
        # Update our central store
        self.store.update_names(p1, p2)
        self.store.update_limits(limit, 3) # Default Best of 3
        
        self.sync_callback() # Tell all screens to update their labels