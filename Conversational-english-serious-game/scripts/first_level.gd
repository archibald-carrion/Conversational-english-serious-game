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

var score = 0
var max_score = 100  # The maximum score achievable if all answers are correct on the first try
var attempts = 0
var score_per_question = max_score / questions.size()  # Divide the total score evenly among all questions

func _ready():
	get_node("congratulations").visible = false
	get_node("congratulations").set_process(false)
	get_node("not_congratulation").visible = false
	get_node("not_congratulation").set_process(false)
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

	# Update answer buttons with the current question's answers
	get_node("answers/HBoxContainer/answers/MarginContainer/answer_0").text = current_question["answers"][0]
	get_node("answers/HBoxContainer/answers/MarginContainer3/answer_1").text = current_question["answers"][1]
	get_node("answers/HBoxContainer/answers/MarginContainer4/answer_2").text = current_question["answers"][2]

	current_correct_button = current_question["correct_answer"]
	attempts = 0  # Reset attempts for each new question

func _on_button_pressed():
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
	
func _on_answer_pressed(button_index):
	attempts += 1
	if button_index == current_correct_button:
		get_node("congratulations").visible = true
		get_node("congratulations").set_process(true)
		get_node("congratulations/VBoxContainer/MarginContainer/next_level").visible = false
		get_node("congratulations/VBoxContainer/MarginContainer/next_level").set_process(false)
		
		update_score()  # Update the score based on the attempts
	else:
		get_node("not_congratulation").visible = true
		get_node("not_congratulation").set_process(true)

func update_score():
	# Deduct points based on the number of attempts
	var deduction = (attempts - 1) * (score_per_question / 3)  # Example: lose a third of points per wrong attempt
	score += max(0, score_per_question - deduction)
	# Ensure score is rounded correctly and does not exceed 100
	score = round(score * 100) / 100.0
	print("Current Score: ", score)

func _on_answer_0_pressed():
	_on_answer_pressed(0)

func _on_answer_1_pressed():
	_on_answer_pressed(1)

func _on_answer_2_pressed():
	_on_answer_pressed(2)
	


func _on_next_question_pressed():
	# Increment question_number only if there are more questions
	if question_number + 1 < questions.size():
		question_number += 1
		get_node("congratulations").visible = false
		get_node("congratulations").set_process(false)
		show_question()
	else:
		get_node("congratulations/VBoxContainer/MarginContainer/next_level").visible = true
		get_node("congratulations/VBoxContainer/MarginContainer/next_level").set_process(true)
		
		get_node("congratulations/VBoxContainer/MarginContainer/next_question").visible = false
		get_node("congratulations/VBoxContainer/MarginContainer/next_question").set_process(false)
		# Handle the case when no more questions are available
		print("No more questions available.")
		display_final_score()  # Show the final score when all questions are answered

func display_final_score():
	# Ensure final score is precisely 100 if no points were lost
	if score > max_score - score_per_question / 2:
		score = max_score
		
	var label = get_node("congratulations/VBoxContainer/congratulation_label")
	label.text = "Congratulations! \nYou've completed the level.\nYour score is: " + str(score) + "/100"

	# Set the font size (replace 24 with your desired size)
	label.add_theme_font_size_override("font_size", 70)
	
	
	Global.level_scores.append(score)  # Access the global level scores
	print("Final Score: ", score)
	
	#for score in Global.level_scores:
		#print("Score: ", score)
	
	# Additional logic can be added here to display the score on the screen, if desired.


func _on_try_again_pressed():
	get_node("not_congratulation").visible = false
	get_node("not_congratulation").set_process(false)


func _on_next_level_pressed():
	# goto next scene
	pass # Replace with function body.
