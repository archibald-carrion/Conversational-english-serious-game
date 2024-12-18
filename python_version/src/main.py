import customtkinter as ctk
from levels_manager import LevelsManager
from PIL import Image
import os
import threading
from playsound import playsound

class App:
    def __init__(self):

        self.levels_manager = LevelsManager('levels.json')

        self.current_level = None

        # Configure the main window
        self.root = ctk.CTk()
        self.root.title("Level Selector")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        # self.root.attributes('-transparentcolor', '#000001')  # Specify a color to make transparent
        # self.root.configure(bg='#000001')  # Match this color with the transparency attribute
        self.root.bind("<Escape>", lambda e: self.root.quit())

        # Set appearance and color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Set the background image - UPDATED PLACEMENT
        self.bg_image = ctk.CTkImage(
            light_image=Image.open("assets/images/background.png"), 
            dark_image=Image.open("assets/images/background.png"),
            size=(800, 600)  # Explicitly set size to match window
        )
        self.my_background = ctk.CTkLabel(self.root, text="", image=self.bg_image)
        self.my_background.place(x=0, y=0, relwidth=1, relheight=1)  # Ensure full coverage


        ''' Main Menu '''
        
        # Create main menu frame
        self.main_menu_frame = ctk.CTkFrame(self.root, fg_color="transparent", bg_color="transparent")
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

        # Modify Levels Button
        self.modify_levels_btn = ctk.CTkButton(
            self.main_menu_frame, 
            text="Modify Levels"
        )
        self.modify_levels_btn.pack(pady=10)

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
        self.my_background.configure(image=self.bg_image)
        
        # Ensure background covers the entire window
        self.my_background.place(x=0, y=0, relwidth=1, relheight=1)

    def update_window_size(self, size):
        """Update the selected window size when the dropdown changes."""
        self.selected_window_size = size

    def load_level(self, level_name, question_index):
        """
        Load and display a specific question for a given level with parallel audio playback.
        
        Args:
            level_name (str): Name of the level
            question_index (int): Index of the question to load
        """
        # Hide other frames
        self.main_menu_frame.pack_forget()
        self.game_configuration_frame.pack_forget()
        self.load_level_frame.pack_forget()

        # Show the level frame
        self.level_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Get the question data
        question_data = self.levels_manager.get_level_question(level_name, question_index)
        if question_data:
            # Update the level title
            self.level_title.configure(text=f"Level {level_name}")

            # Update the question text
            self.question_text.configure(text=question_data["question"])

            # Update the answer buttons
            for i, answer_text in enumerate(question_data["answers"]):
                self.answer_buttons[i].configure(text=answer_text)

            # Play the audio file in a separate thread
            audio_file = question_data["audio_file"]
            if os.path.exists(audio_file):
                def play_audio():
                    playsound(audio_file)
                
                # Create and start the audio thread
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.daemon = True  # Ensure the thread doesn't block app closing
                audio_thread.start()
            else:
                print(f"Error: Audio file not found at {audio_file}")
        else:
            print(f"Error: Question not found for level {level_name} at index {question_index}")

    def handle_answer_click(self, answer_index):
        """
        Handle the user's answer selection with progression to next question.
        
        Args:
            answer_index (int): Index of the selected answer
        """
        # Ensure a level is currently loaded
        if not self.current_level:
            print("No level currently loaded")
            return

        # Track the current question index (add this as an instance variable)
        if not hasattr(self, 'current_question_index'):
            self.current_question_index = 0

        # Get the current question data
        question_data = self.levels_manager.get_level_question(
            self.current_level, 
            self.current_question_index
        )
        
        # Create a feedback label if it doesn't exist
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
            # Correct answer
            self.feedback_label.configure(
                text="Congratulations! ✅", 
                text_color="green"
            )
            
            # Try to load the next question
            next_question_index = self.current_question_index + 1
            next_question = self.levels_manager.get_level_question(
                self.current_level, 
                next_question_index
            )
            
            if next_question:
                # Increment the question index
                self.current_question_index = next_question_index
                
                # Delay and then load the next question
                self.root.after(2000, lambda: self.load_level(self.current_level, next_question_index))
            else:
                # No more questions in this level
                self.feedback_label.configure(
                    text="Congratulations! Level Completed! 🎉", 
                    text_color="green"
                )
                # Optionally return to main menu after a delay
                self.root.after(3000, self.back_to_main_menu)
        else:
            # Incorrect answer
            self.feedback_label.configure(
                text="Try Again! ❌", 
                text_color="red"
            )

        # Clear the feedback after 2 seconds if not progressing
        self.root.after(2000, self.clear_feedback)

    def clear_feedback(self):
        """
        Clear the feedback label text.
        """
        if hasattr(self, 'feedback_label'):
            self.feedback_label.configure(text="")

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = App()
    app.run()