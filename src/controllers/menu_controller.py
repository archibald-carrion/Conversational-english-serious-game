# controllers/menu_controller.py
import customtkinter as ctk
import models.menu_model as menu_model

class MenuController():
    def __init__(self, model: menu_model.MenuModel):
        return None

    def quit_application(self):
        # Quit the application
        ctk.CTk().quit()