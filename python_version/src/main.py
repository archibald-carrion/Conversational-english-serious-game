import customtkinter as ctk
from levels_manager import LevelsManager
from PIL import Image
import os
import threading
from playsound import playsound
from tkinter import filedialog
import pygame

class App:
    def __init__(self):

        # Add a score attribute and initialize to 0
        self.current_score = 0
        self.total_possible_score = 0

        self.levels_manager = LevelsManager('levels.json')

        self.current_level = None

        # Configure the main window
        self.root = ctk.CTk()
        self.root.title("Level Selector")
        self.root.geometry("1280x720")
        self.root.resizable(False, False)
        # self.root.attributes('-transparentcolor', '#000001')  # Specify a color to make transparent
        # self.root.configure(bg='#000001')  # Match this color with the transparency attribute
        self.root.bind("<Escape>", lambda e: self.root.quit())

        # Set appearance and color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # # Set the background image - UPDATED PLACEMENT
        # self.bg_image = ctk.CTkImage(
        #     light_image=Image.open("assets/images/background.png"), 
        #     dark_image=Image.open("assets/images/background.png"),
        #     size=(800, 600)  # Explicitly set size to match window
        # )
        # self.my_background = ctk.CTkLabel(self.root, text="", image=self.bg_image)
        # self.my_background.place(x=0, y=0, relwidth=1, relheight=1)  # Ensure full coverage


        ''' Main Menu '''
        
        # Create main menu frame
        self.main_menu_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_menu_frame.pack(pady=50, padx=100, fill="both", expand=True, anchor="w")

        # Main menu title
        self.menu_title = ctk.CTkLabel(
            self.main_menu_frame, 
            text="Level Manager", 
            font=("Helvetica", 24)
        )
        self.menu_title.pack(pady=50)

        # Load Level Button
        self.load_level_btn = ctk.CTkButton(
            self.main_menu_frame, 
            text="Load Level", 
            command=self.open_load_level_window
        )
        self.load_level_btn.pack(pady=10)

        # Update the Modify Levels Button command
        self.modify_levels_btn = ctk.CTkButton(
            self.main_menu_frame, 
            text="Modify Levels",
            command=self.open_modify_levels_window
        )
        self.modify_levels_btn.pack(pady=10)

        # create new level button
        self.create_level_btn = ctk.CTkButton(
            self.main_menu_frame,
            text="Create New Level",
            command=self.create_new_level
        )
        self.create_level_btn.pack(pady=10)

        # Game Configuration Button
        self.game_configuration_btn = ctk.CTkButton(
            self.main_menu_frame, 
            text="Game Configuration", 
            command=self.open_game_configuration_window
        )
        self.game_configuration_btn.pack(pady=10)

        # Quit Button
        self.quit_btn = ctk.CTkButton(
            self.main_menu_frame, 
            text="Quit Game", 
            command=self.root.quit
        )
        self.quit_btn.pack(pady=10)


        ''' Load Level Frame '''

        # Load Level Frame (initially hidden)
        self.load_level_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        # Level Dropdown
        self.level_dropdown = ctk.CTkOptionMenu(
            self.load_level_frame, 
            values=self.levels_manager.get_level_names()
        )
        self.level_dropdown.pack(pady=20)

        # Load Button in Level Selection
        self.confirm_load_btn = ctk.CTkButton(
            self.load_level_frame, 
            text="Load Selected Level",
            command=self.load_selected_level
        )
        self.confirm_load_btn.pack(pady=10)

        # Back Button
        self.back_btn = ctk.CTkButton(
            self.load_level_frame, 
            text="Back to Menu", 
            command=self.back_to_main_menu
        )
        self.back_btn.pack(pady=10)

        

        ''' Game Configuration Frame '''

        # Game configuration Frame (initially hidden)
        self.game_configuration_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        # Game Title
        self.game_title = ctk.CTkLabel(
            self.game_configuration_frame, 
            text="Game Configuration", 
            font=("Helvetica", 24)
        )

        # drop doiwn button with different window sizes 
        self.window_size_dropdown = ctk.CTkOptionMenu(
            self.game_configuration_frame, 
            values=["800x600", "1280x720", "1920x1080"],
            command=self.update_window_size
        )
        self.window_size_dropdown.pack(pady=20)

        # button at the right of the dropdown to confirm the selection
        self.confirm_window_size_btn = ctk.CTkButton(
            self.game_configuration_frame, 
            text="Confirm Window Size",
            command=self.apply_window_size
        )
        self.confirm_window_size_btn.pack(pady=10)

        # back button to go back to the main menu
        self.back_to_menu_btn = ctk.CTkButton(
            self.game_configuration_frame, 
            text="Back to Menu", 
            command=self.back_to_main_menu
        )
        self.back_to_menu_btn.pack(pady=10)


        ''' Level frame '''

        # Level Frame (initially hidden)
        self.level_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        # Level Title
        self.level_title = ctk.CTkLabel(
            self.level_frame,
            text="",
            font=("Helvetica", 24)
        )
        self.level_title.pack(pady=20)

        # Question Text
        self.question_text = ctk.CTkLabel(
            self.level_frame,
            text="",
            wraplength=600,
            font=("Helvetica", 18)
        )
        self.question_text.pack(pady=20)

        # Answer Buttons
        self.answer_buttons = []
        for i in range(3):
            button = ctk.CTkButton(
                self.level_frame,
                text="",
                command=lambda index=i: self.handle_answer_click(index),
                width=400,
                height=50
            )
            self.answer_buttons.append(button)
            button.pack(pady=10)

        # Back Button
        self.back_button = ctk.CTkButton(
            self.level_frame,
            text="Back to Menu",
            command=self.back_to_main_menu,
            width=200,
            height=40
        )
        self.back_button.pack(pady=20)

        self.score_display = ctk.CTkLabel(
            self.level_frame,
            text=f"Score: {self.current_score}",
            font=("Helvetica", 16),
            text_color="white"
        )
        self.score_display.place(relx=0.95, rely=0.05, anchor="ne")  # Top-right corner

        # Add audio replay button to the level frame
        self.replay_audio_btn = ctk.CTkButton(
            self.level_frame,
            text="🔊 Replay Audio",
            command=self.replay_audio,
            width=200,
            height=40
        )
        self.replay_audio_btn.pack(pady=10)

        # Add a flag to track audio playback
        self.is_audio_playing = False

        ''' Level Completed Frame '''

        # Level Completed Frame (initially hidden)
        self.level_completed_frame = ctk.CTkFrame(self.root, fg_color="transparent")

        # Completion Message
        self.completion_message = ctk.CTkLabel(
            self.level_completed_frame,
            text="Level Completed!",
            font=("Helvetica", 24),
            text_color="green"
        )
        self.completion_message.pack(pady=20)

        # Score Display
        self.score_label = ctk.CTkLabel(
            self.level_completed_frame,
            text="Your Score: 0",
            font=("Helvetica", 20)
        )
        self.score_label.pack(pady=10)

        # Button to return to the main menu
        self.return_to_menu_btn = ctk.CTkButton(
            self.level_completed_frame,
            text="Return to Main Menu",
            command=self.back_to_main_menu
        )
        self.return_to_menu_btn.pack(pady=20)


         

        # Add new frames for level modification

        ''' Modify Levels Frame '''
        self.modify_levels_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Level selection dropdown
        self.modify_level_dropdown = ctk.CTkOptionMenu(
            self.modify_levels_frame,
            values=self.levels_manager.get_level_names()
        )
        self.modify_level_dropdown.pack(pady=20)

        # Select level button
        self.select_level_btn = ctk.CTkButton(
            self.modify_levels_frame,
            text="Select Level",
            command=self.open_question_selection
        )
        self.select_level_btn.pack(pady=10)

        # Back button
        self.modify_back_btn = ctk.CTkButton(
            self.modify_levels_frame,
            text="Back to Menu",
            command=self.back_to_main_menu
        )
        self.modify_back_btn.pack(pady=10)

        ''' Question Selection Frame '''
        self.question_selection_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Question selection dropdown (will be populated when level is selected)
        self.question_dropdown = ctk.CTkOptionMenu(
            self.question_selection_frame,
            values=[""]
        )
        self.question_dropdown.pack(pady=20)

        # Select question button
        self.select_question_btn = ctk.CTkButton(
            self.question_selection_frame,
            text="Modify Selected Question",
            command=self.open_question_editor
        )
        self.select_question_btn.pack(pady=10)

        # Back button
        self.question_select_back_btn = ctk.CTkButton(
            self.question_selection_frame,
            text="Back to Level Selection",
            command=self.back_to_modify_levels
        )
        self.question_select_back_btn.pack(pady=10)

        ''' Question Editor Frame '''
        # Create main frame
        self.question_editor_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        
        # Create a canvas with scrollbar
        self.editor_canvas = ctk.CTkCanvas(
            self.question_editor_frame,
            width=700,
            height=500,
            bg='#2b2b2b',  # Match dark theme
            highlightthickness=0
        )
        self.editor_scrollbar = ctk.CTkScrollbar(
            self.question_editor_frame,
            orientation="vertical",
            command=self.editor_canvas.yview
        )
        self.editor_canvas.configure(yscrollcommand=self.editor_scrollbar.set)

        # Create a frame inside canvas for content
        self.editor_content_frame = ctk.CTkFrame(self.editor_canvas, fg_color="transparent")

        # Pack scrollbar and canvas
        self.editor_scrollbar.pack(side="right", fill="y")
        self.editor_canvas.pack(side="left", fill="both", expand=True, padx=5)

        # Create window in canvas
        self.canvas_frame = self.editor_canvas.create_window(
            (0, 0),
            window=self.editor_content_frame,
            anchor="nw",
            width=680  # Slightly less than canvas width
        )

        # Question text entry
        self.question_label = ctk.CTkLabel(
            self.editor_content_frame,
            text="Question:"
        )
        self.question_label.pack(pady=3)
        
        self.question_entry = ctk.CTkTextbox(
            self.editor_content_frame,
            height=80,  # Reduced height
            width=600
        )
        self.question_entry.pack(pady=5)

        # Answer entries
        self.answer_entries = []
        for i in range(3):
            label = ctk.CTkLabel(
                self.editor_content_frame,
                text=f"Answer {i+1}:"
            )
            label.pack(pady=2)
            
            entry = ctk.CTkEntry(
                self.editor_content_frame,
                width=500
            )
            entry.pack(pady=3)
            self.answer_entries.append(entry)

        # Correct answer selection
        self.correct_answer_label = ctk.CTkLabel(
            self.editor_content_frame,
            text="Correct Answer (0-2):"
        )
        self.correct_answer_label.pack(pady=2)
        
        self.correct_answer_entry = ctk.CTkEntry(
            self.editor_content_frame,
            width=50
        )
        self.correct_answer_entry.pack(pady=3)

        # Audio file selection
        self.audio_path_label = ctk.CTkLabel(
            self.editor_content_frame,
            text="Current Audio File: None",
            wraplength=500  # Prevent long paths from expanding the window
        )
        self.audio_path_label.pack(pady=2)

        self.select_audio_btn = ctk.CTkButton(
            self.editor_content_frame,
            text="Select Audio File",
            command=self.select_audio_file
        )
        self.select_audio_btn.pack(pady=3)

        # Save changes button
        self.save_changes_btn = ctk.CTkButton(
            self.editor_content_frame,
            text="Save Changes",
            command=self.save_question_changes
        )
        self.save_changes_btn.pack(pady=3)

        # Back button
        self.editor_back_btn = ctk.CTkButton(
            self.editor_content_frame,
            text="Back to Question Selection",
            command=self.back_to_question_selection
        )
        self.editor_back_btn.pack(pady=3)

        # Bind canvas configuration to update scroll region
        self.editor_content_frame.bind("<Configure>", self.update_scrollregion)
        self.editor_canvas.bind("<Configure>", self.update_canvas_width)

        # Bind mousewheel to scroll
        self.editor_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def create_new_level(self):
        print("Create new level")

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
        # Hide load level frame
        self.load_level_frame.pack_forget()
        # Hide game configuration frame
        self.game_configuration_frame.pack_forget()
        # Hide level frame
        self.level_frame.pack_forget()
        # Hide level completed frame
        self.level_completed_frame.pack_forget()
        # Hide modify levels frame
        self.modify_levels_frame.pack_forget()
        # Hide question selection frame
        self.question_selection_frame.pack_forget()
        # Hide question editor frame
        self.question_editor_frame.pack_forget()
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
    
    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = App()
    app.run()