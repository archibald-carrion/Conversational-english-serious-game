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

    def save_levels(self):
        """
        Save the current levels data back to the JSON file
        """
        try:
            # Convert back to list of dicts format for saving
            levels_list = [
                {level_name: level_content} 
                for level_name, level_content in self.levels_data.items()
            ]
            
            with open(self.json_path, 'w', encoding='utf-8') as file:
                json.dump(levels_list, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving levels: {str(e)}")
            return False

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

    def update_question(self, level_name, question_index, updated_data):
        """
        Update a specific question in a level with new data
        
        Args:
            level_name (str): Name of the level
            question_index (int): Index of the question to update
            updated_data (dict): New question data containing question, answers, correct_answer, and audio_file
        
        Returns:
            bool: True if update was successful, False otherwise
        """
        try:
            if level_name in self.levels_data:
                level_questions = self.levels_data[level_name]
                if 0 <= question_index < len(level_questions):
                    # Update the question data
                    self.levels_data[level_name][question_index] = updated_data
                    # Save changes to file
                    return self.save_levels()
            return False
        except Exception as e:
            print(f"Error updating question: {str(e)}")
            return False

    def add_level(self, level_name, questions=None):
        """
        Add a new level
        
        Args:
            level_name (str): Name of the new level
            questions (list): Optional list of questions for the level
        
        Returns:
            bool: True if level was added successfully, False otherwise
        """
        if level_name not in self.levels_data:
            self.levels_data[level_name] = questions if questions else []
            return self.save_levels()
        return False

    def delete_level(self, level_name):
        """
        Delete a level
        
        Args:
            level_name (str): Name of the level to delete
        
        Returns:
            bool: True if level was deleted successfully, False otherwise
        """
        if level_name in self.levels_data:
            del self.levels_data[level_name]
            return self.save_levels()
        return False

    def add_question(self, level_name, question_data):
        """
        Add a new question to a level
        
        Args:
            level_name (str): Name of the level
            question_data (dict): Question data to add
        
        Returns:
            bool: True if question was added successfully, False otherwise
        """
        if level_name in self.levels_data:
            self.levels_data[level_name].append(question_data)
            return self.save_levels()
        return False

    def delete_question(self, level_name, question_index):
        """
        Delete a question from a level
        
        Args:
            level_name (str): Name of the level
            question_index (int): Index of the question to delete
        
        Returns:
            bool: True if question was deleted successfully, False otherwise
        """
        if level_name in self.levels_data:
            level_questions = self.levels_data[level_name]
            if 0 <= question_index < len(level_questions):
                self.levels_data[level_name].pop(question_index)
                return self.save_levels()
        return False