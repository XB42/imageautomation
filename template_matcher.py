import cv2
import numpy as np
import pyautogui

def find_template_in_screenshot(template_path, output_path="found_region.png", tiny_threshold=50):
    """
    Searches for a template image within a screenshot and saves the detected region.
    For very small (tiny) template images, the function uses template matching.
    For larger images, it uses SIFT feature matching with homography estimation.

    Args:
        template_path (str): The file path to the template image.
        output_path (str): The file path to save the found region. Defaults to "found_region.png".
        tiny_threshold (int): If the minimum dimension of the template is below this value,
                              template matching is used instead of SIFT.

    Returns:
        bool: True if the template is found and the region is saved; False otherwise.
    """
    # Load the template image from disk.
    template = cv2.imread(template_path)
    if template is None:
        print(f"Template image '{template_path}' not found.")
        return False

    # Convert the template to grayscale.
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    h_temp, w_temp = template_gray.shape

    # Capture a screenshot of the current screen.
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    # Convert from RGB (PIL format) to BGR (OpenCV format)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    # If the template is very small, use template matching.
    if min(h_temp, w_temp) < tiny_threshold:
        print("Template is tiny. Using template matching instead of SIFT.")
        result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.8  # Adjust the threshold as needed.
        if max_val < threshold:
            print(f"No good match found (max correlation: {max_val:.2f}).")
            return False

        # Determine the matching region using the location of the highest correlation.
        top_left = max_loc
        bottom_right = (top_left[0] + w_temp, top_left[1] + h_temp)
        found_region = screenshot_np[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        cv2.imwrite(output_path, found_region)
        print(f"Found region saved as '{output_path}' using template matching.")
        return True

    # Otherwise, use SIFT for feature matching (more robust for larger templates).
    sift = cv2.SIFT_create()
    kp_template, des_template = sift.detectAndCompute(template_gray, None)
    kp_screen, des_screen = sift.detectAndCompute(screenshot_gray, None)

    if des_template is None or des_screen is None:
        print("Failed to compute descriptors for one of the images.")
        return False

    # Create a brute-force matcher using the L2 norm (appropriate for SIFT).
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(des_template, des_screen, k=2)

    # Apply Lowe's ratio test to filter out weak matches.
    good_matches = [m for m, n in matches if m.distance < 0.7 * n.distance]

    MIN_MATCH_COUNT = 6  # Adjust this value based on your requirements.
    if len(good_matches) < MIN_MATCH_COUNT:
        print(f"Not enough good matches found ({len(good_matches)}/{MIN_MATCH_COUNT}).")
        return False

    # Extract the matched keypoint locations.
    src_pts = np.float32([kp_template[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_screen[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Compute homography using RANSAC to account for outliers.
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    if M is None:
        print("Homography could not be computed.")
        return False

    # Define the corners of the template image.
    h, w = template_gray.shape
    template_corners = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
    # Transform the corners to the screenshot coordinate system.
    screen_corners = cv2.perspectiveTransform(template_corners, M)

    # Determine the bounding box from the transformed corners.
    x_coords = screen_corners[:, 0, 0]
    y_coords = screen_corners[:, 0, 1]
    x_min, x_max = int(np.min(x_coords)), int(np.max(x_coords))
    y_min, y_max = int(np.min(y_coords)), int(np.max(y_coords))

    # Clamp coordinates to within the screenshot dimensions.
    height, width = screenshot_np.shape[:2]
    x_min, y_min = max(x_min, 0), max(y_min, 0)
    x_max, y_max = min(x_max, width), min(y_max, height)

    # Crop the region where the template is detected.
    found_region = screenshot_np[y_min:y_max, x_min:x_max]
    cv2.imwrite(output_path, found_region)
    print(f"Found region saved as '{output_path}' using SIFT matching.")
    return True

# This block allows the module to be run directly for testing purposes.
if __name__ == "__main__":
    import sys
    # If no template image is provided, display usage information.
    if len(sys.argv) < 2:
        print("Usage: python script.py <template_image_path>")
    else:
        template_image_path = sys.argv[1]
        find_template_in_screenshot(template_image_path)
