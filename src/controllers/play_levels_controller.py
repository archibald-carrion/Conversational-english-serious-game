# controllers/play_levels_controller.py
import customtkinter as ctk
import models.play_levels_model as play_levels_model

class PlayLevelsController():
    def __init__(self, model: play_levels_model.PlayLevelsModel):
        self.model = model
    
    def get_available_levels(self):
        # get from model the available levels
        return self.model.get_available_levels()

