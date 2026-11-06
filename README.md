# Microbe Tracker 🔬

A lightweight, automated computer vision and kinematics tracking pipeline in Python designed to analyze microorganism motility (such as tardigrades) from brightfield microscope video recordings.

---

## 📌 Overview

Studying microscopic organism kinematics manually is time-consuming and prone to human error. **Microbe Tracker** processes microscope video footage frame by frame to:
1. **Segment moving organisms** from static slide debris using Gaussian blur and Gaussian Mixture-based Background Subtraction (MOG2).
2. **Track spatial coordinates and body geometry**, including centroid coordinates $(x, y)$, body length, width, surface area, and yaw angle (orientation).
3. **Quantify kinematics & morphology**, computing instantaneous velocity, smoothed velocity profiles, rate of deformation ($\frac{d\,\text{Length}}{dt}$), and contraction vs. extension states.
4. **Generate publication-ready scientific figures** inspired by biomechanics and biophysics journal standards.

---

## 📁 Project Structure

```text
microbe-tracker/
├── data/
│   └── 01_sampleclip.mov         # Input microscope video recordings
├── output/
│   ├── tardigrade_tracking.csv   # Raw frame-by-frame spatial & geometric data
│   ├── tardigrade_kinematics.csv # Computed speed, acceleration, and morphological states
│   └── kinematics_plots.png      # Publication-ready summary multi-panel figure
├── src/
│   ├── detector.py               # Functional background subtraction & contour detection
│   ├── tracker.py                # Video capture, centroid extraction & ellipse fitting
│   ├── kinematics.py             # Velocity & morphological deformation classification
│   └── plotter.py                # Publication-style visualization (Seaborn / Matplotlib)
├── main.py                       # Main pipeline orchestration script
├── requirements.txt              # Project dependencies
└── README.md
```

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/microbe-tracker.git
   cd microbe-tracker
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Place your video clip in the `data/` directory (e.g. `data/01_sampleclip.mov`), then simply run:

```bash
python main.py
```

### Execution Flow:
1. `main.py` reads the video and runs `track_video()`.
2. Extracted trajectories are saved to `output/tardigrade_tracking.csv`.
3. Kinematics and deformation are calculated via `compute_kinematics()` and exported to `output/tardigrade_kinematics.csv`.
4. `plot_kinematics_summary()` produces a 4-panel figure saved at `output/kinematics_plots.png`.

---

## 📊 Extracted Metrics

| Metric | Column Name | Description |
| :--- | :--- | :--- |
| **Centroid $(x, y)$** | `x`, `y` | Center of mass coordinates calculated via spatial moments. |
| **Area** | `area_px` | Bounding contour surface area in pixels. |
| **Body Dimensions** | `length_px`, `width_px` | Major and minor axes obtained from fitted bounding ellipses. |
| **Aspect Ratio** | `aspect_ratio` | $\text{Length} / \text{Width}$; indicates body elongation. |
| **Orientation** | `orientation_deg` | Angle of the major axis ($0^\circ - 180^\circ$). |
| **Velocity** | `velocity`, `velocity_smoothed` | Instantaneous and rolling-window smoothed displacement speed. |
| **Morphological State** | `morph_state` | Classified as `Contracted`, `Extended`, or `Intermediate`. |
| **Deformation Rate** | `d_length_dt` | Speed of body stretching or compression ($\text{px/s}$). |

---

## 📈 Visualizations

The generated figure (`output/kinematics_plots.png`) provides:
- **Panel A:** Instantaneous vs. smoothed velocity over time.
- **Panel B:** Yaw / orientation angle dynamics over time.
- **Panel C:** Body aspect ratio with shaded intervals corresponding to contraction events.
- **Panel D:** Deformation rate showing active extension vs. contraction cycles.

---

## 🛠️ Built With

- **[OpenCV (cv2)](https://opencv.org/)** — Computer vision, background subtraction (MOG2), and morphological filters.
- **[NumPy](https://numpy.org/)** & **[Pandas](https://pandas.pydata.org/)** — High-performance numerical operations and time-series data handling.
- **[Matplotlib](https://matplotlib.org/)** & **[Seaborn](https://seaborn.pydata.org/)** — High-resolution scientific figures.
