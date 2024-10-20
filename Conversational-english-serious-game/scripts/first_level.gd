extends Node2D

var questions = [
	{
		"question": "Where do you work, \n and what kind of company is it?",
		"answers": [
			"McDonald's is a well-known company that \n serves fast food and operates globally.",
			"The company is in charge of organizing \n annual events for local communities.",
			"I work at a software company that \n develops mobile applications."
		],
		"correct_answer": 2
	},
	{
		"question": "What kind of projects do you work on in your current job?",
		"answers": [
			"I teach Chemistry at a private university in Guanacaste.",
			"I work on designing new marketing campaigns for our clients.",
			"I enjoy experimenting with new recipes in my free time."
		],
		"correct_answer": 1
	},
	{
		"question": "How long have you worked in this field, and what do you enjoy the most?",
		"answers": [
			"I once traveled to three countries in one summer, which was an unforgettable experience.",
			"I enjoy painting landscapes during my free time, especially in the fall.",
			"I’ve spent 7 years in this field, and I find fulfillment in working with my colleagues."
		],
		"correct_answer": 2
	},
	{
		"question": "Why did you decide to work in this industry?",
		"answers": [
			"I pursued a degree in literature because I enjoy storytelling and exploration of ideas.",
			"I decided to take cooking classes as a way to explore diverse culinary experiences.",
			"I chose to enter this field due to my enthusiasm for technology and innovation."
		],
		"correct_answer": 2
	},
	{
		"question": "Where did you start working when you began your career?",
		"answers": [
			"I was 22 when I decided to volunteer at a local charity to gain experience.",
			"I began my career at a small startup focused on innovative solutions.",
			"I started my career as a musician because I wanted to bring joy to others with my songs."
		],
		"correct_answer": 1
	},
	{
		"question": "What responsibilities do you have in your current job?",
		"answers": [
			"I enjoy attending conferences to learn about industry trends.",
			"The company has a strong focus on community outreach and social responsibility.",
			"My role involves leading a team and supervising project development."
		],
		"correct_answer": 2
	},
	{
		"question": "How do you balance your work with personal life?",
		"answers": [
			"I do so by setting clear boundaries and prioritizing family time.",
			"I prefer watching movies at home to going out.",
			"I appreciate the support of my friends and family in managing my time."
		],
		"correct_answer": 0
	},
	{
		"question": "What skills do you use most often at work, and how do they help you succeed?",
		"answers": [
			"I use my cooking skills to make delicious meals for my family, bringing us together.",
			"I consider myself a creative person, capable of expressing my emotions through art.",
			"I often rely on communication and problem-solving skills, which enhance collaboration."
		],
		"correct_answer": 2
	},
	{
		"question": "Where do you see yourself working in five years, and what position would you like to hold?",
		"answers": [
			"I see myself studying at a prestigious university, focusing on my academic interests.",
			"I see myself traveling to different countries, exploring new cultures and experiences.",
			"I envision being part of a dynamic team in the future, possibly in a leadership role."
		],
		"correct_answer": 2
	},
	{
		"question": "Why do you think working in teams is important for your job?",
		"answers": [
			"I think problem-solving skills are necessary in team-building activities in the workplace.",
			"I believe collaboration is essential in my role, as it fosters creativity and helps achieve common goals.",
			"Employers should encourage their employees to work in teams to strengthen relationships among colleagues."
		],
		"correct_answer": 1
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
	
