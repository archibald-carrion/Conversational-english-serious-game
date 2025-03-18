# controllers/create_levels_controller.py
import models.create_levels_model as create_levels_model

class CreateLevelsController():
    def __init__(self, model: create_levels_model.CreateLevelsModel):
        self.model = model
        

    def create_new_level(self, level_data):
        print("Creating a new level")
        return self.model.create_new_level(level_data)