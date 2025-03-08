# models/play_levels_model.py
import customtkinter as ctk
import utils.json_controller as json_controller

class PlayLevelsModel():
    def __init__(self):
        # create an instance of JSONController
        self.json_controller = json_controller.JSONController(json_path="levels.json")
        return None
    
    def get_available_levels(self):
        # Get available levels from the filesystem
        top_level_key = self.json_controller.get_keys()
        print("PLAY LEVELS MODEL: Top level key:", top_level_key)
        levels = self.json_controller.get_keys(top_level_key[0])
        print("PLAY LEVELS MODEL: Available levels:", levels)
        return levels
