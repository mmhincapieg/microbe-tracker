import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def apply_scientific_style():
    """Configura un estilo de publicación científica similar a Nature/Science."""
    sns.set_theme(style="ticks")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8.5,
        "figure.titlesize": 12,
        "lines.linewidth": 1.5,
        "axes.linewidth": 1.0,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.top": True,
        "ytick.right": True
    })

def plot_kinematics_summary(df, output_path="output/kinematics_plots.png"):
    """
    Genera un panel de figuras al estilo científico (paper):
      - A: Velocidad instantánea vs tiempo (con línea suavizada)
      - B: Ángulo de orientación (º) vs tiempo
      - C: Relación de aspecto (deformación corporal) y estados (Contraction/Extension)
      - D: Tasa de cambio de longitud (dLength/dt) vs tiempo
    """
    apply_scientific_style()
    df_clean = df.dropna(subset=['velocity']).copy()

    fig, axes = plt.subplots(2, 2, figsize=(10, 7), dpi=300)
    plt.subplots_adjust(hspace=0.35, wspace=0.28)

    # Colores sobrios tipo paper
    color_primary = "#4682B4"   # Steel blue (similar a 'Experiment')
    color_accent = "#D9534F"    # Reddish / coral (similar a 'Simulation')
    color_state_contract = "#FFEBEE" # Suave fondo rojizo para contracción
    color_state_extend = "#E0F2F1"   # Suave fondo cian para extensión

    # -------------------------------------------------------------
    # Panel A: Velocidad vs Tiempo
    # -------------------------------------------------------------
    ax_a = axes[0, 0]
    # Curva cruda + suavizada
    sns.lineplot(data=df_clean, x="timestamp_s", y="velocity", ax=ax_a, 
                 color=color_primary, alpha=0.5, label="Raw Velocity")
    if "velocity_smoothed" in df_clean.columns and df_clean["velocity_smoothed"].notna().any():
        sns.lineplot(data=df_clean, x="timestamp_s", y="velocity_smoothed", ax=ax_a, 
                     color=color_accent, linestyle="--", label="Smoothed")
    ax_a.set_xlabel("Time (s)", fontweight="bold")
    ax_a.set_ylabel("Velocity (px/s)", fontweight="bold")
    ax_a.text(-0.15, 1.08, "A", transform=ax_a.transAxes, fontsize=13, fontweight="bold", va="top")
    ax_a.legend(loc="upper right", frameon=True)
    ax_a.set_xlim(df_clean["timestamp_s"].min(), df_clean["timestamp_s"].max())

    # -------------------------------------------------------------
    # Panel B: Ángulo de Orientación vs Tiempo
    # -------------------------------------------------------------
    ax_b = axes[0, 1]
    sns.lineplot(data=df_clean, x="timestamp_s", y="orientation_deg", ax=ax_b, 
                 color=color_primary, label="Orientation")
    ax_b.set_xlabel("Time (s)", fontweight="bold")
    ax_b.set_ylabel("Yaw angle (°)", fontweight="bold")
    ax_b.text(-0.15, 1.08, "B", transform=ax_b.transAxes, fontsize=13, fontweight="bold", va="top")
    ax_b.legend(loc="upper right", frameon=True)
    ax_b.set_xlim(df_clean["timestamp_s"].min(), df_clean["timestamp_s"].max())

    # -------------------------------------------------------------
    # Panel C: Relación de aspecto (Aspect Ratio) y sombreado de estados
    # -------------------------------------------------------------
    ax_c = axes[1, 0]
    sns.lineplot(data=df_clean, x="timestamp_s", y="aspect_ratio", ax=ax_c, 
                 color=color_primary, label="Aspect Ratio")
    
    # Sombreado de fondo según estado morfológico (similar a Beat / Restore en la imagen)
    # Marcar regiones Contracted vs Extended
    if "morph_state" in df_clean.columns:
        contracted = df_clean[df_clean["morph_state"] == "Contracted"]
        for _, row in contracted.iterrows():
            ax_c.axvspan(row["timestamp_s"] - 0.015, row["timestamp_s"] + 0.015, 
                         color="#FFF3E0", alpha=0.3, lw=0)

    ax_c.set_xlabel("Time (s)", fontweight="bold")
    ax_c.set_ylabel("Aspect Ratio (L/W)", fontweight="bold")
    ax_c.text(-0.15, 1.08, "C", transform=ax_c.transAxes, fontsize=13, fontweight="bold", va="top")
    ax_c.legend(loc="upper right", frameon=True)
    ax_c.set_xlim(df_clean["timestamp_s"].min(), df_clean["timestamp_s"].max())

    # -------------------------------------------------------------
    # Panel D: Tasa de deformación (dLength / dt)
    # -------------------------------------------------------------
    ax_d = axes[1, 1]
    if "d_length_dt" in df_clean.columns:
        sns.lineplot(data=df_clean, x="timestamp_s", y="d_length_dt", ax=ax_d, 
                     color=color_accent, linestyle=":", label="Deformation rate")
    ax_d.axhline(0, color="gray", linestyle="--", linewidth=0.8, alpha=0.7)
    ax_d.set_xlabel("Time (s)", fontweight="bold")
    ax_d.set_ylabel("Deformation rate (px/s)", fontweight="bold")
    ax_d.text(-0.15, 1.08, "D", transform=ax_d.transAxes, fontsize=13, fontweight="bold", va="top")
    ax_d.legend(loc="upper right", frameon=True)
    ax_d.set_xlim(df_clean["timestamp_s"].min(), df_clean["timestamp_s"].max())

    # Guardar figura
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Gráfico científico generado exitosamente en: {output_path}")
