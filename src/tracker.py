import cv2
import pandas as pd
from .detector import create_background_subtractor, detect_tardigrade

def track_video(video_path, output_csv=None, min_area=800, max_area=15000):
    """
    Lee un archivo de video, detecta al tardígrado fotograma a fotograma
    y extrae sus métricas de posición y forma a lo largo del tiempo.
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    # Creamos el sustractor de fondo mediante la función auxiliar
    bg_subtractor = create_background_subtractor()
    records = []
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Llamamos a la función de detección directamente
        contour, _ = detect_tardigrade(frame, bg_subtractor, min_area=min_area, max_area=max_area)
        
        if contour is not None:
            # 1. Centroide (Centro de masa del cuerpo)
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = M["m10"] / M["m00"]
                cy = M["m01"] / M["m00"]
            else:
                cx, cy = 0, 0
                
            # 2. Dinámica de forma (Ajustar una elipse para medir extensión/compresión)
            if len(contour) >= 5:
                # fitEllipse devuelve: (centro), (eje_menor, eje_mayor), ángulo
                _, (d1, d2), angle = cv2.fitEllipse(contour)
                length = max(d1, d2)
                width = min(d1, d2)
                aspect_ratio = length / (width + 1e-6)
            else:
                # Alternativa si el contorno tiene muy pocos puntos para una elipse
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
