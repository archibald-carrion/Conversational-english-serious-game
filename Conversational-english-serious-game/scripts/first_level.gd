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

func _ready():
	show_question()

func show_question():
	var current_question = questions[question_number]
	print(current_question["question"])
	current_correct_answer = current_question["correct_answer"]
	print(current_correct_answer)
	
	# read dirrection to the audio
	
	# update the content of each answer button
	
	# update the content of the "bubble"
	
	# play the audio
	
# on click replay, replay audio

# on click of button one, check if correct button, in this case deisplay good message, else bad message

# on click of button two, check if correct button, in this case deisplay good message, else bad message

# on click of button three, check if correct button, in this case deisplay good message, else bad message

