import pandas as pd
from src.tracker import track_video
from src.kinematics import compute_kinematics
from src.plotter import plot_kinematics_summary

# Rutas relativas como strings
video_path = "data/01_sampleclip.mov"
output_csv = "output/tardigrade_tracking.csv"
kinematics_csv = "output/tardigrade_kinematics.csv"
plot_output = "output/kinematics_plots.png"

print(f"\nIniciando tracking del video: {video_path}")
df_raw = track_video(video_path, output_csv=output_csv)
print(f"Tracking completado! Fotogramas analizados: {len(df_raw)}")

# Calcular cinemática (velocidad, estado de contracción/extensión)
df_metrics = compute_kinematics(df_raw)
df_metrics.to_csv(kinematics_csv, index=False)
print(f"Cinemática calculada y guardada en: {kinematics_csv}")

# Generar gráficos científicos estilo publicación
plot_kinematics_summary(df_metrics, output_path=plot_output)


# Generar gráficos científicos estilo publicación
plot_kinematics_summary(df_metrics, output_path=plot_output)