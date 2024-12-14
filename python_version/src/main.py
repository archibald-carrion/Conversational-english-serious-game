import customtkinter as ctk

class LevelSelectorApp:
    def __init__(self):
        # Configure the main window
        self.root = ctk.CTk()
        self.root.title("Level Selector")
        self.root.geometry("400x300")

        # Set appearance and color theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Create main menu frame
        self.main_menu_frame = ctk.CTkFrame(self.root)
        self.main_menu_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Main menu title
        self.menu_title = ctk.CTkLabel(
            self.main_menu_frame, 
            text="Level Manager", 
            font=("Helvetica", 24)
        )
        self.menu_title.pack(pady=20)

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

        # Quit Button
        self.quit_btn = ctk.CTkButton(
            self.main_menu_frame, 
            text="Quit Game", 
            command=self.root.quit
        )
        self.quit_btn.pack(pady=10)

        # Load Level Frame (initially hidden)
        self.load_level_frame = ctk.CTkFrame(self.root)

        # Level Dropdown
        self.level_dropdown = ctk.CTkOptionMenu(
            self.load_level_frame, 
            values=["Level 1", "Level 2", "Level 3"]
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

    def open_load_level_window(self):
        # Hide main menu
        self.main_menu_frame.pack_forget()
        
        # Show load level frame
        self.load_level_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def back_to_main_menu(self):
        # Hide load level frame
        self.load_level_frame.pack_forget()
        
        # Show main menu
        self.main_menu_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def run(self):
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = LevelSelectorApp()
    app.run()