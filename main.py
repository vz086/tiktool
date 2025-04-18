import customtkinter
import os
from PIL import Image
import threading
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from utils.captcha import CaptchaWindow

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set dark mode by default
        customtkinter.set_appearance_mode("dark")
        
        self.title("TikTool V1.0")
        self.geometry("700x450")
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with dark mode image only
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(200, 200))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="TikTool Bot",
                                                             compound="left", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Configuration",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Likes",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")


        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Followers",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")


        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Views",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")


        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="Configuration", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.home_frame_large_image_label.grid(row=1, column=0, padx=20, pady=10)




        self.entry1 = customtkinter.CTkEntry(self.home_frame,width=300, placeholder_text="Profile Link")
        self.entry1.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        self.entry2 = customtkinter.CTkEntry(self.home_frame,width=300, placeholder_text="Video Link")
        self.entry2.grid(row=3, column=0, columnspan=2, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.like_switch = customtkinter.CTkSwitch(
            master=self.second_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.like_switch, "likes"))
        self.like_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew")
        
        self.second_frame_textbox = customtkinter.CTkTextbox(self.second_frame, width=350, height=350)
        self.second_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew")
        
        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.follower_switch = customtkinter.CTkSwitch(
            master=self.third_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.follower_switch, "followers"))
        self.follower_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew")
        
        self.third_frame_textbox = customtkinter.CTkTextbox(self.third_frame, width=350, height=350)
        self.third_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew")

        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.views_switch = customtkinter.CTkSwitch(
            master=self.fourth_frame,
            text="Start the bot",
            font=customtkinter.CTkFont(size=14),
            onvalue="on",
            offvalue="off",
            fg_color="#2f2f2f",
            progress_color="#1e90ff",
            button_color="#ffffff",
            button_hover_color="#cccccc",
            command=lambda: self.handle_switch_toggle(self.views_switch, "views"))
        self.views_switch.grid(row=0, column=1, padx=195, pady=10, sticky="nsew")
        
        self.fourth_frame_textbox = customtkinter.CTkTextbox(self.fourth_frame, width=350, height=350)
        self.fourth_frame_textbox.grid(row=1, column=1, padx=(7, 0), pady=(20, 0), sticky="nsew")

        # Initialize bot threads
        self.likes_bot_thread = None
        self.followers_bot_thread = None
        self.views_bot_thread = None
        
        # Initialize stop flags
        self.likes_bot_running = False
        self.followers_bot_running = False
        self.views_bot_running = False

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def handle_switch_toggle(self, activated_switch, bot_type):
        # List of all switches
        all_switches = [self.like_switch, self.follower_switch, self.views_switch]
        
        # If the activated switch is being turned on
        if activated_switch.get() == "on":
            # Turn off all other switches
            for switch in all_switches:
                if switch != activated_switch:
                    switch.deselect()
            
            # Start the appropriate bot
            if bot_type == "likes":
                self.likes_bot_running = True
                self.likes_bot_thread = threading.Thread(target=self.run_likes_bot)
                self.likes_bot_thread.start()
            elif bot_type == "followers":
                self.followers_bot_running = True
                self.followers_bot_thread = threading.Thread(target=self.run_followers_bot)
                self.followers_bot_thread.start()
            elif bot_type == "views":
                self.views_bot_running = True
                self.views_bot_thread = threading.Thread(target=self.run_views_bot)
                self.views_bot_thread.start()
        else:
            # Stop the appropriate bot
            if bot_type == "likes":
                self.likes_bot_running = False
            elif bot_type == "followers":
                self.followers_bot_running = False
            elif bot_type == "views":
                self.views_bot_running = False

    def run_likes_bot(self):
        global driver
        openZefoy()
        like = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[3]/div/button').click()
        time.sleep(1)
        input = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/input')
        input.send_keys(self.entry2.get())
        time.sleep(1)
        self.second_frame_textbox.insert("end", "Likebot started!\n")
        while self.likes_bot_running:
            try:
                # Click the search button
                search_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/div/button')
                search_button.click()
                time.sleep(1)
                # Try to find and click the target button
                try:
                    target_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/div/form/button')
                    target_button.click()
                    self.second_frame_textbox.insert("end", "Likes sent successfully!\n")
                    self.second_frame_textbox.see("end")
                except:
                    self.second_frame_textbox.see("end")
                
                time.sleep(3)  # Wait 3 seconds before next attempt
                
            except Exception as e:
                self.second_frame_textbox.insert("end", f"Error: {str(e)}\n")
                self.second_frame_textbox.see("end")
                time.sleep(3)  # Wait 3 seconds before retrying
                
        driver.quit()
        self.second_frame_textbox.insert("end", "Views bot stopped.\n")
        self.second_frame_textbox.see("end")

    def run_followers_bot(self):
        global driver
        openZefoy()
        follower = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[2]/div/button').click()
        time.sleep(1)
        input = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/input')
        input.send_keys(self.entry1.get())
        time.sleep(1)
        self.third_frame_textbox.insert("end", "Followbot started!\n")
        while self.followers_bot_running:
            try:
                # Click the search button
                search_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/div/button')
                search_button.click()
                time.sleep(1)
                # Try to find and click the target button
                try:
                    target_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/div/form/button')
                    target_button.click()
                    self.third_frame_textbox.insert("end", "Followers sent successfully!\n")
                    self.third_frame_textbox.see("end")
                except:
                    self.third_frame_textbox.see("end")
                
                time.sleep(3)  # Wait 3 seconds before next attempt
                
            except Exception as e:
                self.third_frame_textbox.insert("end", f"Error: {str(e)}\n")
                self.third_frame_textbox.see("end")
                time.sleep(3)  # Wait 3 seconds before retrying
                
        driver.quit()
        self.third_frame_textbox.insert("end", "Views bot stopped.\n")
        self.third_frame_textbox.see("end")

    def run_views_bot(self):
        global driver
        openZefoy()
        view = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div/div/div[6]/div/button').click()
        time.sleep(1)
        input = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/input')
        input.send_keys(self.entry2.get())
        time.sleep(1)
        self.fourth_frame_textbox.insert("end", "Viewbot started!\n")
        while self.views_bot_running:
            try:
                # Click the search button
                search_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/form/div/div/button')
                search_button.click()
                time.sleep(1)
                # Try to find and click the target button
                try:
                    target_button = driver.find_element(By.XPATH, '/html/body/div[10]/div/div/div[1]/div/form/button')
                    target_button.click()
                    self.fourth_frame_textbox.insert("end", "1000 views sent successfully!\n")
                    self.fourth_frame_textbox.see("end")
                except:
                    self.fourth_frame_textbox.see("end")
                
                time.sleep(3)  # Wait 3 seconds before next attempt
                
            except Exception as e:
                self.fourth_frame_textbox.insert("end", f"Error: {str(e)}\n")
                self.fourth_frame_textbox.see("end")
                time.sleep(3)  # Wait 3 seconds before retrying
                
        driver.quit()
        self.fourth_frame_textbox.insert("end", "Views bot stopped.\n")
        self.fourth_frame_textbox.see("end")

def openZefoy():
    global driver
    chrome_options = uc.ChromeOptions()  
    chrome_options.add_argument("--headless")
    driver = uc.Chrome(options=chrome_options)
    driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": ["https://fundingchoicesmessages.google.com/*"]})
    driver.execute_cdp_cmd("Network.enable", {})
    driver.get("https://zefoy.com/")
    time.sleep(1)
    complete = captcha()


def captcha():
    input = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/div/div/div/input[1]')
    input.send_keys(captchaSave())
    time.sleep(3)
    submit = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/div/div/div/div/button').click()
    time.sleep(3)


def captchaSave():
    global driver
    with open(f'captcha.png', 'wb') as file:
        l = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/form/div/div/img')
        file.write(l.screenshot_as_png)
    captcha_window = CaptchaWindow()
    return captcha_window.result


if __name__ == "__main__":
    app = App()
    app.mainloop()
