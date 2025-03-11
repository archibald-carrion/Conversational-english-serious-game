# controllers/play_levels_controller.py
import customtkinter as ctk
import models.play_levels_model as play_levels_model

class PlayLevelsController():
    def __init__(self, model: play_levels_model.PlayLevelsModel):
        self.model = model
        self.current_level = None
        self.current_question = None
    
    def get_available_levels(self):
        # get from model the available levels
        return self.model.get_available_levels()
    
    def load_level(self, level_name):
        # load the level
        self.current_level = level_name
        self.current_question = 0
        return self.model.load_level(level_name)
    
    def get_current_question(self):
        # get the current question
        return self.model.get_question(self.current_level, self.current_question)
    
    def get_current_question_index(self):
        # get the current question index
        return self.current_question + 1

