import numpy as np
import pandas as pd

def compute_kinematics(df: pd.DataFrame, pixel_to_um_ratio: float = 1.0):
    """
    Calculates speed, acceleration, and classifies morphological states.
    pixel_to_um_ratio: calibration factor (micrometers per pixel). Default is 1 for raw pixels.
    """
    df = df.copy()
    
    # 1. Compute displacements and velocity
    df['dx'] = df['x'].diff() * pixel_to_um_ratio
    df['dy'] = df['y'].diff() * pixel_to_um_ratio
    df['dt'] = df['timestamp_s'].diff()
    
    # Instantaneous speed (distance / time)
    df['velocity'] = np.sqrt(df['dx']**2 + df['dy']**2) / df['dt']
    
    # Smooth velocity with a rolling window (e.g., over 0.5 seconds) to reduce tracking jitter
    window_size = max(3, int(len(df) * 0.02))
    df['velocity_smoothed'] = df['velocity'].rolling(window=window_size, center=True).mean()
    
    # 2. Analyze shape deformation (Contraction vs Extension)
    # A low aspect ratio means the tardigrade is scrunched up.
    # A high aspect ratio means it is elongated.
    mean_aspect = df['aspect_ratio'].mean()
    std_aspect = df['aspect_ratio'].std()
    
    # Define thresholds dynamically based on the organism's baseline
    contracted_threshold = mean_aspect - (0.5 * std_aspect)
    extended_threshold = mean_aspect + (0.5 * std_aspect)
    
    def classify_state(ar):
        if pd.isna(ar):
            return "Unknown"
        elif ar < contracted_threshold:
            return "Contracted"
        elif ar > extended_threshold:
            return "Extended"
        else:
            return "Intermediate"

    df['morph_state'] = df['aspect_ratio'].apply(classify_state)
    
    # Rate of shape change (how fast it is contracting or stretching)
    df['d_length_dt'] = df['length_px'].diff() / df['dt']
    
    return df