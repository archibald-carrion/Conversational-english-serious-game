extends Node2D

var questions = []  # This will be populated from the JSON file
var question_number = 0
var current_correct_answer = 0
var question_answered = false
var current_correct_button = 0

var score = 0
var max_score = 100
var attempts = 0
var score_per_question = 0  # We'll calculate this after loading questions

var current_audio_file = ""

func _ready():
	# Load questions from JSON based on current_level_id
	load_questions_from_json()
	
	get_node("congratulations").visible = false
	get_node("congratulations").set_process(false)
	get_node("not_congratulation").visible = false
	get_node("not_congratulation").set_process(false)
	show_question()

func load_questions_from_json():
	var file = FileAccess.open("res://levels.txt", FileAccess.READ)
	var content = file.get_as_text()
	
	var json_result = JSON.parse_string(content)
	if json_result != null:
		var levels = json_result
		if levels is Array:
			# Find the level that matches current_level_id
			for level_dict in levels:
				print("reading: ")
				print(Global.current_level_id)
				if level_dict.has(Global.current_level_id):
					questions = level_dict[Global.current_level_id]
					score_per_question = max_score / questions.size()
					break
	else:
		print("Error parsing JSON")
		
	if questions.size() == 0:
		print("No questions found for level: ", Global.current_level_id)
		get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
		
func show_question():
	var current_question = questions[question_number]
	var question_text = str(current_question["question"])
	var max_line_length = 25  # Set the maximum length for each line

	#var formatted_text = ""
	#var current_line = ""
	#var words = question_text.split(" ")  # Split the text into words
#
	## Loop through each word and add them to the current line
	#for word in words:
		## Check if adding the next word would exceed the max line length
		#if current_line.length() + word.length() + 1 <= max_line_length:
			## Add the word to the current line
			#if current_line == "":
				#current_line = word
			#else:
				#current_line += " " + word
		#else:
			## Add the current line to the formatted text and start a new line
			#formatted_text += current_line + "\n"
			#current_line = word  # Start the new line with the current word
#
	## Add any remaining text in the current line to formatted_text
	#if current_line != "":
		#formatted_text += current_line

	# Access the question label
	var question_label = get_node("John/TextureRect/MarginContainer/Label")
	
	# Apply smaller font size and center the text
	question_label.add_theme_font_size_override("font_size", 25)  # Adjust font size (20 is an example)
	question_label.text = question_text  # Set the formatted question text

	# Update answer buttons with the current question's answers
	var answer_button_0 = get_node("answers/HBoxContainer/answers/MarginContainer/answer_0")
	var answer_button_1 = get_node("answers/HBoxContainer/answers/MarginContainer3/answer_1")
	var answer_button_2 = get_node("answers/HBoxContainer/answers/MarginContainer4/answer_2")

	# Apply smaller font size to the answer buttons
	answer_button_0.add_theme_font_size_override("font_size", 18)
	answer_button_1.add_theme_font_size_override("font_size", 18)
	answer_button_2.add_theme_font_size_override("font_size", 18)

	# Set text for the answer buttons
	answer_button_0.text = current_question["answers"][0]
	answer_button_1.text = current_question["answers"][1]
	answer_button_2.text = current_question["answers"][2]

	current_correct_button = current_question["correct_answer"]
	attempts = 0  # Reset attempts for each new question
	current_audio_file = current_question["audio_file"]
	play_question_audio(current_audio_file)  # Play the question's audio



	
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
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
	
func play_question_audio(audio_file):
	var audio_player = get_node("AudioStreamPlayer")
	var stream = load(audio_file)  # Use load instead of preload
	audio_player.stream = stream
	audio_player.play()
	
	
	

func _on_play_audio_again_button_pressed():
	# Replay the audio when the button is clicked
	if current_audio_file != "":
		play_question_audio(current_audio_file)  # Play the stored audio file


func _on_goback_main_menu_button_pressed():
	get_tree().change_scene_to_file("res://scenes/main_menu.tscn")

