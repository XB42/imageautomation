from imagelister import recreate_folders
from template_matcher import find_template_in_screenshot
import os
import time
import pyautogui  # This module is used for simulating mouse clicks

time.sleep(2)
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
        time.sleep(0.5)  # Wait briefly after clicking
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
        # Optional: Pause for a few seconds to switch to a relevant window
        time.sleep(1)
        # Press Ctrl + A
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('backspace')
        time.sleep(1)
        pyautogui.moveTo(1200, 500)
        time.sleep(2)
        pyautogui.doubleClick()
        time.sleep(2)
        # Process only image files.
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            input_path = os.path.join(root, filename)
            output_path = os.path.join(output_dir, filename)
            
            # Determine the base name (without extension) in lower case.
            base_name = os.path.splitext(filename)[0].lower()
            
            # If the file name is selectquote or selectrepost, click on quote.png before processing.
            if base_name in ["selectquote", "selectrepost"]:
                quotepath = os.path.join(output_folder, "quotetweetfromrange","quote.png")
                press_button(quotepath)
                time.sleep(2)
                pyautogui.moveTo(pyautogui.position()[0] - 200, pyautogui.position()[1])
                time.sleep(2)
            # If the file name is replyprompt, click on reply.png before processing.
            elif base_name == "replyprompt":
                replypath = os.path.join(output_folder, "replyspitter","reply.png")
                press_button(replypath)
                time.sleep(2)
                pyautogui.moveTo(pyautogui.position()[0] - 200, pyautogui.position()[1])
                time.sleep(2)

            elif base_name == "replybutton":
                # Use the same reply.png path (assuming this is the same button image)
                replypath = os.path.join(output_folder, "replyspitter", "reply.png")
                press_button(replypath)
                time.sleep(2)
                
                # Move cursor or make any adjustment if needed
                pyautogui.moveTo(pyautogui.position()[0] - 200, pyautogui.position()[1])
                time.sleep(2)
                
                # Type some text after pressing the reply button
                pyautogui.write("pp", interval=0.05)
                time.sleep(1)
            elif base_name == "quotebutton":
                # Path to your quote button image (change subfolder/filename as needed)
                quotepath = os.path.join(output_folder, "quotetweetfromrange", "quote.png")
                press_button(quotepath)
                time.sleep(2)       
    
    # Let's assume you need to select the quoted text (this is highly app-dependent)
    # For example, press_button on "quote.png" might open a quote snippet. 
    # Then maybe we select all or do a certain hotkey:
    # pyautogui.hotkey('ctrl', 'a')  # or any other combination
    
    # Type your comment on the quote
                pyautogui.write("pp", interval=0.05)


            # Now process the image.
            if find_template_in_screenshot(input_path, output_path):
                print(f"Template found and region saved for {input_path}.")
            else:
                print(f"Template not found in {input_path}.")
