extends Node2D

var questions = [
	{
		"question": "What is the capital of France?",
		"answers": ["Paris", "London", "Berlin"],
		"correct_answer": 0  # Index of the correct answer in the answers array
	},
	{
		"question": "What is 2 + 2?",
		"answers": ["3", "4", "5"],
		"correct_answer": 1
	},
	{
		"question": "What color is the sky?",
		"answers": ["Green", "Blue", "Red"],
		"correct_answer": 1
	}
]

var question_number = 0
var current_correct_answer = 0
var question_answered = false
var current_correct_button = 0

func _ready():
	get_node("congratulations").visible = false
	get_node("congratulations").set_process(false)
	#get_node("congratulations/HBoxContainer_Background/texture_Background").set_process(false)
	show_question()

func show_question():
	var current_question = questions[question_number]
	var question_text = str(current_question["question"])
	var max_line_length = 25  # Set the maximum length for each line

	var formatted_text = ""
	var current_line = ""
	var words = question_text.split(" ")  # Split the text into words

	# Loop through each word and add them to the current line
	for word in words:
		# Check if adding the next word would exceed the max line length
		if current_line.length() + word.length() + 1 <= max_line_length:
			# Add the word to the current line
			if current_line == "":
				current_line = word
			else:
				current_line += " " + word
		else:
			# Add the current line to the formatted text and start a new line
			formatted_text += current_line + "\n"
			current_line = word  # Start the new line with the current word

	# Add any remaining text in the current line to formatted_text
	if current_line != "":
		formatted_text += current_line

	# Display the formatted text
	get_node("John/HBoxContainer_John/TextureRect/MarginContainer/Label").text = formatted_text
	# print(formatted_text)
	
	get_node("answers/HBoxContainer/answers/MarginContainer/answer_0").text = current_question["answers"][0]
	get_node("answers/HBoxContainer/answers/MarginContainer3/answer_1").text = current_question["answers"][1]
	get_node("answers/HBoxContainer/answers/MarginContainer4/answer_2").text = current_question["answers"][2]

	current_correct_button = current_question["correct_answer"]



	
	# read dirrection to the audio
	
	# update the content of each answer button
	
	# update the content of the "bubble"
	
	# play the audio
	
# on click replay, replay audio

# on click of button one, check if correct button, in this case deisplay good message, else bad message

# on click of button two, check if correct button, in this case deisplay good message, else bad message

# on click of button three, check if correct button, in this case deisplay good message, else bad message



# GOTO MAIN MENU
func _on_button_pressed():
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
	pass # Replace with function body.


func _on_answer_0_pressed():
	if current_correct_button == 0:
		get_node("congratulations").visible = true
		get_node("congratulations").set_process(true)
		
		


func _on_answer_1_pressed():
	if current_correct_button == 1:
		get_node("congratulations").visible = true
		get_node("congratulations").set_process(true)




func _on_answer_2_pressed():
	if current_correct_button == 2:
		get_node("congratulations").visible = true
		get_node("congratulations").set_process(true)


func _on_next_question_pressed():
	question_number = question_number+1
	get_node("congratulations").visible = false
	get_node("congratulations").set_process(false)
	show_question()
