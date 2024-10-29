extends Node2D

var questions = [
{
		"question": "What is the main challenge\nyou face in your job?",
		"answers": [
			"Communicating in different languages\nwith my clients is a constant\nstruggle for me.",
			"Commuting becomes a daily problem\nas I spend more time in my car\nthan in the office.",
			"Prioritizing tasks and setting deadlines\nto manage my time appropriately\nis really difficult for me."
		],
		"correct_answer": 2,
		"audio_file" : "res://assets/audio/diff_02/1.mp3"
	},
	{
		"question": "How has your role in the\ncompany changed over time?",
		"answers": [
			"My responsibilities have been\nconsistent since the my first\nday working here.",
			"I'm now working part-time instead\nof full-time as I needed to\nfinish my studies.",
			"At the beginning I was in an\nentry-level position, but now I am\nworking as a manager."
		],
		"correct_answer": 2,
		"audio_file" : "res://assets/audio/diff_02/2.mp3"
	},
	{
		"question": "What motivates you to keep\nimproving in your current occupation?",
		"answers": [
			"I enjoy the routine of my daily\nwork, so I stay motivated.",
			"I am motivated by continuously\nlearning new technologies.",
			"How my colleagues inspire me\nevery day is my main motivation."
		],
		"correct_answer": 1,
		"audio_file" : "res://assets/audio/diff_02/3.mp3"
	},
	{
		"question": "How do you manage stress\nand pressure at work?",
		"answers": [
			"I try to stay organized and take\nregular breaks to maintain a\nwork-life balance.",
			"Talking to my friends and family\nabout my challenges works for me.",
			"Mindfulness and exercising have\nhelped me in this kind of situation."
		],
		"correct_answer": 0,
		"audio_file" : "res://assets/audio/diff_02/4.mp3"
	},
	{
		"question": "What are the most important\nqualities to succeed in\nyour industry?",
		"answers": [
			"Creativity and innovation are\nimportant in my field.",
			"Adaptability, teamwork, and\nproblem-solving are crucial.",
			"Organization and punctuality\nare key in any job."
		],
		"correct_answer": 1,
		"audio_file" : "res://assets/audio/diff_02/5.mp3"
	},
	{
		"question": "What kind of impact do you hope\nyour work will have on the company\nand its future growth?",
		"answers": [
			"I hope my work will help the\ncompany reach new clients.",
			"I hope my work will contribute to\nthe company's expansion into new markets.",
			"I hope my work will improve\ncommunication between departments."
		],
		"correct_answer": 1,
		"audio_file" : "res://assets/audio/diff_02/6.mp3"
	},
	{
		"question": "How do you keep yourself updated\nwith the latest trends and\nadvancements in your field?",
		"answers": [
			"I regularly attend conferences\nand take online courses.",
			"Watching the news every morning\nhelps me keep updated.",
			"I learn new trends by following\nprofessionals on social media."
		],
		"correct_answer": 0,
		"audio_file" : "res://assets/audio/diff_02/7.mp3"
	},
	{
		"question": "How does technology help you\nimprove your job performance?",
		"answers": [
			"Technology plays a key role by\nstreamlining processes and\nautomating tasks.",
			"Technology plays a key role by\nfacilitating communication with\ninternational teams.",
			"Technology plays a key role by\nallowing the participation in\ninternational trainings online."
		],
		"correct_answer": 0,
		"audio_file" : "res://assets/audio/diff_02/8.mp3"
	},
	{
		"question": "How does teamwork contribute\nto achieving the company's goals?",
		"answers": [
			"It combines expertise to meet\nobjectives through clear communication.",
			"The main factor of teamwork is\nsharing ideas to advance efficiently.",
			"Motivating team members to work\ntogether is a key contribution."
		],
		"correct_answer": 0,
		"audio_file" : "res://assets/audio/diff_02/9.mp3"
	},
	{
		"question": "What advice would you give to\nsomeone starting a career\nin your field?",
		"answers": [
			"I'd suggest building strong\nrelationships with colleagues.",
			"They should work on being patient\nand open to learning.",
			"I'd recommend focusing on technical\nskills and networking."
		],
		"correct_answer": 2,
		"audio_file" : "res://assets/audio/diff_02/10.mp3"
	}
];


var question_number = 0
var current_correct_answer = 0
var question_answered = false
var current_correct_button = 0

var score = 0
var max_score = 100  # The maximum score achievable if all answers are correct on the first try
var attempts = 0
var score_per_question = max_score / questions.size()  # Divide the total score evenly among all questions

var current_audio_file = ""  # Variable to store the current audio file

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
	pass # Replace with function body.
	
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

