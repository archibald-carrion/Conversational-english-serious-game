import customtkinter as ctk
from PIL import Image

class FrameInitializer:
    def __init__(self, app):
        self.app = app

    def initialize_main_menu_frame(self):
        """Initialize the main menu frame and its components"""
        self.app.main_menu_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        self.app.main_menu_frame.pack(pady=50, padx=100, fill="both", expand=True, anchor="w")

        # Main menu title
        self.app.menu_title = ctk.CTkLabel(
            self.app.main_menu_frame, 
            text="Level Manager", 
            font=("Helvetica", 24)
        )
        self.app.menu_title.pack(pady=50)

        # Create buttons
        buttons = [
            ("Load Level", self.app.open_load_level_window),
            ("Modify Levels", self.app.open_modify_levels_window),
            ("Create New Level", self.app.create_new_level),
            ("Game Configuration", self.app.open_game_configuration_window),
            ("Quit Game", self.app.root.quit)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.app.main_menu_frame,
                text=text,
                command=command
            )
            btn.pack(pady=10)

    def initialize_load_level_frame(self):
        """Initialize the load level frame and its components"""
        self.app.load_level_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")

        self.app.level_dropdown = ctk.CTkOptionMenu(
            self.app.load_level_frame,
            values=self.app.levels_manager.get_level_names()
        )
        self.app.level_dropdown.pack(pady=20)

        buttons = [
            ("Load Selected Level", self.app.load_selected_level),
            ("Back to Menu", self.app.back_to_main_menu)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.app.load_level_frame,
                text=text,
                command=command
            )
            btn.pack(pady=10)

    def initialize_game_configuration_frame(self):
        """Initialize the game configuration frame and its components"""
        self.app.game_configuration_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")

        self.app.game_title = ctk.CTkLabel(
            self.app.game_configuration_frame,
            text="Game Configuration",
            font=("Helvetica", 24)
        )

        self.app.window_size_dropdown = ctk.CTkOptionMenu(
            self.app.game_configuration_frame,
            values=["800x600", "1280x720", "1920x1080"],
            command=self.app.update_window_size
        )
        self.app.window_size_dropdown.pack(pady=20)

        buttons = [
            ("Confirm Window Size", self.app.apply_window_size),
            ("Back to Menu", self.app.back_to_main_menu)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.app.game_configuration_frame,
                text=text,
                command=command
            )
            btn.pack(pady=10)

    def initialize_level_frame(self):
        """Initialize the level frame and its components"""
        self.app.level_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")

        # Level Title
        self.app.level_title = ctk.CTkLabel(
            self.app.level_frame,
            text="",
            font=("Helvetica", 24)
        )
        self.app.level_title.pack(pady=20)

        # Question Text
        self.app.question_text = ctk.CTkLabel(
            self.app.level_frame,
            text="",
            wraplength=600,
            font=("Helvetica", 18)
        )
        self.app.question_text.pack(pady=20)

        # Answer Buttons
        self.app.answer_buttons = []
        for i in range(3):
            button = ctk.CTkButton(
                self.app.level_frame,
                text="",
                command=lambda index=i: self.app.handle_answer_click(index),
                width=400,
                height=50
            )
            self.app.answer_buttons.append(button)
            button.pack(pady=10)

        # Score Display
        self.app.score_display = ctk.CTkLabel(
            self.app.level_frame,
            text=f"Score: {self.app.current_score}",
            font=("Helvetica", 16),
            text_color="white"
        )
        self.app.score_display.place(relx=0.95, rely=0.05, anchor="ne")

        # Audio and Back buttons
        buttons = [
            ("🔊 Replay Audio", self.app.replay_audio, 200, 40),
            ("Back to Menu", self.app.back_to_main_menu, 200, 40)
        ]

        for text, command, width, height in buttons:
            btn = ctk.CTkButton(
                self.app.level_frame,
                text=text,
                command=command,
                width=width,
                height=height
            )
            btn.pack(pady=10)

    def initialize_level_completed_frame(self):
        """Initialize the level completed frame and its components"""
        self.app.level_completed_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")

        # Completion Message
        self.app.completion_message = ctk.CTkLabel(
            self.app.level_completed_frame,
            text="Level Completed!",
            font=("Helvetica", 24),
            text_color="green"
        )
        self.app.completion_message.pack(pady=20)

        # Score Display
        self.app.score_label = ctk.CTkLabel(
            self.app.level_completed_frame,
            text="Your Score: 0",
            font=("Helvetica", 20)
        )
        self.app.score_label.pack(pady=10)

        # Button to return to the main menu
        self.app.return_to_menu_btn = ctk.CTkButton(
            self.app.level_completed_frame,
            text="Return to Main Menu",
            command=self.app.back_to_main_menu
        )
        self.app.return_to_menu_btn.pack(pady=20)

    def initialize_modify_levels_frame(self):
        """Initialize the modify levels frame and its components"""
        self.app.modify_levels_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")

        self.app.modify_level_dropdown = ctk.CTkOptionMenu(
            self.app.modify_levels_frame,
            values=self.app.levels_manager.get_level_names()
        )
        self.app.modify_level_dropdown.pack(pady=20)

        buttons = [
            ("Select Level", self.app.open_question_selection),
            ("Back to Menu", self.app.back_to_main_menu)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.app.modify_levels_frame,
                text=text,
                command=command
            )
            btn.pack(pady=10)

    def initialize_question_selection_frame(self):
        """Initialize the question selection frame and its components"""
        self.app.question_selection_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")

        self.app.question_dropdown = ctk.CTkOptionMenu(
            self.app.question_selection_frame,
            values=[""]
        )
        self.app.question_dropdown.pack(pady=20)

        buttons = [
            ("Modify Selected Question", self.app.open_question_editor),
            ("Back to Level Selection", self.app.back_to_modify_levels)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.app.question_selection_frame,
                text=text,
                command=command
            )
            btn.pack(pady=10)

    def initialize_question_editor_frame(self):
        """Initialize the question editor frame and its components"""
        self.app.question_editor_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        
        # Create scrollable canvas
        self.app.editor_canvas = ctk.CTkCanvas(
            self.app.question_editor_frame,
            width=700,
            height=500,
            bg='#2b2b2b',
            highlightthickness=0
        )
        self.app.editor_scrollbar = ctk.CTkScrollbar(
            self.app.question_editor_frame,
            orientation="vertical",
            command=self.app.editor_canvas.yview
        )
        self.app.editor_canvas.configure(yscrollcommand=self.app.editor_scrollbar.set)

        # Create content frame
        self.app.editor_content_frame = ctk.CTkFrame(self.app.editor_canvas, fg_color="transparent")
        
        # Setup canvas and scrollbar
        self.app.editor_scrollbar.pack(side="right", fill="y")
        self.app.editor_canvas.pack(side="left", fill="both", expand=True, padx=5)
        
        self.app.canvas_frame = self.app.editor_canvas.create_window(
            (0, 0),
            window=self.app.editor_content_frame,
            anchor="nw",
            width=680
        )

        # Add question entry
        self.app.question_label = ctk.CTkLabel(self.app.editor_content_frame, text="Question:")
        self.app.question_label.pack(pady=3)
        
        self.app.question_entry = ctk.CTkTextbox(
            self.app.editor_content_frame,
            height=80,
            width=600
        )
        self.app.question_entry.pack(pady=5)

        # Add answer entries
        self.app.answer_entries = []
        for i in range(3):
            label = ctk.CTkLabel(
                self.app.editor_content_frame,
                text=f"Answer {i+1}:"
            )
            label.pack(pady=2)
            
            entry = ctk.CTkEntry(
                self.app.editor_content_frame,
                width=500
            )
            entry.pack(pady=3)
            self.app.answer_entries.append(entry)

        # Add correct answer entry
        self.app.correct_answer_label = ctk.CTkLabel(
            self.app.editor_content_frame,
            text="Correct Answer (0-2):"
        )
        self.app.correct_answer_label.pack(pady=2)
        
        self.app.correct_answer_entry = ctk.CTkEntry(
            self.app.editor_content_frame,
            width=50
        )
        self.app.correct_answer_entry.pack(pady=3)

        # Add audio selection
        self.app.audio_path_label = ctk.CTkLabel(
            self.app.editor_content_frame,
            text="Current Audio File: None",
            wraplength=500
        )
        self.app.audio_path_label.pack(pady=2)

        buttons = [
            ("Select Audio File", self.app.select_audio_file),
            ("Save Changes", self.app.save_question_changes),
            ("Back to Question Selection", self.app.back_to_question_selection)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self.app.editor_content_frame,
                text=text,
                command=command
            )
            btn.pack(pady=3)

        # Bind events
        self.app.editor_content_frame.bind("<Configure>", self.app.update_scrollregion)
        self.app.editor_canvas.bind("<Configure>", self.app.update_canvas_width)
        self.app.editor_canvas.bind_all("<MouseWheel>", self.app.on_mousewheel)

    def initialize_level_creator_frames(self):
        """Initialize frames for creating new levels"""
        
        ''' Level Name Frame '''
        self.app.level_name_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        
        # Title
        self.app.new_level_title = ctk.CTkLabel(
            self.app.level_name_frame,
            text="Create New Level",
            font=("Helvetica", 24)
        )
        self.app.new_level_title.pack(pady=20)
        
        # Level name entry
        self.app.level_name_label = ctk.CTkLabel(
            self.app.level_name_frame,
            text="Enter Level Name:"
        )
        self.app.level_name_label.pack(pady=5)
        
        self.app.level_name_entry = ctk.CTkEntry(
            self.app.level_name_frame,
            width=300
        )
        self.app.level_name_entry.pack(pady=10)
        
        # Error message label (initially hidden)
        self.app.name_error_label = ctk.CTkLabel(
            self.app.level_name_frame,
            text="",
            text_color="red"
        )
        self.app.name_error_label.pack(pady=5)
        self.app.name_error_label.pack_forget()  # Hide initially
        
        # Continue button
        self.app.continue_to_questions_btn = ctk.CTkButton(
            self.app.level_name_frame,
            text="Continue to Questions",
            command=self.app.start_question_creation
        )
        self.app.continue_to_questions_btn.pack(pady=10)
        
        # Back button
        self.app.name_back_btn = ctk.CTkButton(
            self.app.level_name_frame,
            text="Back to Menu",
            command=self.app.back_to_main_menu
        )
        self.app.name_back_btn.pack(pady=10)

        ''' Question Creation Frame '''
        self.app.question_creation_frame = ctk.CTkFrame(self.app.root, fg_color="transparent")
        
        # Create a canvas with scrollbar for question creation
        self.app.creation_canvas = ctk.CTkCanvas(
            self.app.question_creation_frame,
            width=700,
            height=500,
            bg='#2b2b2b',
            highlightthickness=0
        )
        self.app.creation_scrollbar = ctk.CTkScrollbar(
            self.app.question_creation_frame,
            orientation="vertical",
            command=self.app.creation_canvas.yview
        )
        self.app.creation_canvas.configure(yscrollcommand=self.app.creation_scrollbar.set)
        
        # Create a frame inside canvas for content
        self.app.creation_content_frame = ctk.CTkFrame(self.app.creation_canvas, fg_color="#2b2b2b")
        
        # Pack scrollbar and canvas
        self.app.creation_scrollbar.pack(side="right", fill="y")
        self.app.creation_canvas.pack(side="left", fill="both", expand=True, padx=5)
        
        # Create window in canvas
        self.app.creation_window = self.app.creation_canvas.create_window(
            (0, 0),
            window=self.app.creation_content_frame,
            anchor="nw",
            width=680
        )
        
        # Progress indicator
        self.app.question_progress = ctk.CTkLabel(
            self.app.creation_content_frame,
            text="Question 1/10",
            font=("Helvetica", 18)
        )
        self.app.question_progress.pack(pady=10)
        
        # Question text entry
        self.app.new_question_label = ctk.CTkLabel(
            self.app.creation_content_frame,
            text="Question:"
        )
        self.app.new_question_label.pack(pady=3)
        
        self.app.new_question_entry = ctk.CTkTextbox(
            self.app.creation_content_frame,
            height=80,
            width=600
        )
        self.app.new_question_entry.pack(pady=5)
        
        # Answer entries
        self.app.new_answer_entries = []
        for i in range(3):
            label = ctk.CTkLabel(
                self.app.creation_content_frame,
                text=f"Answer {i+1}:"
            )
            label.pack(pady=2)
            
            entry = ctk.CTkEntry(
                self.app.creation_content_frame,
                width=500
            )
            entry.pack(pady=3)
            self.app.new_answer_entries.append(entry)
        
        # Correct answer selection
        self.app.new_correct_answer_label = ctk.CTkLabel(
            self.app.creation_content_frame,
            text="Correct Answer (0-2):"
        )
        self.app.new_correct_answer_label.pack(pady=2)
        
        self.app.new_correct_answer_entry = ctk.CTkEntry(
            self.app.creation_content_frame,
            width=50
        )
        self.app.new_correct_answer_entry.pack(pady=3)
        
        # Error message for validation
        self.app.creation_error_label = ctk.CTkLabel(
            self.app.creation_content_frame,
            text="",
            text_color="red"
        )
        self.app.creation_error_label.pack(pady=5)
        self.app.creation_error_label.pack_forget()  # Hide initially
        
        # Audio file selection
        self.app.new_audio_path_label = ctk.CTkLabel(
            self.app.creation_content_frame,
            text="Current Audio File: None",
            wraplength=500
        )
        self.app.new_audio_path_label.pack(pady=2)
        
        self.app.new_select_audio_btn = ctk.CTkButton(
            self.app.creation_content_frame,
            text="Select Audio File",
            command=self.app.select_new_audio_file
        )
        self.app.new_select_audio_btn.pack(pady=3)
        
        # Navigation buttons
        self.app.button_frame = ctk.CTkFrame(
            self.app.creation_content_frame,
            fg_color="transparent"
        )
        self.app.button_frame.pack(pady=10, expand=True, anchor="center")
        
        self.app.prev_question_btn = ctk.CTkButton(
            self.app.button_frame,
            text="Previous Question",
            command=self.app.prev_question,
            state="disabled"  # Initially disabled
        )
        self.app.prev_question_btn.pack(side="left", padx=5)
        
        self.app.next_question_btn = ctk.CTkButton(
            self.app.button_frame,
            text="Next Question",
            command=self.app.next_question
        )
        self.app.next_question_btn.pack(side="left", padx=5)
        
        # Create a frame for save button to help with centering
        self.app.save_button_frame = ctk.CTkFrame(
            self.app.creation_content_frame, 
            fg_color="transparent"
        )
        self.app.save_button_frame.pack(pady=10, expand=True, anchor="center")

        # Save level button (initially hidden)
        self.app.save_level_btn = ctk.CTkButton(
            self.app.save_button_frame,
            text="Save Level",
            command=self.app.save_new_level
        )
        self.app.save_level_btn.pack(anchor="center")
        
        # Back button
        self.app.creation_back_btn = ctk.CTkButton(
            self.app.creation_content_frame,
            text="Back to Level Name",
            command=self.app.back_to_level_name
        )
        self.app.creation_back_btn.pack(pady=10)
        
        # Bind canvas configuration
        self.app.creation_content_frame.bind("<Configure>", self.app.update_creation_scrollregion)
        self.app.creation_canvas.bind("<Configure>", self.app.update_creation_canvas_width)
        self.app.root.bind("<MouseWheel>", self.app.on_creation_mousewheel)