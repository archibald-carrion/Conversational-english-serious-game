# view/create_levels_view.py
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import pygame
from CTkMessagebox import CTkMessagebox  # Import the message box component

class CreateLevelsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent
        
        # Initialize pygame mixer for audio preview
        pygame.mixer.init()
        self.current_audio = None
        
        # Store questions as we create them
        self.questions = []
        self.current_question_index = 0
        self.total_questions = 10  # Keep this as 10 for display purposes
        self.zero_indexed_questions = range(0, 10)  # 0-9 indexing
        
        # Create the level name UI
        self.create_level_name_view()
        # Create the question creation UI (hidden initially)
        self.create_question_creation_view()
        # Create the completion UI (hidden initially)
        self.create_completion_view()

    def create_level_name_view(self):
        """Initialize the level name frame and its components"""
        # Main container for level name UI
        self.level_name_frame = ctk.CTkFrame(self)
        self.level_name_frame.pack(fill="both", expand=True)
        
        # Add a scrollable frame inside the main frame
        self.level_name_scrollable = ctk.CTkScrollableFrame(self.level_name_frame)
        self.level_name_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Main title
        title = ctk.CTkLabel(
            self.level_name_scrollable, 
            text="Create New Level", 
            font=("Helvetica", 24)
        )
        title.pack(pady=30)

        # Create the entry for level name
        level_label = ctk.CTkLabel(
            self.level_name_scrollable,
            text="Enter a Name for the New Level:",
            font=("Helvetica", 16)
        )
        level_label.pack(pady=(20, 5))
        
        self.level_name_entry = ctk.CTkEntry(
            self.level_name_scrollable,
            width=300,
            placeholder_text="Level Name"
        )
        self.level_name_entry.pack(pady=10)

        # Create buttons
        buttons = [
            ("Start Creating Questions", self.start_question_creation),
            ("Back to Menu", self.back_to_main_menu)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.level_name_scrollable,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10)

    def create_question_creation_view(self):
        """Initialize the question creation frame and its components"""
        # Main container for question creation UI
        self.question_creation_frame = ctk.CTkFrame(self)
        
        # Add a scrollable frame inside the main frame
        self.question_creation_scrollable = ctk.CTkScrollableFrame(self.question_creation_frame)
        self.question_creation_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.question_header = ctk.CTkLabel(
            self.question_creation_scrollable, 
            text="Creating Question 1 of 10", 
            font=("Helvetica", 24)
        )
        self.question_header.pack(pady=20)
        
        # Level info label
        self.level_info_label = ctk.CTkLabel(
            self.question_creation_scrollable,
            text="Level: None",
            font=("Helvetica", 16)
        )
        self.level_info_label.pack(pady=10)
        
        # Question text entry
        question_label = ctk.CTkLabel(
            self.question_creation_scrollable,
            text="Question Text:",
            font=("Helvetica", 16),
            anchor="w"
        )
        question_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.question_entry = ctk.CTkTextbox(
            self.question_creation_scrollable,
            height=100,
            width=500
        )
        self.question_entry.pack(pady=(0, 10), padx=20, fill="x")
                
        # Answer entries
        answers_label = ctk.CTkLabel(
            self.question_creation_scrollable,
            text="Answer Options:",
            font=("Helvetica", 16),
            anchor="w"
        )
        answers_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        # Create entries for three answers
        self.answer_entries = []
        self.answer_frames = []
        
        for i in range(3):
            answer_frame = ctk.CTkFrame(self.question_creation_scrollable)
            answer_frame.pack(pady=5, padx=20, fill="x")
            self.answer_frames.append(answer_frame)
            
            # Answer text entry
            entry = ctk.CTkEntry(
                answer_frame,
                placeholder_text=f"Answer {i+1}",
                width=400
            )
            entry.pack(side="left", padx=10, fill="x", expand=True)
            self.answer_entries.append(entry)

        # Add dropdown for correct answer selection
        correct_answer_frame = ctk.CTkFrame(self.question_creation_scrollable)
        correct_answer_frame.pack(pady=10, padx=20, fill="x")
        
        correct_answer_label = ctk.CTkLabel(
            correct_answer_frame,
            text="Correct Answer:",
            font=("Helvetica", 14),
            anchor="w"
        )
        correct_answer_label.pack(side="left", padx=5)
        
        # Create string variable for dropdown
        self.correct_answer_var = ctk.StringVar(value="Answer 1")
        
        # Create the dropdown for correct answer selection
        self.correct_answer_dropdown = ctk.CTkOptionMenu(
            correct_answer_frame,
            values=["Answer 1", "Answer 2", "Answer 3"],
            variable=self.correct_answer_var
        )
        self.correct_answer_dropdown.pack(side="left", padx=10)
        
        # Media section - Image
        media_label = ctk.CTkLabel(
            self.question_creation_scrollable,
            text="Media Files (Optional):",
            font=("Helvetica", 16),
            anchor="w"
        )
        media_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Image selection
        image_frame = ctk.CTkFrame(self.question_creation_scrollable)
        image_frame.pack(pady=5, padx=20, fill="x")
        
        image_label = ctk.CTkLabel(image_frame, text="Image:")
        image_label.pack(side="left", padx=5)
        
        self.image_path_var = ctk.StringVar(value="")
        self.image_display = ctk.CTkLabel(image_frame, text="No image selected", width=200)
        self.image_display.pack(side="left", padx=10, fill="x", expand=True)
        
        image_button = ctk.CTkButton(
            image_frame,
            text="Browse...",
            command=self.browse_image,
            width=100
        )
        image_button.pack(side="right", padx=10)
        
        # Display image preview
        self.image_preview_frame = ctk.CTkFrame(
            self.question_creation_scrollable,
            width=300,
            height=200
        )
        self.image_preview_frame.pack(pady=10, padx=20)
        self.image_preview_label = ctk.CTkLabel(self.image_preview_frame, text="")
        self.image_preview_label.pack(fill="both", expand=True)
        
        # Audio selection
        audio_frame = ctk.CTkFrame(self.question_creation_scrollable)
        audio_frame.pack(pady=5, padx=20, fill="x")
        
        audio_label = ctk.CTkLabel(audio_frame, text="Audio:")
        audio_label.pack(side="left", padx=5)
        
        self.audio_path_var = ctk.StringVar(value="")
        self.audio_display = ctk.CTkLabel(audio_frame, text="No audio selected", width=200)
        self.audio_display.pack(side="left", padx=10, fill="x", expand=True)
        
        audio_button = ctk.CTkButton(
            audio_frame,
            text="Browse...",
            command=self.browse_audio,
            width=100
        )
        audio_button.pack(side="right", padx=10)
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.question_creation_scrollable)
        button_frame.pack(pady=20, fill="x")
        
        self.next_btn = ctk.CTkButton(
            button_frame,
            text="Next Question",
            command=self.save_and_next,
            width=150
        )
        self.next_btn.pack(side="right", padx=10, pady=10)

        self.cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.back_to_level_name,
            width=150
        )
        self.cancel_btn.pack(side="left", padx=10, pady=10)

    def create_completion_view(self):
        """Initialize the completion frame and its components"""
        # Main container for completion UI
        self.completion_frame = ctk.CTkFrame(self)
        
        # Add a main frame inside
        self.completion_main = ctk.CTkFrame(self.completion_frame)
        self.completion_main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkLabel(
            self.completion_main, 
            text="Level Creation Complete!", 
            font=("Helvetica", 24)
        )
        header.pack(pady=30)
        
        # Summary info
        self.level_summary = ctk.CTkLabel(
            self.completion_main,
            text="",
            font=("Helvetica", 16)
        )
        self.level_summary.pack(pady=20)
        
        # Question count
        self.question_count = ctk.CTkLabel(
            self.completion_main,
            text="",
            font=("Helvetica", 14)
        )
        self.question_count.pack(pady=10)
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.completion_main)
        button_frame.pack(pady=30, fill="x")
        
        create_another_btn = ctk.CTkButton(
            button_frame,
            text="Create Another Level",
            command=self.create_another_level,
            width=200
        )
        create_another_btn.pack(side="left", padx=20, pady=10)

        menu_btn = ctk.CTkButton(
            button_frame,
            text="Back to Main Menu",
            command=self.back_to_main_menu,
            width=200
        )
        menu_btn.pack(side="right", padx=20, pady=10)

    def start_question_creation(self):
        """Start the question creation process"""
        level_name = self.level_name_entry.get().strip()
        
        if not level_name:
            # Show popup message box instead of print
            CTkMessagebox(
                title="Error",
                message="Level name cannot be empty.",
                icon="warning"
            )
            return
        
        # Reset questions list
        self.questions = []
        self.current_question_index = 0  # Now represents question 0
        
        # Update level info
        self.level_info_label.configure(text=f"Level: {level_name}")
        
        # Update question header - keep the display as 1-based for user-friendliness
        self.question_header.configure(text=f"Creating Question {self.current_question_index + 1} of {self.total_questions}")
        
        # Clear form fields
        self.clear_question_form()
        
        # Show question creation view
        self.show_question_creation_view()

    def clear_question_form(self):
        """Clear all form fields"""
        # Clear question text
        self.question_entry.delete("0.0", "end")
        
        # Clear answers
        for entry in self.answer_entries:
            entry.delete(0, "end")
        
        # Reset dropdown
        default_options = ["Answer 1", "Answer 2", "Answer 3"]
        self.correct_answer_dropdown.configure(values=default_options)
        self.correct_answer_dropdown.set(default_options[0])
        
        # Clear image
        self.image_path_var.set("")
        self.clear_image_preview()
        self.image_display.configure(text="No image selected")
        
        # Clear audio
        self.audio_path_var.set("")
        self.audio_display.configure(text="No audio selected")
        
        # Stop any playing audio
        if self.current_audio:
            pygame.mixer.music.stop()
            self.current_audio = None

    def update_answer_dropdown(self):
        """Update the dropdown with current answer entries"""
        answer_texts = []
        for i, entry in enumerate(self.answer_entries):
            text = entry.get().strip()
            if text:
                # Show abbreviated text in dropdown
                display_text = text if len(text) <= 20 else f"{text[:20]}..."
                answer_texts.append(f"Answer {i+1}: {display_text}")
            else:
                answer_texts.append(f"Answer {i+1}: (empty)")
        
        # Update dropdown values if we have answers
        if answer_texts:
            self.correct_answer_dropdown.configure(values=answer_texts)

    def get_correct_answer_index(self):
        """Extract the index of the selected correct answer from dropdown"""
        selected_option = self.correct_answer_dropdown.get()
        try:
            # Extract number from "Answer X: text"
            answer_num = int(selected_option.split(":")[0].replace("Answer ", ""))
            return str(answer_num - 1)  # Convert to 0-based index as string
        except (ValueError, IndexError):
            return "0"  # Default to first answer

    def save_and_next(self):
        """Save the current question and proceed to the next one"""
        # Get current question data
        question_text = self.question_entry.get("0.0", "end-1c").strip()

        if not question_text:
            # Show popup message box instead of print
            CTkMessagebox(
                title="Error",
                message="Question text cannot be empty.",
                icon="warning"
            )
            return
        
        answers = {}
        empty_answers = 0
        for i, entry in enumerate(self.answer_entries):
            answer_text = entry.get().strip()
            if answer_text:
                answers[str(i)] = answer_text  # Already using 0-based indexing for answers
            else:
                empty_answers += 1
        
        # Ensure we have all answers filled
        if len(answers) < 3:
            # Show popup message box instead of print
            CTkMessagebox(
                title="Error",
                message="You must provide all three answer options.",
                icon="warning"
            )
            return
        
        # Get correct answer from dropdown
        correct_answer = self.get_correct_answer_index()
        
        # Ensure correct answer has content
        if correct_answer not in answers:
            # Show popup message box instead of print
            CTkMessagebox(
                title="Error",
                message="You must select a valid answer as correct.",
                icon="warning"
            )
            return
        
        # Create question data - using 0-based indexing internally
        question_data = {
            "question_index": self.current_question_index,  # 0-based
            "question": question_text,
            "answers": answers,
            "correct_answer": correct_answer,
            "image_file": self.image_path_var.get(),
            "audio_file": self.audio_path_var.get()
        }
        
        # Add question to our list
        self.questions.append(question_data)
        
        # Increment question index
        self.current_question_index += 1
        
        # Check if we've completed all questions - comparing against total_questions
        if self.current_question_index >= self.total_questions:
            # Save the level
            self.save_level()
        else:
            # Update for next question - but display user-friendly 1-based numbering
            self.question_header.configure(
                text=f"Creating Question {self.current_question_index + 1} of {self.total_questions}"
            )
            
            # Update next button text for last question
            if self.current_question_index == self.total_questions - 1:
                self.next_btn.configure(text="Complete Level")
            
            # Clear form for next question
            self.clear_question_form()

    def save_level(self):
        """Save all questions as a new level"""
        level_name = self.level_name_entry.get().strip()
        
        # Create level data
        level_data = {
            "name": level_name,
            "questions": self.questions
        }
        
        # Save level using controller
        success = self.controller.create_new_level(level_data)
        
        if success:
            # Update completion view
            self.level_summary.configure(text=f"Level '{level_name}' has been created.")
            self.question_count.configure(text=f"Total questions: {len(self.questions)}")
            
            # Show completion view
            self.show_completion_view()
        else:
            # Show popup message box instead of print
            CTkMessagebox(
                title="Error",
                message="Failed to save level. Please try again.",
                icon="error"
            )

    def browse_image(self):
        """Open file dialog to select an image"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.image_path_var.set(file_path)
            self.image_display.configure(text=os.path.basename(file_path))
            self.display_image_preview(file_path)

    def browse_audio(self):
        """Open file dialog to select audio"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Select Audio",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.ogg"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            self.audio_path_var.set(file_path)
            self.audio_display.configure(text=os.path.basename(file_path))
            
            # Preview audio
            try:
                # Stop previous audio if playing
                if self.current_audio:
                    pygame.mixer.music.stop()
                
                # Load and play new audio
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                self.current_audio = file_path
            except Exception as e:
                # Show popup message box instead of print
                CTkMessagebox(
                    title="Error",
                    message=f"Error playing audio: {e}",
                    icon="error"
                )

    def display_image_preview(self, image_path):
        """Display an image preview"""
        try:
            # Use PIL to open and resize the image
            pil_image = Image.open(image_path)
            # Resize to fit frame while preserving aspect ratio
            max_width, max_height = 300, 200
            pil_image.thumbnail((max_width, max_height))
            
            # Convert to Tkinter-compatible format
            tk_image = ImageTk.PhotoImage(pil_image)
            
            # Update label with the image
            self.image_preview_label.configure(image=tk_image)
            # Keep a reference to prevent garbage collection
            self.image_preview_label.image = tk_image
        except Exception as e:
            # Show popup message box instead of print
            CTkMessagebox(
                title="Error",
                message=f"Error loading image: {e}",
                icon="error"
            )
            self.clear_image_preview()

    def clear_image_preview(self):
        """Clear the image preview"""
        self.image_preview_label.configure(image=None)
        self.image_preview_label.image = None

    def create_another_level(self):
        """Start creating another level"""
        # Reset everything
        self.questions = []
        self.current_question_index = 0
        self.level_name_entry.delete(0, "end")
        
        # Show level name view
        self.show_level_name_view()

    def show_level_name_view(self):
        """Show the level name view"""
        # Hide other frames
        if hasattr(self, 'question_creation_frame'):
            self.question_creation_frame.pack_forget()
        if hasattr(self, 'completion_frame'):
            self.completion_frame.pack_forget()
        
        # Show level name frame
        self.level_name_frame.pack(fill="both", expand=True)

    def show_question_creation_view(self):
        """Show the question creation view"""
        # Hide other frames
        self.level_name_frame.pack_forget()
        if hasattr(self, 'completion_frame'):
            self.completion_frame.pack_forget()
        
        # Show question creation frame
        self.question_creation_frame.pack(fill="both", expand=True)

    def show_completion_view(self):
        """Show the completion view"""
        # Hide other frames
        self.level_name_frame.pack_forget()
        self.question_creation_frame.pack_forget()
        
        # Show completion frame
        self.completion_frame.pack(fill="both", expand=True)

    def back_to_level_name(self):
        """Go back to level name view"""
        # Confirm with user that progress will be lost
        if self.questions:
            # Show a confirmation dialog
            confirm = CTkMessagebox(
                title="Confirm",
                message="Going back will discard your current progress. Continue?",
                icon="question",
                option_1="Yes",
                option_2="No"
            )
            if confirm.get() == "No":
                return
        
        # Reset questions
        self.questions = []
        self.current_question_index = 0
        
        # Show level name view
        self.show_level_name_view()

    def back_to_main_menu(self):
        """Go back to the main menu"""
        # Check if we're in the completion view (where no confirmation is needed)
        if hasattr(self, 'completion_frame') and self.completion_frame.winfo_ismapped():
            # Skip confirmation if we're in the completion view
            pass
        # If we have questions in progress, confirm with user
        elif hasattr(self, 'questions') and self.questions:
            confirm = CTkMessagebox(
                title="Confirm",
                message="Going back to menu will discard your current progress. Continue?",
                icon="question",
                option_1="Yes",
                option_2="No"
            )
            if confirm.get() == "No":
                return
        
        # This will be called by the switch_view function from main.py
        from app import switch_view
        
        # Import here to avoid circular imports
        from view.menu_view import MenuView
        
        # Find the menu view in the parent's children
        for child in self.parent.winfo_children():
            if isinstance(child, MenuView):
                switch_view(self.parent, child)
                break