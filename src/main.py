import customtkinter as ctk
from levels_manager import LevelsManager
from frame_initializer import FrameInitializer
from PIL import Image
import os
import threading
from playsound import playsound
from tkinter import filedialog
import pygame

class App:
    def __init__(self):
        # Initialize basic attributes
        self.current_score = 0
        self.total_possible_score = 0
        self.levels_manager = LevelsManager('levels.json')
        self.current_level = None
        self.is_audio_playing = False

        # Configure the main window
        self.root = ctk.CTk()
        self.root.title("Level Selector")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        self.root.bind("<Escape>", lambda e: self.root.quit())

        # Set appearance and color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Initialize all frames
        self.initialize_frames()

    def initialize_frames(self):
        """Initialize all frames in the application"""
        frame_initializer = FrameInitializer(self)
        
        frame_initializer.initialize_main_menu_frame()
        frame_initializer.initialize_load_level_frame()
        frame_initializer.initialize_game_configuration_frame()
        frame_initializer.initialize_level_frame()
        frame_initializer.initialize_level_completed_frame()
        frame_initializer.initialize_modify_levels_frame()
        frame_initializer.initialize_question_selection_frame()
        frame_initializer.initialize_question_editor_frame()
        self.initialize_level_creator_frames()
    
    def update_scrollregion(self, event):
        """Update the scroll region when the content frame changes"""
        self.editor_canvas.configure(scrollregion=self.editor_canvas.bbox("all"))

    def update_canvas_width(self, event):
        """Update the width of the canvas window when the canvas is resized"""
        self.editor_canvas.itemconfig(self.canvas_frame, width=event.width-20)

    def on_mousewheel(self, event):
        """Handle mousewheel scrolling"""
        if self.question_editor_frame.winfo_ismapped():  # Only scroll if editor frame is visible
            self.editor_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def get_level_data(self, level_name):
        return self.levels.get(level_name)

    def load_selected_level(self):
        """
        Load the selected level from the dropdown.
        """
        print(f"Selected level: {self.level_dropdown.get()}")
        self.current_level = self.level_dropdown.get()
        self.load_level(self.current_level, 0)

    def open_game_configuration_window(self):
        # Hide main menu
        self.main_menu_frame.pack_forget()
        
        # Show game configuration frame
        self.game_configuration_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def open_load_level_window(self):
        # Hide main menu
        self.main_menu_frame.pack_forget()
        
        # Show load level frame
        self.load_level_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def back_to_main_menu(self):
        # Use the centralized method to hide all frames
        self.hide_all_frames()
        # Show main menu
        self.main_menu_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def apply_window_size(self):
        """Apply the selected window size and reflect changes."""
        self.root.geometry(self.selected_window_size)
        # Optionally adjust UI elements to fit the new window size

        width, height = map(int, self.selected_window_size.split('x'))
        self.bg_image = ctk.CTkImage(
            light_image=Image.open("assets/images/background.png"), 
            dark_image=Image.open("assets/images/background.png"),
            size=(width, height)
        )
        #self.my_background.configure(image=self.bg_image)
        
        # Ensure background covers the entire window
        #self.my_background.place(x=0, y=0, relwidth=1, relheight=1)

    def update_window_size(self, size):
        """Update the selected window size when the dropdown changes."""
        self.selected_window_size = size

    def replay_audio(self):
        """
        Replay the audio for the current question if not already playing.
        """
        if not self.is_audio_playing and hasattr(self, 'current_level'):
            question_data = self.levels_manager.get_level_question(
                self.current_level, 
                self.current_question_index
            )
            
            audio_file = question_data["audio_file"]
            if os.path.exists(audio_file):
                def play_audio():
                    try:
                        # Set flag to prevent multiple playbacks
                        self.is_audio_playing = True
                        
                        sound = pygame.mixer.Sound(audio_file)
                        sound.play()
                        
                        # Wait for the sound to finish
                        pygame.time.wait(int(sound.get_length() * 1000))
                        
                        # Reset the flag when audio finishes
                        self.is_audio_playing = False
                    except Exception as e:
                        print(f"Error playing audio: {e}")
                        self.is_audio_playing = False
                
                # Create and start the audio thread
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.daemon = True  # Ensure the thread doesn't block app closing
                audio_thread.start()
            else:
                print(f"Error: Audio file not found at {audio_file}")

    def load_level(self, level_name, question_index):
        """
        Load and display a specific question for a given level
        """
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Reset score when starting a new level
        if question_index == 0:
            self.current_score = 0
            # Calculate total possible score (10 points per question)
            level_questions = self.levels_manager.get_level_questions(level_name)
            self.total_possible_score = len(level_questions) * 10
            self.score_display.configure(text=f"Score: {self.current_score}/{self.total_possible_score}")

        # Hide other frames
        self.main_menu_frame.pack_forget()
        self.game_configuration_frame.pack_forget()
        self.load_level_frame.pack_forget()

        # Show the level frame
        self.level_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Reset audio playing flag
        self.is_audio_playing = False

        # Get the question data
        question_data = self.levels_manager.get_level_question(level_name, question_index)
        if question_data:
            # Set current level and question index
            self.current_level = level_name
            self.current_question_index = question_index

            # Update the level title
            self.level_title.configure(text=f"Level {level_name}")

            # Update the question text
            self.question_text.configure(text=question_data["question"])

            # Update the answer buttons
            for i, answer_text in enumerate(question_data["answers"]):
                self.answer_buttons[i].configure(text=answer_text)

            # Play the audio file
            audio_file = question_data["audio_file"]
            if os.path.exists(audio_file):
                def play_audio():
                    try:
                        self.is_audio_playing = True
                        sound = pygame.mixer.Sound(audio_file)
                        sound.play()
                        pygame.time.wait(int(sound.get_length() * 1000))
                        self.is_audio_playing = False
                    except Exception as e:
                        print(f"Error playing audio: {e}")
                        self.is_audio_playing = False
                        
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.daemon = True
                audio_thread.start()
            else:
                print(f"Error: Audio file not found at {audio_file}")
        else:
            print(f"Error: Question not found for level {level_name} at index {question_index}")

        # Add cleanup method for properly closing pygame mixer
        def cleanup_pygame():
            pygame.mixer.quit()
        
        # Bind cleanup to window closing if not already bound
        if not hasattr(self, '_pygame_cleanup_bound'):
            if hasattr(self, 'master'):  # Assuming this is within a tkinter application
                self.master.protocol("WM_DELETE_WINDOW", 
                    lambda: (cleanup_pygame(), self.master.destroy()))
                self._pygame_cleanup_bound = True

    def handle_answer_click(self, answer_index):
        if not self.current_level:
            print("No level currently loaded")
            return

        if not hasattr(self, 'current_question_index'):
            self.current_question_index = 0
            
        if not hasattr(self, 'current_attempts'):
            self.current_attempts = 0

        question_data = self.levels_manager.get_level_question(
            self.current_level, 
            self.current_question_index
        )
        
        if not hasattr(self, 'feedback_label'):
            self.feedback_label = ctk.CTkLabel(
                self.level_frame,
                text="",
                font=("Helvetica", 20),
                text_color="green"
            )
            self.feedback_label.pack(pady=10)

        # Check if the selected answer is correct
        if answer_index == question_data.get("correct_answer", -1):
            # Award points based on number of attempts
            points = 10 if self.current_attempts == 0 else (5 if self.current_attempts == 1 else 0)
            self.current_score += points
            
            # Update score display
            self.score_display.configure(text=f"Score: {self.current_score}/{self.total_possible_score}")
            
            # Feedback message includes points earned
            self.feedback_label.configure(
                text=f"Correct! +{points} points ✅", 
                text_color="green"
            )
            
            # Reset attempts for next question
            self.current_attempts = 0
            
            # Try to load next question
            next_question_index = self.current_question_index + 1
            next_question = self.levels_manager.get_level_question(
                self.current_level, 
                next_question_index
            )
            
            if next_question:
                self.current_question_index = next_question_index
                self.root.after(2000, lambda: self.load_level(self.current_level, next_question_index))
            else:
                self.feedback_label.configure(
                    text="Level Completed! 🎉", 
                    text_color="green"
                )
                self.root.after(2000, self.show_level_completed_frame)
        else:
            # Increment attempts counter
            self.current_attempts += 1
            
            # Update feedback based on remaining attempts
            remaining_attempts = 3 - self.current_attempts
            feedback_text = f"Try Again! {remaining_attempts} attempts left ❌"
            
            if self.current_attempts >= 3:
                feedback_text = "Moving to next question..."
                self.current_attempts = 0
                next_question_index = self.current_question_index + 1
                self.root.after(2000, lambda: self.load_level(self.current_level, next_question_index))
                
            self.feedback_label.configure(
                text=feedback_text, 
                text_color="red"
            )

        self.root.after(2000, self.clear_feedback)

    def clear_feedback(self):
        """
        Clear the feedback label text.
        """
        if hasattr(self, 'feedback_label'):
            self.feedback_label.configure(text="")

    def show_level_completed_frame(self):
        """
        Display the level completed frame with the score.
        """
        # Hide other frames
        self.level_frame.pack_forget()

        # Update and show the level completed frame
        self.score_label.configure(text=f"Your Score: {self.current_score}/{self.total_possible_score}")
        self.level_completed_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def open_modify_levels_window(self):
        """Open the modify levels window"""
        self.main_menu_frame.pack_forget()
        self.modify_levels_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def open_question_selection(self):
        """Open the question selection window for the chosen level"""
        selected_level = self.modify_level_dropdown.get()
        questions = self.levels_manager.get_level_questions(selected_level)
        
        # Update question dropdown with question numbers
        question_numbers = [f"Question {i+1}" for i in range(len(questions))]
        self.question_dropdown.configure(values=question_numbers)
        if question_numbers:
            self.question_dropdown.set(question_numbers[0])

        self.modify_levels_frame.pack_forget()
        self.question_selection_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def open_question_editor(self):
        """Open the question editor for the selected question"""
        selected_level = self.modify_level_dropdown.get()
        question_index = int(self.question_dropdown.get().split()[-1]) - 1
        
        # Get current question data
        question_data = self.levels_manager.get_level_question(selected_level, question_index)
        
        # Populate fields with current data
        self.question_entry.delete("0.0", "end")
        self.question_entry.insert("0.0", question_data["question"])
        
        for i, answer in enumerate(question_data["answers"]):
            self.answer_entries[i].delete(0, "end")
            self.answer_entries[i].insert(0, answer)
        
        self.correct_answer_entry.delete(0, "end")
        self.correct_answer_entry.insert(0, str(question_data["correct_answer"]))
        
        self.audio_path_label.configure(text=f"Current Audio File: {question_data['audio_file']}")
        self.current_audio_path = question_data['audio_file']

        self.question_selection_frame.pack_forget()
        self.question_editor_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def select_audio_file(self):
        """Open file dialog to select new audio file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav")]
        )
        if file_path:
            self.current_audio_path = file_path
            self.audio_path_label.configure(text=f"Current Audio File: {file_path}")

    def save_question_changes(self):
        """Save the modified question data"""
        selected_level = self.modify_level_dropdown.get()
        question_index = int(self.question_dropdown.get().split()[-1]) - 1
        
        # Get the updated data
        updated_data = {
            "question": self.question_entry.get("0.0", "end").strip(),
            "answers": [entry.get() for entry in self.answer_entries],
            "correct_answer": int(self.correct_answer_entry.get()),
            "audio_file": self.current_audio_path
        }
        
        # Update the question in the levels manager
        self.levels_manager.update_question(selected_level, question_index, updated_data)
        
        # Remove any existing confirmation message
        if hasattr(self, 'confirmation_label'):
            self.confirmation_label.destroy()
        
        # Create new confirmation message
        self.confirmation_label = ctk.CTkLabel(
            self.editor_content_frame,  # Place it in the content frame
            text="Changes saved successfully! ✓",
            text_color="green",
            font=("Helvetica", 16)
        )
        
        # Place the confirmation message after the back button
        self.confirmation_label.pack(pady=10)
        
        # Remove the confirmation message after 2 seconds
        self.root.after(2000, lambda: self.confirmation_label.destroy() if hasattr(self, 'confirmation_label') else None)

    def back_to_modify_levels(self):
        """Return to the modify levels frame"""
        self.question_selection_frame.pack_forget()
        self.modify_levels_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def back_to_question_selection(self):
        """Return to the question selection frame"""
        self.question_editor_frame.pack_forget()
        self.question_selection_frame.pack(pady=50, padx=50, fill="both", expand=True)


    def create_new_level(self):
        """Open the level creation window"""
        # Hide main menu
        self.main_menu_frame.pack_forget()
        
        # Reset entry and error message
        self.level_name_entry.delete(0, "end")
        self.name_error_label.configure(text="")
        self.name_error_label.pack_forget()
        
        # Show the level name frame
        self.level_name_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def initialize_level_creator_frames(self):
        """Initialize frames for creating new levels"""
        
        ''' Level Name Frame '''
        self.level_name_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Title
        self.new_level_title = ctk.CTkLabel(
            self.level_name_frame,
            text="Create New Level",
            font=("Helvetica", 24)
        )
        self.new_level_title.pack(pady=20)
        
        # Level name entry
        self.level_name_label = ctk.CTkLabel(
            self.level_name_frame,
            text="Enter Level Name:"
        )
        self.level_name_label.pack(pady=5)
        
        self.level_name_entry = ctk.CTkEntry(
            self.level_name_frame,
            width=300
        )
        self.level_name_entry.pack(pady=10)
        
        # Error message label (initially hidden)
        self.name_error_label = ctk.CTkLabel(
            self.level_name_frame,
            text="",
            text_color="red"
        )
        self.name_error_label.pack(pady=5)
        self.name_error_label.pack_forget()  # Hide initially
        
        # Continue button
        self.continue_to_questions_btn = ctk.CTkButton(
            self.level_name_frame,
            text="Continue to Questions",
            command=self.start_question_creation
        )
        self.continue_to_questions_btn.pack(pady=10)
        
        # Back button
        self.name_back_btn = ctk.CTkButton(
            self.level_name_frame,
            text="Back to Menu",
            command=self.back_to_main_menu
        )
        self.name_back_btn.pack(pady=10)

        ''' Question Creation Frame '''
        self.question_creation_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Create a canvas with scrollbar for question creation
        self.creation_canvas = ctk.CTkCanvas(
            self.question_creation_frame,
            width=700,
            height=500,
            bg='#2b2b2b',
            highlightthickness=0
        )
        self.creation_scrollbar = ctk.CTkScrollbar(
            self.question_creation_frame,
            orientation="vertical",
            command=self.creation_canvas.yview
        )
        self.creation_canvas.configure(yscrollcommand=self.creation_scrollbar.set)
        
        # Create a frame inside canvas for content
        self.creation_content_frame = ctk.CTkFrame(self.creation_canvas, fg_color="#2b2b2b")
        
        # Pack scrollbar and canvas
        self.creation_scrollbar.pack(side="right", fill="y")
        self.creation_canvas.pack(side="left", fill="both", expand=True, padx=5)
        
        # Create window in canvas
        self.creation_window = self.creation_canvas.create_window(
            (0, 0),
            window=self.creation_content_frame,
            anchor="nw",
            width=680
        )
        
        # Progress indicator
        self.question_progress = ctk.CTkLabel(
            self.creation_content_frame,
            text="Question 1/10",
            font=("Helvetica", 18)
        )
        self.question_progress.pack(pady=10)
        
        # Question text entry
        self.new_question_label = ctk.CTkLabel(
            self.creation_content_frame,
            text="Question:"
        )
        self.new_question_label.pack(pady=3)
        
        self.new_question_entry = ctk.CTkTextbox(
            self.creation_content_frame,
            height=80,
            width=600
        )
        self.new_question_entry.pack(pady=5)
        
        # Answer entries
        self.new_answer_entries = []
        for i in range(3):
            label = ctk.CTkLabel(
                self.creation_content_frame,
                text=f"Answer {i+1}:"
            )
            label.pack(pady=2)
            
            entry = ctk.CTkEntry(
                self.creation_content_frame,
                width=500
            )
            entry.pack(pady=3)
            self.new_answer_entries.append(entry)
        
        # Correct answer selection
        self.new_correct_answer_label = ctk.CTkLabel(
            self.creation_content_frame,
            text="Correct Answer (0-2):"
        )
        self.new_correct_answer_label.pack(pady=2)
        
        self.new_correct_answer_entry = ctk.CTkEntry(
            self.creation_content_frame,
            width=50
        )
        self.new_correct_answer_entry.pack(pady=3)
        
        # Error message for validation
        self.creation_error_label = ctk.CTkLabel(
            self.creation_content_frame,
            text="",
            text_color="red"
        )
        self.creation_error_label.pack(pady=5)
        self.creation_error_label.pack_forget()  # Hide initially
        
        # Audio file selection
        self.new_audio_path_label = ctk.CTkLabel(
            self.creation_content_frame,
            text="Current Audio File: None",
            wraplength=500
        )
        self.new_audio_path_label.pack(pady=2)
        
        self.new_select_audio_btn = ctk.CTkButton(
            self.creation_content_frame,
            text="Select Audio File",
            command=self.select_new_audio_file
        )
        self.new_select_audio_btn.pack(pady=3)
        
        # Navigation buttons
        self.button_frame = ctk.CTkFrame(
            self.creation_content_frame,
            fg_color="transparent"
        )
        self.button_frame.pack(pady=10)
        
        self.prev_question_btn = ctk.CTkButton(
            self.button_frame,
            text="Previous Question",
            command=self.prev_question,
            state="disabled"  # Initially disabled
        )
        self.prev_question_btn.pack(side="left", padx=5)
        
        self.next_question_btn = ctk.CTkButton(
            self.button_frame,
            text="Next Question",
            command=self.next_question
        )
        self.next_question_btn.pack(side="left", padx=5)
        
        # Save level button (initially hidden)
        self.save_level_btn = ctk.CTkButton(
            self.creation_content_frame,
            text="Save Level",
            command=self.save_new_level
        )
        
        # Back button
        self.creation_back_btn = ctk.CTkButton(
            self.creation_content_frame,
            text="Back to Level Name",
            command=self.back_to_level_name
        )
        self.creation_back_btn.pack(pady=10)
        
        # Bind canvas configuration
        self.creation_content_frame.bind("<Configure>", self.update_creation_scrollregion)
        self.creation_canvas.bind("<Configure>", self.update_creation_canvas_width)
        self.root.bind("<MouseWheel>", self.on_creation_mousewheel)


    def start_question_creation(self):
        """Start creating questions for the new level"""
        level_name = self.level_name_entry.get().strip()
        
        # Validate level name
        if not level_name:
            self.name_error_label.configure(text="Please enter a level name")
            self.name_error_label.pack(pady=5)
            return
        
        # Check if level already exists
        if level_name in self.levels_manager.get_level_names():
            self.name_error_label.configure(text="Level name already exists")
            self.name_error_label.pack(pady=5)
            return
        
        # Initialize question storage with empty templates
        self.new_level_questions = []
        for _ in range(10):
            self.new_level_questions.append({
                "question": "",
                "answers": ["", "", ""],
                "correct_answer": 0,
                "audio_file": ""
            })
        
        self.current_creation_index = 0
        self.current_new_audio_path = ""
        
        # Hide level name frame and show question creation frame
        self.level_name_frame.pack_forget()
        self.creation_error_label.pack_forget()
        self.question_creation_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Reset and load the first question
        self.load_current_question()
        self.update_creation_progress()

    def update_creation_progress(self):
        """Update the progress indicator and navigation buttons"""
        self.question_progress.configure(text=f"Question {self.current_creation_index + 1}/10")
        
        # Update navigation button states
        self.prev_question_btn.configure(state="normal" if self.current_creation_index > 0 else "disabled")
        
        # Show/hide save button on last question
        if self.current_creation_index == 9:
            self.next_question_btn.pack_forget()
            self.save_level_btn.pack(side="left", padx=5)
        else:
            if self.save_level_btn.winfo_manager():  # Check if it's currently packed
                self.save_level_btn.pack_forget()
            if not self.next_question_btn.winfo_manager():  # Check if it's not packed
                self.next_question_btn.pack(side="left", padx=5)

    def validate_current_question(self):
        """Validate the current question data"""
        question = self.new_question_entry.get("0.0", "end").strip()
        if not question:
            self.creation_error_label.configure(text="Question text cannot be empty")
            self.creation_error_label.pack(pady=5)
            return False
        
        # Validate answers - at least two answers must be provided
        valid_answers = [entry.get().strip() for entry in self.new_answer_entries if entry.get().strip()]
        if len(valid_answers) < 2:
            self.creation_error_label.configure(text="At least two answer options must be provided")
            self.creation_error_label.pack(pady=5)
            return False
        
        # Validate correct answer
        try:
            correct_answer = int(self.new_correct_answer_entry.get())
            if not (0 <= correct_answer < len(self.new_answer_entries)):
                raise ValueError
        except (ValueError, TypeError):
            self.creation_error_label.configure(text=f"Correct answer must be a number between 0 and {len(self.new_answer_entries)-1}")
            self.creation_error_label.pack(pady=5)
            return False
        
        # All validation passed
        self.creation_error_label.pack_forget()
        return True

    def save_current_question(self):
        """Save the current question data if valid"""
        if not self.validate_current_question():
            return False
        
        correct_answer = int(self.new_correct_answer_entry.get())
        
        self.new_level_questions[self.current_creation_index] = {
            "question": self.new_question_entry.get("0.0", "end").strip(),
            "answers": [entry.get() for entry in self.new_answer_entries],
            "correct_answer": correct_answer,
            "audio_file": getattr(self, 'current_new_audio_path', "")
        }
        return True

    def load_current_question(self):
        """Load the current question data into the form"""
        question_data = self.new_level_questions[self.current_creation_index]
        
        self.new_question_entry.delete("0.0", "end")
        self.new_question_entry.insert("0.0", question_data["question"])
        
        for i, answer in enumerate(question_data["answers"]):
            self.new_answer_entries[i].delete(0, "end")
            self.new_answer_entries[i].insert(0, answer)
        
        self.new_correct_answer_entry.delete(0, "end")
        self.new_correct_answer_entry.insert(0, str(question_data["correct_answer"]))
        
        audio_path = question_data.get('audio_file', '')
        display_path = audio_path if audio_path else "None"
        self.new_audio_path_label.configure(text=f"Current Audio File: {display_path}")
        self.current_new_audio_path = audio_path

    def next_question(self):
        """Save current question and move to next if valid"""
        if not self.save_current_question():
            return
        
        self.current_creation_index = min(9, self.current_creation_index + 1)
        self.load_current_question()
        self.update_creation_progress()

    def prev_question(self):
        """Save current question and move to previous if valid"""
        if not self.save_current_question():
            return
        
        self.current_creation_index = max(0, self.current_creation_index - 1)
        self.load_current_question()
        self.update_creation_progress()

    def select_new_audio_file(self):
        """Select audio file for new question"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.mp3 *.wav")]
        )
        if file_path:
            self.current_new_audio_path = file_path
            self.new_audio_path_label.configure(text=f"Current Audio File: {file_path}")

    def save_new_level(self):
        """Save the complete new level if all questions are valid"""
        if not self.save_current_question():  # Validate current question
            return
        
        # Check if we have at least one valid question
        valid_questions = [q for q in self.new_level_questions if q["question"].strip()]
        if not valid_questions:
            self.creation_error_label.configure(text="At least one question must be provided")
            self.creation_error_label.pack(pady=5)
            return
        
        level_name = self.level_name_entry.get().strip()
        
        # Filter out empty questions
        final_questions = [q for q in self.new_level_questions if q["question"].strip()]
        
        # Add the new level to the levels manager
        if self.levels_manager.add_level(level_name, final_questions):
            self.show_success_message()
            # Use hide_all_frames instead of just hiding the current frame
            self.hide_all_frames()
            self.main_menu_frame.pack(pady=50, padx=50, fill="both", expand=True)
        else:
            self.creation_error_label.configure(text="Failed to save level. Please try again.")
            self.creation_error_label.pack(pady=5)

    def show_success_message(self):
        """Show a success message when level is saved"""
        success_window = ctk.CTkToplevel(self.root)
        success_window.title("Success")
        success_window.geometry("300x100")
        success_window.resizable(False, False)
        success_window.transient(self.root)  # Make it a transient window
        success_window.grab_set()  # Make it modal
        
        # Center the window
        success_window.update_idletasks()
        width = success_window.winfo_width()
        height = success_window.winfo_height()
        x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
        y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
        success_window.geometry(f"{width}x{height}+{x}+{y}")
        
        label = ctk.CTkLabel(
            success_window,
            text="Level saved successfully!",
            font=("Helvetica", 16)
        )
        label.pack(pady=20)
        
        def close_window():
            success_window.grab_release()
            success_window.destroy()
        
        # Close after 2 seconds
        self.root.after(2000, close_window)

    def back_to_level_name(self):
        """Return to level name frame"""
        if self.save_current_question():
            self.question_creation_frame.pack_forget()
            self.level_name_frame.pack(pady=50, padx=50, fill="both", expand=True)

    def update_creation_scrollregion(self, event):
        """Update the scroll region for question creation"""
        self.creation_canvas.configure(scrollregion=self.creation_canvas.bbox("all"))

    def update_creation_canvas_width(self, event):
        """Update the width of the creation canvas window"""
        self.creation_canvas.itemconfig(self.creation_window, width=event.width-20)

    def on_creation_mousewheel(self, event):
        """Handle mousewheel scrolling in creation frame"""
        if self.question_creation_frame.winfo_ismapped():
            self.creation_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


    def hide_all_frames(self):
        """Hide all frames in the application to prevent frame stacking issues"""
        # Main frames
        if hasattr(self, 'main_menu_frame'):
            self.main_menu_frame.pack_forget()
        if hasattr(self, 'load_level_frame'):
            self.load_level_frame.pack_forget()
        if hasattr(self, 'game_configuration_frame'):
            self.game_configuration_frame.pack_forget()
        if hasattr(self, 'level_frame'):
            self.level_frame.pack_forget()
        if hasattr(self, 'level_completed_frame'):
            self.level_completed_frame.pack_forget()
        
        # Level modification frames
        if hasattr(self, 'modify_levels_frame'):
            self.modify_levels_frame.pack_forget()
        if hasattr(self, 'question_selection_frame'):
            self.question_selection_frame.pack_forget()
        if hasattr(self, 'question_editor_frame'):
            self.question_editor_frame.pack_forget()
        
        # Level creation frames
        if hasattr(self, 'level_name_frame'):
            self.level_name_frame.pack_forget()
        if hasattr(self, 'question_creation_frame'):
            self.question_creation_frame.pack_forget()

    
    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = App()
    app.run()