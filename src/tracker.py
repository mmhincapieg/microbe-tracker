import cv2
import pandas as pd
from detector import TardigradeDetector

def track_video(video_path, output_csv=None):
    cap = cv2.VideoCapture("01_sampleclip.mov", "/Users/mariamanuh/CodingProjects/microbe-tracker/data")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    detector = TardigradeDetector(min_area=800) # Adjusted for typical tardigrade size
    records = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        contour, _ = detector.detect(frame)
        
        if contour is not None:
            # 1. Centroid (Center of Mass)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = M["m10"] / M["m00"]
                cy = M["m01"] / M["m00"]
            else:
                cx, cy = 0, 0
                
            # 2. Shape Dynamics (Fitted Ellipse for Body Extension/Compression)
            if len(contour) >= 5:
                # fitEllipse returns: (center_x, center_y), (minor_axis, major_axis), angle
                _, (d1, d2), angle = cv2.fitEllipse(contour)
                length = max(d1, d2)
                width = min(d1, d2)
                aspect_ratio = length / (width + 1e-6)
            else:
                # Fallback to bounding box if contour is too small
                x, y, w, h = cv2.boundingRect(contour)
                length = max(w, h)
                width = min(w, h)
                aspect_ratio = length / (width + 1e-6)
                angle = 0

            records.append({
                "frame": frame_idx,
                "timestamp_s": frame_idx / fps,
                "x": cx,
                "y": cy,
                "area_px": cv2.contourArea(contour),
                "length_px": length,
                "width_px": width,
                "aspect_ratio": aspect_ratio,
                "orientation_deg": angle
            })
            
        frame_idx += 1

    cap.release()
    df = pd.DataFrame(records)
    
    if output_csv:
        df.to_csv(output_csv, index=False)
        
    return df