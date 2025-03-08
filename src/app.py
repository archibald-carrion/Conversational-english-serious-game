# main.py
import customtkinter as ctk  
from controllers.create_levels_controller import CreateLevelsController
from controllers.modify_levels_controller import ModifyLevelsController
from controllers.play_levels_controller import PlayLevelsController
from controllers.delete_levels_controller import DeleteLevelsController
from controllers.menu_controller import MenuController
from controllers.config_menu_controller import ConfigMenuController  

from models.create_levels_model import CreateLevelsModel
from models.modify_levels_model import ModifyLevelsModel
from models.play_levels_model import PlayLevelsModel
from models.delete_levels_model import DeleteLevelsModel
from models.menu_model import MenuModel
from models.config_menu_model import ConfigMenuModel  

from view.create_levels_view import CreateLevelsView
from view.modify_levels_view import ModifyLevelsView
from view.play_levels_view import PlayLevelsView
from view.delete_levels_view import DeleteLevelsView
from view.menu_view import MenuView
from view.config_menu_view import ConfigMenuView  

def switch_view(container_frame, active_view):
    # Hide all views
    for widget in container_frame.winfo_children():
        widget.pack_forget()
         
    # Show the active view
    active_view.pack(fill="both", expand=True)

def main():
    # create the root window
    root = ctk.CTk()
    root.title("The best application (ever)")
    root.geometry("1280x720")
    root.resizable(False, False)
    root.bind("<Escape>", lambda e: root.quit())
     
    # Set appearance and color theme
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
     
    # Create a container for the views
    container_frame = ctk.CTkFrame(root)
    container_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
     
    # initialize our MVC components starting with the models
    create_levels_model = CreateLevelsModel()
    modify_levels_model = ModifyLevelsModel()
    play_levels_model = PlayLevelsModel()
    delete_levels_model = DeleteLevelsModel()
    menu_model = MenuModel()
    config_menu_model = ConfigMenuModel()
     
    # then the controllers
    create_levels_controller = CreateLevelsController(create_levels_model)
    modify_levels_controller = ModifyLevelsController(modify_levels_model)
    play_levels_controller = PlayLevelsController(play_levels_model)
    delete_levels_controller = DeleteLevelsController(delete_levels_model)
    menu_controller = MenuController(menu_model)
    config_menu_controller = ConfigMenuController(config_menu_model)
     
    # and finally the views
    create_levels_view = CreateLevelsView(container_frame, create_levels_controller)
    modify_levels_view = ModifyLevelsView(container_frame, modify_levels_controller)
    play_levels_view = PlayLevelsView(container_frame, play_levels_controller)
    delete_levels_view = DeleteLevelsView(container_frame, delete_levels_controller)
    config_menu_view = ConfigMenuView(container_frame, config_menu_controller)
    
    # Create the menu view and pass necessary views for navigation
    menu_view = MenuView(
        container_frame, 
        menu_controller,
        switch_view_callback=switch_view,
        create_levels_view=create_levels_view,
        modify_levels_view=modify_levels_view,
        play_levels_view=play_levels_view,
        config_menu_view=config_menu_view
    )
    
    # Show the menu view initially
    switch_view(container_frame, menu_view)
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()