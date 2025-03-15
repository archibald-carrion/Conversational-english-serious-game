# models/modify_levels_model.py
# import customtkinter as ctk
import utils.json_controller as json_controller
import json


class ModifyLevelsModel():
    def __init__(self):
        # create an instance of JSONController
        self.json_controller = json_controller.JSONController(json_path="levels.json")
        return None
    
    def get_available_levels(self):
        # Get available levels from the filesystem
        top_level_key = self.json_controller.get_keys()
        # print("PLAY LEVELS MODEL: Top level key:", top_level_key)
        levels = self.json_controller.get_keys(top_level_key[0])
        # print("MODIFY LEVELS MODEL: Available levels:", levels)
        return levels
    
    def load_level(self, level_name):
        content_level = self.json_controller.get_item(level_name)
        return content_level
    
    def get_all_questions(self, level_name):

        content_level = self.json_controller.get_item(level_name)
        # print("MODIFY LEVELS MODEL: Content level:", content_level)

        def extract_questions(content_level):
            return [entry["question"] for entry in content_level.values()]

        questions = extract_questions(content_level)
        # print(json.dumps(questions, indent=2))  # Pretty-print the result
        return questions
    
    def get_question_answers(self, level_name, question_number):
        content_level = self.json_controller.get_item(level_name)
        # print("MODIFY LEVELS MODEL: Content level:", content_level)

        def extract_answers(content_level, question_number):
            return content_level[str(question_number)]["answers"]
        
        answers = extract_answers(content_level, question_number)
        # print(json.dumps(answers, indent=2))
        return answers
    
    def save_question(self, level_name, question_number, question_data):
        print("SAVING QUESTION | New question data:", question_data)
        # content_level = self.json_controller.get_item(level_name)
        # print("MODIFY LEVELS MODEL: Content level:", content_level)

        # def update_question(content_level, question_number, question_data):
        #     content_level[str(question_number)] = question_data
        #     return content_level

        # updated_content = update_question(content_level, question_number, question_data)
        # self.json_controller.update_item(level_name, updated_content)
        return None
    
    def get_correct_answer_index(self, level_name, question_number):
        content_level = self.json_controller.get_item(level_name)
        # print("MODIFY LEVELS MODEL: Content level:", content_level)

        def extract_correct_answer(content_level, question_number):
            return content_level[str(question_number)]["correct_answer"]
        
        correct_answer = extract_correct_answer(content_level, question_number)
        # print(json.dumps(answers, indent=2))
        return correct_answer