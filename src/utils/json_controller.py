import json
import os
import traceback

class JSONController:
    def __init__(self, json_path='data.json'):
        """
        Initialize the JSONController with the path to the JSON file.
        
        Args:
            json_path (str): Path to the JSON file.
        """
        self.json_path = os.path.abspath(json_path)  # Get absolute path
        print(f"Using JSON file at: {self.json_path}")
        self.data = self.load_data()
        print("DATA:", self.data)

    def load_data(self):
        """
        Load data from the JSON file.
        
        Returns:
            dict: Loaded data or empty dictionary if file doesn't exist.
        """
        # Check if file exists
        if not os.path.exists(self.json_path):
            print(f"Warning: {self.json_path} not found, creating new file.")
            empty_data = {}
            self.data = empty_data
            self.save_data()  # Create the file with empty dictionary
            return empty_data

        # Check if file is accessible
        if not os.access(self.json_path, os.R_OK):
            print(f"Error: No read permission for {self.json_path}")
            return {}
            
        # Try to read the file
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                print(f"File content length: {len(file_content)} bytes")
                
                if not file_content.strip():
                    print("Warning: File is empty")
                    return {}
                    
                try:
                    data = json.loads(file_content)
                    if not isinstance(data, dict):
                        print(f"Warning: JSON content is not a dictionary, it's a {type(data)}")
                        return {}
                    return data
                except json.JSONDecodeError as je:
                    print(f"JSON Decode Error at line {je.lineno}, column {je.colno}: {je.msg}")
                    print(f"Near text: {file_content[max(0, je.pos-20):je.pos+20]}")
                    return {}
        except IOError as e:
            print(f"I/O Error: {str(e)}")
            traceback.print_exc()
            return {}
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            traceback.print_exc()
            return {}

    def save_data(self):
        """
        Save the current data back to the JSON file.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Make sure directory exists
            directory = os.path.dirname(self.json_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            with open(self.json_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, indent=4, ensure_ascii=False)
            print(f"Successfully saved data to {self.json_path}")
            return True
        except Exception as e:
            print(f"Error saving JSON: {str(e)}")
            traceback.print_exc()
            return False

    def get_item(self, key):
        """
        Retrieve an item by key.
        
        Args:
            key (str): The key to retrieve.
        
        Returns:
            Any: The value associated with the key, or None if not found.
        """
        return self.data.get(key, None)
    
    def get_keys(self, key=None):
        """
        Retrieve all keys in the JSON structure or at the level directly below the specified key.
        
        Args:
            key (str, optional): The parent key to look under. If None, returns top-level keys.
        
        Returns:
            list: A list of all keys at the specified level in the JSON structure.
        """
        if key is None:
            # Return top-level keys if no key is specified
            return list(self.data.keys())
        
        # Get the item at the specified key
        item = self.get_item(key)
        
        # Check if the item exists and is a dictionary
        if item is not None and isinstance(item, dict):
            return list(item.keys())
        
        # Return empty list if the key doesn't exist or isn't a dictionary
        return []

    def add_item(self, key, value):
        """
        Add a new item to the JSON structure.
        
        Args:
            key (str): The key for the new item.
            value (Any): The value to store.
        
        Returns:
            bool: True if successful, False if key already exists.
        """
        if key not in self.data:
            self.data[key] = value
            return self.save_data()
        return False

    def delete_item(self, key):
        """
        Delete an item from the JSON structure.
        
        Args:
            key (str): The key to remove.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        if key in self.data:
            del self.data[key]
            return self.save_data()
        return False

    def update_item(self, key, value):
        """
        Update an existing item in the JSON structure.
        
        Args:
            key (str): The key to update.
            value (Any): The new value to store.
        
        Returns:
            bool: True if successful, False if key doesn't exist.
        """
        if key in self.data:
            self.data[key] = value
            return self.save_data()
        return False