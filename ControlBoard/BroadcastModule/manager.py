from ControlBoard.BroadcastModule.deploy_action import DeployBroadcastAction

class BroadcastManager:
    def __init__(self, ui, triggers):
        self.ui = ui
        self.deploy_act = DeployBroadcastAction(ui, triggers)
        
    def start_broadcast(self):
        self.deploy_act.execute()