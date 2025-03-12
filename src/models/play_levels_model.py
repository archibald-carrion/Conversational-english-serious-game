# models/play_levels_model.py
# import json
# import customtkinter as ctk
import utils.json_controller as json_controller

class PlayLevelsModel():
    def __init__(self):
        # create an instance of JSONController
        self.json_controller = json_controller.JSONController(json_path="levels.json")
        return None
    
    def get_available_levels(self):
        # Get available levels from the filesystem
        top_level_key = self.json_controller.get_keys()
        # print("PLAY LEVELS MODEL: Top level key:", top_level_key)
        levels = self.json_controller.get_keys(top_level_key[0])
        # print("PLAY LEVELS MODEL: Available levels:", levels)
        return levels

    def load_level(self, level_name):
        # Load the level
        # print("PLAY LEVELS MODEL: Loading level", level_name)
        content_level = self.json_controller.get_item(level_name)
        # print("PLAY LEVELS MODEL: Content level:", content_level)
        return content_level
    
    def get_question(self, level_name, question_number):
        # Get the question
        content_level = self.json_controller.get_item(level_name)
        question = self.get_question_data(content_level, question_number)
        print("PLAY LEVELS MODEL: Question:", question)
        return question
    

    def get_question_data(self, data, question_number):
        """
        Retrieve structured data for a given question number.

        Args:
            data_str (str): The JSON-like string containing all question data.
            question_number (str): The key representing the question number.

        Returns:
            dict: A dictionary containing the structured question data or None if not found.
        """

        # Convert question_number to string since the keys in the dictionary are strings
        question_key = str(question_number)
        
        # Check if the question number exists in the dictionary
        if question_key not in data:
            return f"Question number {question_number} does not exist in the data."
        
        # Return the full content for the specified question
        return data[question_key]
    
    def check_answer(self, level_name, question_number, answer):
        # Check the answer
        content_level = self.json_controller.get_item(level_name)
        question = self.get_question_data(content_level, question_number)
        correct_answer = question["correct_answer"] 
        return correct_answer == answer
