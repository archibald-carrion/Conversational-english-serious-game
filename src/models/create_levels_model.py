# models/create_levels_model.py
import utils.json_controller as json_controller
import json

class CreateLevelsModel():
    def __init__(self):
        # Create an instance of JSONController to interact with levels.json
        self.json_controller = json_controller.JSONController(json_path="levels.json")
        return None
    
    def create_new_level(self, level_data):
        """
        Creates a new level in the levels.json file
        
        Parameters:
        level_data (dict): A dictionary containing 'name' and 'questions' keys
                          where 'questions' is a list of question dictionaries
        
        Returns:
        bool: True if level was created successfully, False otherwise
        """
        print("Creating a new level")
        
        try:
            # Get the top level key (likely "levels")
            top_level_key = self.json_controller.get_keys()[0]
            
            # Get the current data structure from the json_controller
            levels_data = self.json_controller.data
            
            # Get the level name and questions from level_data
            level_name = level_data['name']
            questions_list = level_data['questions']
            
            # Convert questions list to dict with question number as key
            questions_dict = {}
            for i, question in enumerate(questions_list):
                # Process question data to ensure proper data types
                if "correct_answer" in question:
                    question["correct_answer"] = int(question["correct_answer"])
                
                # Format answers properly if needed
                if "answers" in question and isinstance(question["answers"], dict):
                    # Ensure answer values are strings
                    for ans_key, ans_value in question["answers"].items():
                        question["answers"][ans_key] = str(ans_value)
                
                # Convert other fields to strings as needed
                for key, value in question.items():
                    if key not in ["correct_answer", "answers"]:
                        if not isinstance(value, str):
                            question[key] = str(value)
                
                # Add to questions dictionary with position as key
                questions_dict[str(i+1)] = question
            
            # Add the new level to the levels data
            levels_data[top_level_key][level_name] = questions_dict
            
            # Save the updated data back to the JSON file
            self.json_controller.save_data()
            
            print(f"Level '{level_name}' created successfully")
            return True
            
        except Exception as e:
            print(f"Error creating new level: {e}")
            return False