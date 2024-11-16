
		

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

