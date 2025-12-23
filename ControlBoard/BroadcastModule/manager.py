from ControlBoard.BroadcastModule.hype_action import HypeAction
# ADD THIS IMPORT TO RESOLVE THE NAMEERROR
from ControlBoard.BroadcastModule.deploy_action import DeployBroadcastAction

class BroadcastManager:
    def __init__(self, ui, engine, triggers):
        self.ui = ui
        self.engine = engine
        # Now defined via import
        self.deploy_act = DeployBroadcastAction(ui, triggers)
        # New Hype Action registered here
        self.hype_act = HypeAction(ui, engine, triggers['hype'])
        
    def broadcast_hype(self):
        """The Hub calls this when the optional button is pressed."""
        self.hype_act.execute()

    def start_broadcast(self):
        self.deploy_act.execute()