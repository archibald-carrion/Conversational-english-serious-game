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
    
    def get_question_answers(self, index_question):
        self.current_question = index_question
        return self.model.get_question_answers(self.current_level, self.current_question-1)
    
    def get_correct_answer_index(self, index_question):
        self.current_question = index_question
        answers = self.model.get_correct_answer_index(self.current_level, self.current_question-1)
        return answers
    
    def save_question(self, question_data):
        question_data["id"] = question_data["id"] - 1
        self.current_question = question_data["id"]
        return self.model.save_question(self.current_level, self.current_question, question_data)

    def get_image_path(self, index_question):
        self.current_question = index_question
        return self.model.get_image_path(self.current_level, self.current_question-1)
    
    def get_audio_path(self, index_question):
        self.current_question = index_question
        return self.model.get_audio_path(self.current_level, self.current_question-1)
    
    def refresh_json(self):
        # refresh the json file
        return self.model.refresh_json()