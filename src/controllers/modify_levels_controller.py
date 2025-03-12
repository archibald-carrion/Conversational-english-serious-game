# controllers/modify_levels_controller.py
import customtkinter as ctk
import models.modify_levels_model as modify_levels_model

class ModifyLevelsController():
    def __init__(self, model: modify_levels_model.ModifyLevelsModel):
        self.model = model
        self.current_level = None
        self.current_question = None

    def get_available_levels(self):
        return self.model.get_available_levels()
    
    def load_level(self, level_name):
        self.current_level = level_name
        self.current_question = 0
        return self.model.load_level(level_name)
    
    def get_all_questions(self):
        return self.model.get_all_questions(self.current_level)