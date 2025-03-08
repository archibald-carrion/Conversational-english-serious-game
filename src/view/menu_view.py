# view/menu_view.py
import customtkinter as ctk

class MenuView(ctk.CTkFrame):
    def __init__(self, parent, controller, switch_view_callback=None, 
                 create_levels_view=None, modify_levels_view=None, 
                 play_levels_view=None, config_menu_view=None):
        super().__init__(parent)
        
        self.controller = controller
        self.switch_view_callback = switch_view_callback
        self.parent = parent
        
        # Store the other views for navigation
        self.create_levels_view = create_levels_view
        self.modify_levels_view = modify_levels_view
        self.play_levels_view = play_levels_view
        self.config_menu_view = config_menu_view
        
        # Create the main menu
        self.create_menu()
    
    def create_menu(self):
        """Initialize the main menu frame and its components"""
        # Main menu title
        menu_title = ctk.CTkLabel(
            self, 
            text="Level Manager", 
            font=("Helvetica", 24)
        )
        menu_title.pack(pady=50)

        # Create buttons
        buttons = [
            ("Load Level", self.open_load_level_window),
            ("Modify Levels", self.open_modify_levels_window),
            ("Create New Level", self.create_new_level),
            ("Game Configuration", self.open_game_configuration_window),
            ("Quit Game", self.quit_game)
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                self,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10)

    def open_load_level_window(self):
        """Open the load level window (play levels)"""
        if self.play_levels_view and self.switch_view_callback:
            # Update the level dropdown before showing if needed
            if hasattr(self.play_levels_view, 'update_level_dropdown'):
                self.play_levels_view.update_level_dropdown()
            self.switch_view_callback(self.parent, self.play_levels_view)

    def open_modify_levels_window(self):
        """Open the modify levels window"""
        if self.modify_levels_view and self.switch_view_callback:
            self.switch_view_callback(self.parent, self.modify_levels_view)

    def create_new_level(self):
        """Open the level creation window"""
        if self.create_levels_view and self.switch_view_callback:
            # Reset entry and error message if needed
            if hasattr(self.create_levels_view, 'level_name_entry'):
                self.create_levels_view.level_name_entry.delete(0, "end")
            if hasattr(self.create_levels_view, 'name_error_label'):
                self.create_levels_view.name_error_label.configure(text="")
                
            self.switch_view_callback(self.parent, self.create_levels_view)

    def open_game_configuration_window(self):
        """Open the game configuration window"""
        if self.config_menu_view and self.switch_view_callback:
            self.switch_view_callback(self.parent, self.config_menu_view)
    
    def quit_game(self):
        """Quit the application"""
        self.controller.quit_application()