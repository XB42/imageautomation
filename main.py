from imagelister import recreate_folders
from template_matcher import find_template_in_screenshot
import os
import time
import pyautogui  # This module is used for simulating mouse clicks

# Initial delay to allow time for setup
time.sleep(20)
recreate_folders()

# Define the input and output folders.
input_folder = "images"
output_folder = "recreated_images"

def press_button(image_path):
    """
    Locate the button image on screen and click its center.
    """
    location = pyautogui.locateCenterOnScreen(image_path)
    if location:
        pyautogui.click(location)
        time.sleep(5)  # Wait after clicking
        print(f"Clicked on {image_path} at {location}.")
    else:
        print(f"Button {image_path} not found on screen.")

# Walk through the input folder recursively.
for root, dirs, files in os.walk(input_folder):
    # Compute the relative path of the current directory.
    rel_path = os.path.relpath(root, input_folder)
    # Create the corresponding directory in the output folder.
    output_dir = os.path.join(output_folder, rel_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in files:
        # Pause to switch to the relevant window
        time.sleep(10)
        # Press Ctrl + A
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(10)
        pyautogui.hotkey('backspace')
        time.sleep(10)
        pyautogui.moveTo(1200, 500)
        time.sleep(20)
        pyautogui.doubleClick()
        time.sleep(20)
        # Process only image files.
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            input_path = os.path.join(root, filename)
            output_path = os.path.join(output_dir, filename)
            
            # Determine the base name (without extension) in lower case.
            base_name = os.path.splitext(filename)[0].lower()
            
            if base_name in ["selectquote", "selectrepost"]:
                quotepath = os.path.join(output_folder, "quotetweetfromrange", "quote.png")
                press_button(quotepath)
                time.sleep(20)
                pyautogui.moveTo(pyautogui.position()[0] - 200, pyautogui.position()[1])
                time.sleep(20)
            elif base_name == "replyprompt":
                replypath = os.path.join(output_folder, "replyspitter", "reply.png")
                press_button(replypath)
                time.sleep(20)
                pyautogui.moveTo(pyautogui.position()[0] - 200, pyautogui.position()[1])
                time.sleep(20)
            elif base_name == "replybutton":
                replypath = os.path.join(output_folder, "replyspitter", "reply.png")
                press_button(replypath)
                time.sleep(20)
                pyautogui.moveTo(pyautogui.position()[0] - 200, pyautogui.position()[1])
                time.sleep(20)
                pyautogui.write("pp", interval=0.05)
                time.sleep(10)
            elif base_name == "quotebutton":
                quotepath = os.path.join(output_folder, "quotetweetfromrange", "quote.png")
                press_button(quotepath)
                time.sleep(20)
                pyautogui.write("pp", interval=0.05)

            # Now process the image.
            if find_template_in_screenshot(input_path, output_path):
                print(f"Template found and region saved for {input_path}.")
            else:
                print(f"Template not found in {input_path}.")