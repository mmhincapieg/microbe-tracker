import cv2
import numpy as np

class TardigradeDetector:
    def __init__(self, min_area=500, max_area=15000):
        # The tardigrade is significantly larger than background debris
        self.min_area = min_area
        self.max_area = max_area
        # Background subtractor to isolate movement and ignore static slide debris
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

    def detect(self, frame):
        """Extracts the largest moving contour matching the tardigrade."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Blur to smooth out internal textures of the organism
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(blurred)
        
        # Morphological operations to close holes inside the tardigrade body
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask_closed = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        mask_cleaned = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)

        # Find contours
        contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        valid_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if self.min_area < area < self.max_area:
                valid_contours.append(cnt)
                
        # Assume the largest valid moving contour is the tardigrade
        if valid_contours:
            target_contour = max(valid_contours, key=cv2.contourArea)
            return target_contour, mask_cleaned
            
        return None, mask_cleaned