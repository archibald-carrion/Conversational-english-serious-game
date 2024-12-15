import customtkinter as ctk
from levels_manager import LevelsManager
from PIL import Image

class App:
    def __init__(self):

        self.levels_manager = LevelsManager('levels.json')


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
            text="Load Selected Level"
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

        # Level Title, it's the name of the selected level from the dropdown

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

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = App()
    app.run()