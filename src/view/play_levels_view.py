# view/play_levels_view.py
import customtkinter as ctk

class PlayLevelsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.parent = parent
        
        # Create the play levels UI
        self.create_play_levels_view()

    def create_play_levels_view(self):
        """Initialize the play levels frame and its components"""
        # Main title
        title = ctk.CTkLabel(
            self, 
            text="Load Level", 
            font=("Helvetica", 24)
        )
        title.pack(pady=30)

        # Create the dropdown for level selection
        self.level_dropdown = ctk.CTkOptionMenu(
            self,
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
                self,
                text=text,
                command=command,
                width=200
            )
            btn.pack(pady=10)

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
        """Call controller to load the selected level"""
        selected_level = self.level_dropdown.get()
        
        # Only proceed if a valid level is selected
        if selected_level != "No levels available":
            success = self.controller.load_level(selected_level)
            
            if success:
                # You might want to show a success message or navigate to the game view
                print(f"Level '{selected_level}' loaded successfully")
            else:
                # Show error message
                print(f"Failed to load level '{selected_level}'")

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