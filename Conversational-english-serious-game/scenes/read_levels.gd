extends Node2D

# Global variable to store the current level name
var current_level

# Called when the node enters the scene tree for the first time.
func _ready():
	# Read the levels from the levels.txt file
	var file = FileAccess.open("res://levels.txt", FileAccess.READ)
	var content = file.get_as_text()
	
	# Parse the JSON content and add the levels to the OptionButton
	var levels =  JSON.parse_string(content)
	var option_button = $CanvasLayer/VBoxContainer/MarginContainer/OptionButton
	for level in levels:
		option_button.add_item(level)
	
	# Set the current level to the first one in the list
	current_level = levels[0]

# when CanvasLayer/VBoxContainer/MarginContainer4/create_level is clicked, set the selected option of CanvasLayer/VBoxContainer/MarginContainer/OptionButton as the current level (need to be global to be access in other scenes)
func _on_create_level_pressed():
	var option_button = $CanvasLayer/VBoxContainer/MarginContainer/OptionButton
	current_level = option_button.get_selected_text()


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


