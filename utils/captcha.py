import customtkinter
import os
from PIL import Image
import threading
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

class CaptchaWindow(customtkinter.CTkToplevel):
    def __init__(self, is_retry=False):
        super().__init__()
        self.geometry("400x500")
        self.title("Captcha Entry")
        
        # Make window appear on top
        self.lift()  # Lift the window
        self.attributes('-topmost', True)  # Keep on top
        self.focus_force()  # Force focus
        
        # Load and display the captcha image
        img = customtkinter.CTkImage(Image.open("captcha.png"), size=(300, 100))
        self.image_label = customtkinter.CTkLabel(self, image=img, text="")
        self.image_label.pack(pady=20)
        
        # Show error message if retry
        if is_retry:
            self.error_label = customtkinter.CTkLabel(self, text="Incorrect captcha! Please try again.", text_color="red")
            self.error_label.pack(pady=10)
        
        # Create entry for captcha input
        self.captcha_entry = customtkinter.CTkEntry(self, width=200, placeholder_text="Enter Captcha")
        self.captcha_entry.pack(pady=20)
        self.captcha_entry.focus()  # Set focus to entry
        
        # Create submit button
        self.submit_button = customtkinter.CTkButton(self, text="Complete", command=self.submit)
        self.submit_button.pack(pady=20)
        
        self.result = None
        self.wait_window()
    
    def submit(self):
        self.result = self.captcha_entry.get()
        self.destroy()
