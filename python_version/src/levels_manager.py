import json
import os

class LevelsManager:
    def __init__(self, json_path='levels.json'):
        """
        Initialize the LevelsManager with the path to the levels JSON file
        
        Args:
            json_path (str): Path to the JSON file containing levels data
        """
        self.json_path = json_path
        self.levels_data = self.load_levels()

    def load_levels(self):
        """
        Load levels from the JSON file
        
        Returns:
            dict: A dictionary containing levels data
        """
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                levels = json.load(file)
                # Convert list of dicts to more accessible format
                processed_levels = {}
                for level_dict in levels:
                    for level_key, level_content in level_dict.items():
                        processed_levels[level_key] = level_content
                return processed_levels
        except FileNotFoundError:
            print(f"Error: Levels file not found at {self.json_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.json_path}")
            return {}

    def get_level_names(self):
        """
        Get the names of available levels
        
        Returns:
            list: Names of available levels
        """
        return list(self.levels_data.keys())

    def get_level_questions(self, level_name):
        """
        Get all questions for a specific level
        
        Args:
            level_name (str): Name of the level
        
        Returns:
            list: Questions for the specified level
        """
        return self.levels_data.get(level_name, [])

    def get_level_question(self, level_name, question_index):
        """
        Get a specific question from a level
        
        Args:
            level_name (str): Name of the level
            question_index (int): Index of the question
        
        Returns:
            dict: Question data or None if not found
        """
        level_questions = self.get_level_questions(level_name)
        if 0 <= question_index < len(level_questions):
            return level_questions[question_index]
        return None