import customtkinter as ctk
from PIL import Image, ImageTk
import os
import pygame  # For audio playback

class PlayLevelsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent
        
        # Score tracking
        self.question_attempts = {}  # To track attempts per question
        self.score = 0
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        self.current_audio = None
        
        # Create the play levels UI
        self.create_play_levels_view()
        # Initialize game components (hidden initially)
        self.create_game_components()

    def create_play_levels_view(self):
        """Initialize the play levels frame and its components"""
        # Main container for selection UI
        self.selection_frame = ctk.CTkFrame(self)
        self.selection_frame.pack(fill="both", expand=True)
        
        # Main title
        title = ctk.CTkLabel(
            self.selection_frame, 
            text="Load Level", 
            font=("Helvetica", 24)
        )
        title.pack(pady=30)

        # Create the dropdown for level selection
        self.level_dropdown = ctk.CTkOptionMenu(
            self.selection_frame,
            values=[]  # Start with empty list
        )
        self.level_dropdown.pack(pady=20)

        # Create buttons
        buttons = [
            ("Load Selected Level", self.load_selected_level),
            ("Back to Menu", self.back_to_main_menu)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.selection_frame,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10)

    def create_game_components(self):
        """Create the game UI components (hidden initially)"""
        # Main container for game UI
        self.game_frame = ctk.CTkFrame(self)
        
        # Question counter
        self.question_counter = ctk.CTkLabel(
            self.game_frame,
            text="Question 1/10",
            font=("Helvetica", 14)
        )
        self.question_counter.pack(pady=(20, 5))
        
        # Question display
        self.question_label = ctk.CTkLabel(
            self.game_frame,
            text="",
            font=("Helvetica", 18),
            wraplength=500
        )
        self.question_label.pack(pady=(5, 20))
        
        # Replay audio button
        self.replay_button = ctk.CTkButton(
            self.game_frame,
            text="Replay Audio",
            command=self.replay_audio,
            width=150,
            state="disabled"  # Initially disabled until audio is played
        )
        self.replay_button.pack(pady=10)
        
        # Image frame
        self.image_frame = ctk.CTkFrame(
            self.game_frame,
            width=300,
            height=200
        )
        self.image_frame.pack(pady=20)
        self.image_label = ctk.CTkLabel(self.image_frame, text="")
        self.image_label.pack(fill="both", expand=True)
        
        # Answer buttons container
        self.answers_frame = ctk.CTkFrame(self.game_frame)
        self.answers_frame.pack(pady=20, fill="x")
        
        # Create three answer buttons
        self.answer_buttons = []
        for i in range(3):
            btn = ctk.CTkButton(
                self.answers_frame,
                text=f"Answer {i+1}",
                command=lambda idx=i: self.select_answer(idx),
                width=200
            )
            btn.pack(pady=10)
            self.answer_buttons.append(btn)
        
        # Back button for the game view
        self.back_button = ctk.CTkButton(
            self.game_frame,
            text="Back to Level Selection",
            command=self.back_to_level_selection,
            width=200
        )
        self.back_button.pack(pady=20)
        
        # Don't pack the game_frame initially - it will be hidden

    def update_level_dropdown(self):
        """Update the level dropdown with available levels"""
        # Get levels from controller
        levels = self.controller.get_available_levels()
        
        # If we have levels, update the dropdown
        if levels:
            self.level_dropdown.configure(values=levels)
            self.level_dropdown.set(levels[0])  # Set first level as default
        else:
            self.level_dropdown.configure(values=["No levels available"])
            self.level_dropdown.set("No levels available")

    def load_selected_level(self):
        """Call controller to load the selected level and switch to game view"""
        selected_level = self.level_dropdown.get()
        
        # Only proceed if a valid level is selected
        if selected_level != "No levels available":
            success = self.controller.load_level(selected_level)
            
            if success:
                # Reset score and attempts for new level
                self.score = 0
                self.question_attempts = {}
                
                # Switch to game view
                self.show_game_view()
                
                # Load the first question
                self.load_question()
            else:
                # Show error message
                print(f"Failed to load level '{selected_level}'")

    def show_game_view(self):
        """Hide selection view and show game view"""
        self.selection_frame.pack_forget()
        self.game_frame.pack(fill="both", expand=True)

    def back_to_level_selection(self):
        """Hide game view and show selection view"""
        self.game_frame.pack_forget()
        self.selection_frame.pack(fill="both", expand=True)
        
        # Stop any playing audio when leaving the game view
        self.stop_audio()

    def load_question(self):
        """Load the current question from the controller"""
        # reset attempts 
        self.attempts = 0

        # Get current question data from controller
        question_data = self.controller.get_current_question()
        # the returned index is 1 to 10
        current_question_index = self.controller.get_current_question_index()
        total_questions = 10 # TODO: change this to be class variable instead of local
        # self.controller.get_total_questions()
        
        # Update question counter
        self.question_counter.configure(
            text=f"Question {current_question_index}/{total_questions}"
        )
        
        if question_data:
            # Initialize attempts counter for this question if it doesn't exist
            question_id = question_data.get("id", current_question_index)
            if question_id not in self.question_attempts:
                self.question_attempts[question_id] = 0
            
            # Clear selected answers for this new question
            if hasattr(self, 'selected_answers'):
                self.selected_answers[question_id] = set()
                
            # Update question text
            self.question_label.configure(text=question_data.get("question", ""))
            
            # Update answer buttons
            answers = question_data.get("answers", [])
            print("Answers:", answers)
            # Fixed code to fill buttons with answers
            for i, button in enumerate(self.answer_buttons):
                answer_key = str(i)  # Convert index to string key
                if answer_key in answers:
                    button.configure(
                        text=answers[answer_key],
                        fg_color="#1f6aa5",  # Reset to default color
                        state="normal"  # Enable all buttons for the new question
                    )
                    button.pack(pady=10)
                else:
                    button.pack_forget()  # Hide buttons if we don't have an answer for this index
            
            # Handle image
            image_path = question_data.get("image_path", "")
            if image_path and os.path.exists(image_path):
                self.display_image(image_path)
            else:
                # Hide or clear image
                self.clear_image()
                
            # Store audio path and play it automatically
            self.current_audio = question_data.get("audio_file", "")
            if not self.current_audio or not os.path.exists(self.current_audio):
                self.replay_button.configure(state="disabled")
            else:
                # Enable replay button
                self.replay_button.configure(state="normal")
                
                # Auto-play the audio after a short delay
                self.after(500, self.play_audio)

    def display_image(self, image_path):
        """Display an image in the image frame"""
        try:
            # Use PIL to open and resize the image
            pil_image = Image.open(image_path)
            # Resize to fit frame while preserving aspect ratio
            max_width, max_height = 300, 200
            pil_image.thumbnail((max_width, max_height))
            
            # Convert to Tkinter-compatible format
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # Update label with the image
            self.image_label.configure(image=tk_image)
            # Keep a reference to prevent garbage collection
            self.image_label.image = tk_image
        except Exception as e:
            print(f"Error loading image: {e}")
            self.clear_image()

    def clear_image(self):
        """Clear the image label"""
        self.image_label.configure(image=None)
        self.image_label.image = None

    def play_audio(self):
        """Play the audio for the current question"""
        if hasattr(self, 'current_audio') and self.current_audio and os.path.exists(self.current_audio):
            # Stop any currently playing audio
            self.stop_audio()
            
            # Play the new audio
            try:
                pygame.mixer.music.load(self.current_audio)
                pygame.mixer.music.play()
                
                # Disable replay button during playback
                self.replay_button.configure(state="disabled")
                
                # Re-enable replay button after audio finishes
                audio_length = self.get_audio_length(self.current_audio)
                self.after(int(audio_length * 1000), self.enable_replay_button)
            except Exception as e:
                print(f"Error playing audio: {e}")

    def replay_audio(self):
        """Replay the audio for the current question"""
        self.play_audio()

    def stop_audio(self):
        """Stop any currently playing audio"""
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def enable_replay_button(self):
        """Re-enable the replay button after audio finishes"""
        if hasattr(self, 'current_audio') and self.current_audio and os.path.exists(self.current_audio):
            self.replay_button.configure(state="normal")

    def get_audio_length(self, audio_path):
        """Get the length of an audio file in seconds"""
        try:
            sound = pygame.mixer.Sound(audio_path)
            return sound.get_length()
        except:
            # Default to 3 seconds if can't determine length
            return 3.0

    def select_answer(self, answer_idx):
        """Process the user's answer selection"""
        # Get current question ID
        question_data = self.controller.get_current_question()
        question_id = question_data.get("id", self.controller.get_current_question_index())
        
        # Initialize a set to track selected answers for this question if not already there
        if not hasattr(self, 'selected_answers'):
            self.selected_answers = {}
        
        if question_id not in self.selected_answers:
            self.selected_answers[question_id] = set()
        
        # Add this answer to the selected set
        self.selected_answers[question_id].add(answer_idx)
        
        # Increment attempts counter for this question
        self.question_attempts[question_id] = self.question_attempts.get(question_id, 0) + 1
        self.attempts += 1
        
        # Check if answer is correct
        result = self.controller.check_answer(answer_idx)
        
        if result:
            # Calculate score based on attempts
            if self.attempts == 1:
                # First attempt - 10 points
                points = 10
            elif self.attempts == 2:
                # Second attempt - 5 points
                points = 5
            else:
                # Third attempt - 2 points
                points = 2
                
            # Add points to total score
            self.score += points
            
            # Add visual feedback (show points gained)
            self.answer_buttons[answer_idx].configure(
                fg_color="green", 
                text=f"{self.answer_buttons[answer_idx].cget('text')} (+{points} pts)"
            )
            
            # Disable all buttons to prevent further selection after correct answer
            for btn in self.answer_buttons:
                btn.configure(state="disabled")
            
            # Disable replay button after correct answer
            self.replay_button.configure(state="disabled")
                
            # Load next question after a delay
            self.after(1500, self.load_next_question)
        else:
            # Wrong answer - no points, just visual feedback
            self.answer_buttons[answer_idx].configure(fg_color="red", state="disabled")
            
            # Check if this was the 3rd attempt
            if self.question_attempts[question_id] >= 3:
                # Highlight the correct answer if we've used all attempts
                correct_idx = self.get_correct_answer_index(question_data)
                if correct_idx is not None:
                    self.answer_buttons[correct_idx].configure(
                        fg_color="green",
                        text=f"{self.answer_buttons[correct_idx].cget('text')} (Correct)"
                    )
                
                # Disable all remaining buttons
                for idx, btn in enumerate(self.answer_buttons):
                    btn.configure(state="disabled")
                
                # Disable replay button
                self.replay_button.configure(state="disabled")
                    
                # Move to next question after a delay
                self.after(1500, self.load_next_question)

    def get_correct_answer_index(self, question_data):
        """Get the index of the correct answer"""
        correct_answer = question_data.get("correct_answer")
        if correct_answer is not None:
            try:
                return int(correct_answer)
            except (ValueError, TypeError):
                pass
        return None

    def load_next_question(self):
        """Load the next question or end the level"""
        current_question_index = self.controller.get_current_question_index()
        total_questions = 10 # TODO: change this to be class variable instead of local
        if current_question_index <= total_questions:
            # Load next question
            self.load_question()
        else:
            # End of level - show completion message
            self.show_level_complete()

    def show_level_complete(self):
        """Show level completion message and stats"""
        # Clear existing content
        for widget in self.game_frame.winfo_children():
            widget.pack_forget()
            
        # Show completion message
        completion_label = ctk.CTkLabel(
            self.game_frame,
            text="Level Complete!",
            font=("Helvetica", 24)
        )
        completion_label.pack(pady=30)
        
        # Calculate max possible score (10 points × 10 questions)
        max_score = 100
        
        # Display score
        score_label = ctk.CTkLabel(
            self.game_frame,
            text=f"Your Score: {self.score}/{max_score}",
            font=("Helvetica", 18)
        )
        score_label.pack(pady=10)
        
        # Calculate and display percentage
        percentage = (self.score / max_score) * 100
        percentage_label = ctk.CTkLabel(
            self.game_frame,
            text=f"Performance: {percentage:.1f}%",
            font=("Helvetica", 16)
        )
        percentage_label.pack(pady=5)
        
        # Performance feedback
        if percentage >= 90:
            feedback = "Excellent! Perfect score!"
        elif percentage >= 70:
            feedback = "Great job!"
        elif percentage >= 50:
            feedback = "Good effort!"
        else:
            feedback = "Keep practicing!"
            
        feedback_label = ctk.CTkLabel(
            self.game_frame,
            text=feedback,
            font=("Helvetica", 16)
        )
        feedback_label.pack(pady=5)
        
        # Save score to controller if implemented
        try:
            self.controller.save_level_score(self.score)
        except:
            pass
        
        # Back button
        back_btn = ctk.CTkButton(
            self.game_frame,
            text="Back to Level Selection",
            command=self.back_to_level_selection,
            width=200
        )
        back_btn.pack(pady=20)
        
        # Play again button
        replay_btn = ctk.CTkButton(
            self.game_frame,
            text="Play Again",
            command=self.replay_level,
            width=200
        )
        replay_btn.pack(pady=10)

    def replay_level(self):
        """Replay the current level"""
        # Reset score and attempts
        self.score = 0
        self.question_attempts = {}
        
        # Completely destroy the old game frame
        self.game_frame.destroy()
        
        # Create a new game frame and components
        self.create_game_components()
        
        # Show the game view again
        self.show_game_view()
        
        # Reset level in controller
        self.controller.reset_current_question_index()  # You need to implement this method in your controller
        
        # Load the first question
        self.load_question()

    def back_to_main_menu(self):
        """Go back to the main menu"""
        # This will be called by the switch_view function from main.py
        from app import switch_view
        
        # Import here to avoid circular imports
        from view.menu_view import MenuView
        
        # Find the menu view in the parent's children
        for child in self.parent.winfo_children():
            if isinstance(child, MenuView):
                switch_view(self.parent, child)
                break