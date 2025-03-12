# view/modify_levels_view.py
import customtkinter as ctk
import customtkinter as ctk
from PIL import Image, ImageTk
import os
import pygame

class ModifyLevelsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent
        
        # Initialize pygame mixer for audio preview
        pygame.mixer.init()
        self.current_audio = None
        
        # Create the level selection UI
        self.create_level_selection_view()
        # Create the question selection UI (hidden initially)
        self.create_question_selection_view()
        # Create the question editing UI (hidden initially)
        self.create_question_editor_view()

    def create_level_selection_view(self):
        """Initialize the level selection frame and its components"""
        # Main container for level selection UI
        self.level_selection_frame = ctk.CTkFrame(self)
        self.level_selection_frame.pack(fill="both", expand=True)
        
        # Main title
        title = ctk.CTkLabel(
            self.level_selection_frame, 
            text="Modify Questions", 
            font=("Helvetica", 24)
        )
        title.pack(pady=30)

        # Create the dropdown for level selection
        level_label = ctk.CTkLabel(
            self.level_selection_frame,
            text="Select a Level to Modify:",
            font=("Helvetica", 16)
        )
        level_label.pack(pady=(20, 5))
        
        self.level_dropdown = ctk.CTkOptionMenu(
            self.level_selection_frame,
            values=[]  # Start with empty list
        )
        self.level_dropdown.pack(pady=10)

        # Create buttons
        buttons = [
            ("Select Level", self.load_selected_level),
            ("Back to Menu", self.back_to_main_menu)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.level_selection_frame,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10)

    def create_question_selection_view(self):
        """Initialize the question selection frame and its components"""
        # Main container for question selection UI
        self.question_selection_frame = ctk.CTkFrame(self)
        
        # Header
        header = ctk.CTkLabel(
            self.question_selection_frame, 
            text="Select a Question to Modify", 
            font=("Helvetica", 24)
        )
        header.pack(pady=20)
        
        # Level info label
        self.level_info_label = ctk.CTkLabel(
            self.question_selection_frame,
            text="Current Level: None",
            font=("Helvetica", 16)
        )
        self.level_info_label.pack(pady=10)
        
        # Create a scrollable frame for questions
        self.questions_container = ctk.CTkScrollableFrame(
            self.question_selection_frame,
            width=500,
            height=300
        )
        self.questions_container.pack(pady=20, fill="both", expand=True)
        
        # Container for the action buttons
        button_frame = ctk.CTkFrame(self.question_selection_frame)
        button_frame.pack(pady=20, fill="x")
        
        # Add New Question button
        self.add_question_btn = ctk.CTkButton(
            button_frame,
            text="Add New Question",
            command=self.create_new_question,
            width=200
        )
        self.add_question_btn.pack(side="left", padx=10, pady=10)
        
        # Back button
        back_btn = ctk.CTkButton(
            button_frame,
            text="Back to Level Selection",
            command=self.back_to_level_selection,
            width=200
        )
        back_btn.pack(side="right", padx=10, pady=10)

    def create_question_editor_view(self):
        """Initialize the question editor frame and its components"""
        # Main container for question editor UI
        self.question_editor_frame = ctk.CTkFrame(self)
        
        # Header
        header = ctk.CTkLabel(
            self.question_editor_frame, 
            text="Edit Question", 
            font=("Helvetica", 24)
        )
        header.pack(pady=20)
        
        # Question ID display (hidden, for tracking)
        self.question_id_var = ctk.StringVar(value="")
        
        # Question text entry
        question_label = ctk.CTkLabel(
            self.question_editor_frame,
            text="Question Text:",
            font=("Helvetica", 16),
            anchor="w"
        )
        question_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.question_entry = ctk.CTkTextbox(
            self.question_editor_frame,
            height=100,
            width=500
        )
        self.question_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        # Answer entries
        answers_label = ctk.CTkLabel(
            self.question_editor_frame,
            text="Answer Options:",
            font=("Helvetica", 16),
            anchor="w"
        )
        answers_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        # Create entries for three answers
        self.answer_entries = []
        self.answer_frames = []
        
        for i in range(3):
            answer_frame = ctk.CTkFrame(self.question_editor_frame)
            answer_frame.pack(pady=5, padx=20, fill="x")
            self.answer_frames.append(answer_frame)
            
            # Radio button for correct answer
            correct_var = ctk.IntVar(value=0)
            self.correct_answer_var = correct_var
            
            radio = ctk.CTkRadioButton(
                answer_frame,
                text="",
                variable=correct_var,
                value=i
            )
            radio.pack(side="left", padx=5)
            
            # Answer text entry
            entry = ctk.CTkEntry(
                answer_frame,
                placeholder_text=f"Answer {i+1}",
                width=400
            )
            entry.pack(side="left", padx=10, fill="x", expand=True)
            self.answer_entries.append(entry)
        
        # Media section - Image
        media_label = ctk.CTkLabel(
            self.question_editor_frame,
            text="Media Files:",
            font=("Helvetica", 16),
            anchor="w"
        )
        media_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Image selection
        image_frame = ctk.CTkFrame(self.question_editor_frame)
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
            self.question_editor_frame,
            width=300,
            height=200
        )
        self.image_preview_frame.pack(pady=10, padx=20)
        self.image_preview_label = ctk.CTkLabel(self.image_preview_frame, text="")
        self.image_preview_label.pack(fill="both", expand=True)
        
        # Audio selection
        audio_frame = ctk.CTkFrame(self.question_editor_frame)
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
        
        # Audio playback controls
        audio_controls = ctk.CTkFrame(self.question_editor_frame)
        audio_controls.pack(pady=10, padx=20)
        
        play_button = ctk.CTkButton(
            audio_controls,
            text="Play",
            command=self.play_audio_preview,
            width=100
        )
        play_button.pack(side="left", padx=10)
        
        stop_button = ctk.CTkButton(
            audio_controls,
            text="Stop",
            command=self.stop_audio,
            width=100
        )
        stop_button.pack(side="left", padx=10)
        
        # Action buttons
        button_frame = ctk.CTkFrame(self.question_editor_frame)
        button_frame.pack(pady=20, fill="x")
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Question",
            command=self.save_question,
            width=150
        )
        save_btn.pack(side="left", padx=10, pady=10)
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="Delete Question",
            command=self.delete_question,
            fg_color="#b22222",  # Dark red
            hover_color="#8b0000",  # Darker red
            width=150
        )
        delete_btn.pack(side="left", padx=10, pady=10)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.back_to_question_selection,
            width=150
        )
        cancel_btn.pack(side="right", padx=10, pady=10)

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
        """Load the selected level and show question selection view"""
        selected_level = self.level_dropdown.get()
        
        # Only proceed if a valid level is selected
        if selected_level != "No levels available":
            success = self.controller.load_level(selected_level)
            
            if success:
                # Update level info label
                self.level_info_label.configure(text=f"Current Level: {selected_level}")
                
                # Load questions for this level
                self.populate_questions_list()
                
                # Switch to question selection view
                self.show_question_selection_view()
            else:
                # Show error message
                print(f"Failed to load level '{selected_level}'")
    
    def populate_questions_list(self):
        """Populate the questions list with buttons for each question"""
        # Clear existing questions
        for widget in self.questions_container.winfo_children():
            widget.destroy()

        # Get questions from controller
        raw_questions = self.controller.get_all_questions()
        
        # Ensure questions are stored as a dictionary with string keys
        questions = {
            str(i + 1): {"id": i + 1, "question": question.replace("\n", " ")}
            for i, question in enumerate(raw_questions)
        }

        if questions:
            # Create a button for each question
            for key, question in questions.items():
                # Create frame for each question
                question_frame = ctk.CTkFrame(self.questions_container)
                question_frame.pack(fill="x", pady=5, padx=5)

                # Get question text
                question_text = question.get("question", f"Question {key}")

                # # Truncate question text if too long
                # if len(question_text) > 50:
                #     question_text = question_text[:47] + "..."

                # Create label with question number and text
                label = ctk.CTkLabel(
                    question_frame,
                    text=f"Q{key}: {question_text}",
                    anchor="w",
                    justify="left"
                )
                label.pack(side="left", padx=10, pady=5, fill="x", expand=True)

                # Create edit button
                edit_btn = ctk.CTkButton(
                    question_frame,
                    text="Edit",
                    command=lambda q=question: self.edit_question(q),
                    width=80
                )
                edit_btn.pack(side="right", padx=10, pady=5)
        else:
            # No questions available
            label = ctk.CTkLabel(
                self.questions_container,
                text="No questions available for this level.",
                font=("Helvetica", 14)
            )
            label.pack(pady=20)


    def edit_question(self, question):
        """Load a question into the editor"""
        # Set question ID
        self.question_id_var.set(question.get("id", ""))
        
        # Set question text
        self.question_entry.delete("0.0", "end")
        self.question_entry.insert("0.0", question.get("question", ""))
        
        # Set answers
        answers = question.get("answers", {})
        for i in range(3):
            answer_key = str(i)
            if answer_key in answers:
                self.answer_entries[i].delete(0, "end")
                self.answer_entries[i].insert(0, answers[answer_key])
            else:
                self.answer_entries[i].delete(0, "end")
        
        # Set correct answer
        correct_answer = question.get("correct_answer", None)
        if correct_answer is not None:
            try:
                self.correct_answer_var.set(int(correct_answer))
            except (ValueError, TypeError):
                self.correct_answer_var.set(0)
        else:
            self.correct_answer_var.set(0)
        
        # Set image
        image_path = question.get("image_file", "")
        self.image_path_var.set(image_path)
        if image_path and os.path.exists(image_path):
            self.display_image_preview(image_path)
            self.image_display.configure(text=os.path.basename(image_path))
        else:
            self.clear_image_preview()
            self.image_display.configure(text="No image selected")
        
        # Set audio
        audio_path = question.get("audio_file", "")
        self.audio_path_var.set(audio_path)
        if audio_path and os.path.exists(audio_path):
            self.audio_display.configure(text=os.path.basename(audio_path))
        else:
            self.audio_display.configure(text="No audio selected")
        
        # Switch to editor view
        self.show_question_editor_view()

    def create_new_question(self):
        """Create a new blank question in the editor"""
        # Reset question ID
        self.question_id_var.set("")
        
        # Clear question text
        self.question_entry.delete("0.0", "end")
        
        # Clear answers
        for entry in self.answer_entries:
            entry.delete(0, "end")
        
        # Reset correct answer
        self.correct_answer_var.set(0)
        
        # Clear image
        self.image_path_var.set("")
        self.clear_image_preview()
        self.image_display.configure(text="No image selected")
        
        # Clear audio
        self.audio_path_var.set("")
        self.audio_display.configure(text="No audio selected")
        
        # Switch to editor view
        self.show_question_editor_view()

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
            print(f"Error loading image: {e}")
            self.clear_image_preview()

    def clear_image_preview(self):
        """Clear the image preview"""
        self.image_preview_label.configure(image=None)
        self.image_preview_label.image = None

    def play_audio_preview(self):
        """Play the selected audio file"""
        audio_path = self.audio_path_var.get()
        if audio_path and os.path.exists(audio_path):
            # Stop any currently playing audio
            self.stop_audio()
            
            # Play the new audio
            try:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"Error playing audio: {e}")

    def stop_audio(self):
        """Stop any currently playing audio"""
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def save_question(self):
        """Save the current question data"""
        # Get question ID (empty for new questions)
        question_id = self.question_id_var.get()
        
        # Get question text
        question_text = self.question_entry.get("0.0", "end-1c").strip()
        if not question_text:
            # Show error message
            print("Question text cannot be empty")
            return
        
        # Get answers
        answers = {}
        empty_answers = 0
        for i, entry in enumerate(self.answer_entries):
            answer_text = entry.get().strip()
            if answer_text:
                answers[str(i)] = answer_text
            else:
                empty_answers += 1
        
        # Ensure we have at least 2 answers
        if len(answers) < 2:
            # Show error message
            print("You must provide at least 2 answer options")
            return
        
        # Get correct answer
        correct_answer = str(self.correct_answer_var.get())
        
        # Ensure correct answer has content
        if correct_answer not in answers:
            # Show error message
            print("You must select a valid answer as correct")
            return
        
        # Create question data
        question_data = {
            "question": question_text,
            "answers": answers,
            "correct_answer": correct_answer,
            "image_file": self.image_path_var.get(),
            "audio_file": self.audio_path_var.get()
        }
        
        # If question ID exists, add it to the data
        if question_id:
            question_data["id"] = question_id
        
        # Save question using controller
        success = self.controller.save_question(question_data)
        
        if success:
            # Return to question selection view and refresh the list
            self.back_to_question_selection()
            self.populate_questions_list()
        else:
            # Show error message
            print("Failed to save question")

    def delete_question(self):
        """Delete the current question"""
        question_id = self.question_id_var.get()
        
        # Only try to delete if we have a question ID
        if question_id:
            # Get confirmation (simplified for this example)
            from tkinter import messagebox
            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete this question?"
            )
            
            if confirm:
                # Delete question using controller
                success = self.controller.delete_question(question_id)
                
                if success:
                    # Return to question selection view and refresh the list
                    self.back_to_question_selection()
                    self.populate_questions_list()
                else:
                    # Show error message
                    print("Failed to delete question")
        else:
            # New questions don't need to be deleted
            self.back_to_question_selection()

    def show_question_selection_view(self):
        """Show the question selection view"""
        # Hide other frames
        self.level_selection_frame.pack_forget()
        if hasattr(self, 'question_editor_frame'):
            self.question_editor_frame.pack_forget()
        
        # Show question selection frame
        self.question_selection_frame.pack(fill="both", expand=True)

    def show_question_editor_view(self):
        """Show the question editor view"""
        # Hide other frames
        self.level_selection_frame.pack_forget()
        self.question_selection_frame.pack_forget()
        
        # Show question editor frame
        self.question_editor_frame.pack(fill="both", expand=True)

    def back_to_level_selection(self):
        """Go back to level selection view"""
        # Stop any playing audio
        self.stop_audio()
        
        # Hide current frame
        self.question_selection_frame.pack_forget()
        
        # Show level selection frame
        self.level_selection_frame.pack(fill="both", expand=True)

    def back_to_question_selection(self):
        """Go back to question selection view"""
        # Stop any playing audio
        self.stop_audio()
        
        # Hide current frame
        self.question_editor_frame.pack_forget()
        
        # Show question selection frame
        self.question_selection_frame.pack(fill="both", expand=True)

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