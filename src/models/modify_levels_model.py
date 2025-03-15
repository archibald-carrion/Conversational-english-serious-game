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
    
    def get_correct_answer_index(self, level_name, question_number):
        content_level = self.json_controller.get_item(level_name)
        # print("MODIFY LEVELS MODEL: Content level:", content_level)

        def extract_correct_answer(content_level, question_number):
            return content_level[str(question_number)]["correct_answer"]
        
        correct_answer = extract_correct_answer(content_level, question_number)
        # print(json.dumps(answers, indent=2))
        return correct_answer
    
    def get_image_path(self, level_name, question_number):
        content_level = self.json_controller.get_item(level_name)
        # print("MODIFY LEVELS MODEL: Content level:", content_level)

        def extract_image_path(content_level, question_number):
            return content_level[str(question_number)]["image_file"]
        
        image_path = extract_image_path(content_level, question_number)
        # print(json.dumps(answers, indent=2))
        return image_path
    
    def get_audio_path(self, level_name, question_number):
        content_level = self.json_controller.get_item(level_name)
        # print("MODIFY LEVELS MODEL: Content level:", content_level)

        def extract_audio_path(content_level, question_number):
            return content_level[str(question_number)]["audio_file"]
        
        audio_path = extract_audio_path(content_level, question_number)
        # print(json.dumps(answers, indent=2))
        return audio_path
    
    # def save_question(self, level_name, question_number, question_data):
    #     print("SAVING QUESTION | New question data:", question_data)
        
    #     # Get the current data structure from the json_controller
    #     # Since there's no get_data() method, we'll use the data attribute directly
    #     levels_data = self.json_controller.data
        
    #     # Navigate to the correct location in the JSON structure
    #     # First get the top level key (likely "levels")
    #     top_level_key = self.json_controller.get_keys()[0]

    #     question_data["id"] = int(question_data["id"])
        
    #     # Update the question data at the specified position
    #     levels_data[top_level_key][level_name][str(question_number)] = question_data
        
    #     # Save the updated data back to the JSON file
    #     # We don't need to pass the data as the controller already has the reference
    #     self.json_controller.save_data()
        
    #     print(f"Question {question_number} in {level_name} updated successfully")
    #     return True

    def save_question(self, level_name, question_number, question_data):
        print("SAVING QUESTION | New question data:", question_data)
        
        # Get the current data structure from the json_controller
        levels_data = self.json_controller.data
        
        # Navigate to the correct location in the JSON structure
        top_level_key = self.json_controller.get_keys()[0]
        
        # Ensure correct data types
        # Convert id to integer
        # if "id" in question_data:
        #     question_data["id"] = int(question_data["id"])
        
        # eliminate the id key from the question_data as it is not needed in the JSON file
        if "id" in question_data:
            del question_data["id"]


        # Convert correct_answer to integer (since this should be stored as number)
        if "correct_answer" in question_data:
            question_data["correct_answer"] = int(question_data["correct_answer"])
        
        # Make sure everything else is stored as strings
        for key, value in question_data.items():
            if key not in ["id", "correct_answer"]:
                if isinstance(value, dict):
                    # For nested dictionaries like answers
                    for sub_key, sub_value in value.items():
                        value[sub_key] = str(sub_value)
                elif not isinstance(value, str):
                    question_data[key] = str(value)
        
        # Update the question data at the specified position
        levels_data[top_level_key][level_name][str(question_number)] = question_data
        
        # Save the updated data back to the JSON file
        self.json_controller.save_data()
        
        print(f"Question {question_number} in {level_name} updated successfully")
        return True