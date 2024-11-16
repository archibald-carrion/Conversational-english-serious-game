extends Node2D

# Global variable to store the current level name
var current_level

# Called when the node enters the scene tree for the first time.
func _ready():
	# Read the levels from the levels.txt file
	var file = FileAccess.open("res://levels.txt", FileAccess.READ)
	var content = file.get_as_text()
	
	var json_result = JSON.parse_string(content)
	if json_result != null:
		var levels = json_result
		if levels is Array:
			var option_button = $CanvasLayer/VBoxContainer/MarginContainer/OptionButton
			
			# Iterate through the main array
			for level_dict in levels:
				# Each item is a dictionary with a single key (like "level 1" or "level 2")
				for level_name in level_dict:
					option_button.add_item(level_name)
					
			# Set the current level to the first one
			if levels.size() > 0:
				# Get the first key of the first dictionary
				var first_level_name = levels[0].keys()[0]
				current_level = first_level_name
				
				Global.current_level_id = first_level_name
	else:
		print("Error parsing JSON")

# when CanvasLayer/VBoxContainer/MarginContainer4/create_level is clicked, set the selected option of CanvasLayer/VBoxContainer/MarginContainer/OptionButton as the current level (need to be global to be access in other scenes)
func _on_create_level_pressed():
	get_tree().change_scene_to_file("res://scenes/level_01.tscn")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass




func _on_option_button_item_selected(index):
	var option_button = $CanvasLayer/VBoxContainer/MarginContainer/OptionButton
	var selected_level = option_button.get_item_text(index)
	current_level = selected_level
	Global.current_level_id = selected_level
	print("Selected level changed to: ", selected_level)





func _on_exit_pressed():
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
