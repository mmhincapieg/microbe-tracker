import cv2
import numpy as np

def create_background_subtractor():
    """
    Crea y configura el algoritmo sustractor de fondo (MOG2).
    Aprende el fondo para separar lo que se mueve de lo que está quieto.
    """
    return cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)

def detect_tardigrade(frame, bg_subtractor, min_area=500, max_area=15000):
    """
    Procesa un fotograma (frame) y encuentra el contorno del tardígrado en movimiento.
    
    Parámetros:
        frame: Imagen en color (BGR) del video.
        bg_subtractor: Objeto sustractor de fondo configurado.
        min_area: Área mínima en píxeles para ignorar ruido.
        max_area: Área máxima en píxeles para ignorar cambios globales de luz.
        
    Retorna:
        target_contour: El contorno más grande encontrado (o None si no detecta nada).
        mask_cleaned: La imagen binaria (máscara blanco y negro) limpia.
    """
    # 1. Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 2. Suavizar la imagen para reducir ruido
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 3. Restar el fondo para detectar movimiento (lo estático es negro, lo que se mueve es blanco)
    fg_mask = bg_subtractor.apply(blurred)
    
    # 4. Operaciones morfológicas para limpiar la máscara
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_closed = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)   # Cierra huecos internos
    mask_cleaned = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel) # Elimina puntos sueltos de ruido

    # 5. Encontrar los bordes/contornos de las zonas blancas
    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 6. Filtrar por tamaño (área)
    valid_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area < area < max_area:
            valid_contours.append(cnt)
            
    # 7. Asumir que el contorno más grande es el tardígrado
    if valid_contours:
        target_contour = max(valid_contours, key=cv2.contourArea)
        return target_contour, mask_cleaned
        
    return None, mask_cleaned
