# view/modify_levels_view.py
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
        # Main container for level selection UI - now using scrollable frame
        self.level_selection_frame = ctk.CTkFrame(self)
        self.level_selection_frame.pack(fill="both", expand=True)
        
        # Add a scrollable frame inside the main frame
        self.level_selection_scrollable = ctk.CTkScrollableFrame(self.level_selection_frame)
        self.level_selection_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Main title
        title = ctk.CTkLabel(
            self.level_selection_scrollable, 
            text="Modify Questions", 
            font=("Helvetica", 24)
        )
        title.pack(pady=30)

        # Create the dropdown for level selection
        level_label = ctk.CTkLabel(
            self.level_selection_scrollable,
            text="Select a Level to Modify:",
            font=("Helvetica", 16)
        )
        level_label.pack(pady=(20, 5))
        
        self.level_dropdown = ctk.CTkOptionMenu(
            self.level_selection_scrollable,
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
                self.level_selection_scrollable,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10)

    def create_question_selection_view(self):
        """Initialize the question selection frame and its components"""
        # Main container for question selection UI
        self.question_selection_frame = ctk.CTkFrame(self)
        
        # Add a scrollable frame inside the main frame
        self.question_selection_scrollable = ctk.CTkScrollableFrame(self.question_selection_frame)
        self.question_selection_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = ctk.CTkLabel(
            self.question_selection_scrollable, 
            text="Select a Question to Modify", 
            font=("Helvetica", 24)
        )
        header.pack(pady=20)
        
        # Level info label
        self.level_info_label = ctk.CTkLabel(
            self.question_selection_scrollable,
            text="Current Level: None",
            font=("Helvetica", 16)
        )
        self.level_info_label.pack(pady=10)
        
        # Create a scrollable frame for questions
        self.questions_container = ctk.CTkScrollableFrame(
            self.question_selection_scrollable,
            width=500,
            height=300
        )
        self.questions_container.pack(pady=20, fill="both", expand=True)
        
        # Container for the action buttons
        button_frame = ctk.CTkFrame(self.question_selection_scrollable)
        button_frame.pack(pady=20, fill="x")

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
        
        # Add a scrollable frame inside the main frame
        self.question_editor_scrollable = ctk.CTkScrollableFrame(self.question_editor_frame)
        self.question_editor_scrollable.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header = ctk.CTkLabel(
            self.question_editor_scrollable, 
            text="Edit Question", 
            font=("Helvetica", 24)
        )
        header.pack(pady=20)
        
        # Question ID display (hidden, for tracking)
        self.question_id_var = ctk.StringVar(value="")
        
        # Question text entry
        question_label = ctk.CTkLabel(
            self.question_editor_scrollable,
            text="Question Text:",
            font=("Helvetica", 16),
            anchor="w"
        )
        question_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.question_entry = ctk.CTkTextbox(
            self.question_editor_scrollable,
            height=100,
            width=500
        )
        self.question_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        # Answer entries
        answers_label = ctk.CTkLabel(
            self.question_editor_scrollable,
            text="Answer Options:",
            font=("Helvetica", 16),
            anchor="w"
        )
        answers_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        # Create entries for three answers
        self.answer_entries = []
        self.answer_frames = []
        
        for i in range(3):
            answer_frame = ctk.CTkFrame(self.question_editor_scrollable)
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
        correct_answer_frame = ctk.CTkFrame(self.question_editor_scrollable)
        correct_answer_frame.pack(pady=10, padx=20, fill="x")
        
        correct_answer_label = ctk.CTkLabel(
            correct_answer_frame,
            text="Correct Answer:",
            font=("Helvetica", 14),
            anchor="w"
        )
        correct_answer_label.pack(side="left", padx=5)
        
        # Create string variable for dropdown
        self.correct_answer_var = ctk.StringVar(value="0")
        
        # Create the dropdown for correct answer selection
        self.correct_answer_dropdown = ctk.CTkOptionMenu(
            correct_answer_frame,
            values=["Answer 1", "Answer 2", "Answer 3"],
            variable=self.correct_answer_var
        )
        self.correct_answer_dropdown.pack(side="left", padx=10)
        
        # Media section - Image
        media_label = ctk.CTkLabel(
            self.question_editor_scrollable,
            text="Media Files:",
            font=("Helvetica", 16),
            anchor="w"
        )
        media_label.pack(pady=(20, 5), padx=20, anchor="w")
        
        # Image selection
        image_frame = ctk.CTkFrame(self.question_editor_scrollable)
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
            self.question_editor_scrollable,
            width=300,
            height=200
        )
        self.image_preview_frame.pack(pady=10, padx=20)
        self.image_preview_label = ctk.CTkLabel(self.image_preview_frame, text="")
        self.image_preview_label.pack(fill="both", expand=True)
        
        # Audio selection
        audio_frame = ctk.CTkFrame(self.question_editor_scrollable)
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
        button_frame = ctk.CTkFrame(self.question_editor_scrollable)
        button_frame.pack(pady=20, fill="x")
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save Question",
            command=self.save_question,
            width=150
        )
        save_btn.pack(side="left", padx=10, pady=10)

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

    # def update_answer_dropdown_values(self):
    #     """Update dropdown values based on current answer entries"""
    #     answer_texts = []
    #     for i, entry in enumerate(self.answer_entries):
    #         text = entry.get().strip()
    #         if text:
    #             answer_texts.append(f"Answer {i+1}: {text[:20]}...")
    #         else:
    #             answer_texts.append(f"Answer {i+1}: (empty)")
        
    #     # Update dropdown values
    #     if answer_texts:
    #         self.correct_answer_dropdown.configure(values=answer_texts)
    
    # def get_selected_answer_index(self):
    #     """Get the index of the selected answer from the dropdown"""
    #     current_value = self.correct_answer_var.get()
    #     print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + current_value)
    #     # Extract the answer number from the dropdown text (e.g., "Answer 2: text..." -> 1)
    #     if current_value.startswith("Answer "):
    #         try:
    #             index = int(current_value.split(":")[0].replace("Answer ", "")) - 1
    #             return str(index)
    #         except (ValueError, IndexError):
    #             return "0"
    #     return "0"  # Default to first answer if parsing fails

    def edit_question(self, question):
        """Load a question into the editor"""
        # Set question ID
        self.question_id_var.set(question.get("id", ""))

        # Set question text - display literal \n as is
        self.question_entry.delete("0.0", "end")
        question_text = question.get("question", "")
        self.question_entry.insert("0.0", question_text)

        # Set answers - display literal \n as is
        answers_dict = self.controller.get_question_answers(question.get("id", ""))
        print("Answers:", answers_dict)

        # Convert dictionary values to list, ensuring keys are correctly mapped
        answers_list = [answers_dict[str(i)] for i in range(len(answers_dict)) if str(i) in answers_dict]

        for i in range(3):
            if i < len(answers_list):
                self.answer_entries[i].delete(0, "end")
                self.answer_entries[i].insert(0, answers_list[i])
            else:
                self.answer_entries[i].delete(0, "end")

        # Update the dropdown with current answers
        answer_texts = []
        for i, entry in enumerate(self.answer_entries):
            text = entry.get().strip()
            if text:
                # Show abbreviated text in dropdown
                display_text = text if len(text) <= 20 else f"{text[:20]}..."
                answer_texts.append(f"Answer {i+1}: {display_text}")
            else:
                answer_texts.append(f"Answer {i+1}: (empty)")

        self.correct_answer_dropdown.configure(values=answer_texts)

        # Set correct answer in dropdown
        correct_answer = self.controller.get_correct_answer_index(question.get("id", ""))
        # print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        # print(question)
        # print("Correct answer:", correct_answer)
        try:
            correct_index = int(correct_answer)
            # Select the corresponding item in dropdown
            if 0 <= correct_index < len(answer_texts):
                self.correct_answer_dropdown.set(answer_texts[correct_index])
            else:
                self.correct_answer_dropdown.set(answer_texts[0])
        except (ValueError, TypeError):
            self.correct_answer_dropdown.set(answer_texts[0])

        # Set image
        image_path = self.controller.get_image_path(question.get("id", ""))
        self.image_path_var.set(image_path)
        if image_path and os.path.exists(image_path):
            self.display_image_preview(image_path)
            self.image_display.configure(text=os.path.basename(image_path))
        else:
            self.clear_image_preview()
            self.image_display.configure(text="No image selected")

        # Set audio
        audio_path = self.controller.get_audio_path(question.get("id", ""))
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
        
        # Reset dropdown options
        default_options = ["Answer 1: (empty)", "Answer 2: (empty)", "Answer 3: (empty)"]
        self.correct_answer_dropdown.configure(values=default_options)
        self.correct_answer_dropdown.set(default_options[0])
        
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
    
    def get_correct_answer_index(self):
        """Extract the index of the selected correct answer from dropdown"""
        selected_option = self.correct_answer_dropdown.get()
        try:
            # Extract number from "Answer X: text"
            answer_num = int(selected_option.split(":")[0].replace("Answer ", ""))
            return str(answer_num - 1)  # Convert to 0-based index as string
        except (ValueError, IndexError):
            return "0"  # Default to first answer

    def save_question(self):
        """Save the current question data"""
        # Get question ID (empty for new questions)
        question_id = self.question_id_var.get()
        
        question_text = self.question_entry.get("0.0", "end-1c").strip()

        if not question_text:
            print("Question text cannot be empty")
            return
        
        answers = {}
        empty_answers = 0
        for i, entry in enumerate(self.answer_entries):
            answer_text = entry.get().strip()
            if answer_text:
                answers[str(i)] = answer_text
            else:
                empty_answers += 1
        
        # Ensure we have all answers filled
        if len(answers) < 3:
            print("You must provide all answer options")
            return
        
        # Get correct answer from dropdown
        correct_answer = self.get_correct_answer_index()
        
        # Ensure correct answer has content
        if correct_answer not in answers:
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
            # cast question_id to int
            question_id = int(question_id)
            question_data["id"] = question_id

        print("##################################")
        print("Question data:", question_data)
        
        # Save question using controller
        success = self.controller.save_question(question_data)
        
        if success:
            self.back_to_question_selection()
            self.populate_questions_list()
        else:
            print("Failed to save question")

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
        # Hide current frame
        self.question_selection_frame.pack_forget()
        
        # Show level selection frame
        self.level_selection_frame.pack(fill="both", expand=True)

    def back_to_question_selection(self):
        """Go back to question selection view"""
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