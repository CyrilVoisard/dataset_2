# A Dataset of Clinical Gait Signals with Wearable Sensors from Healthy, Neurological, and Orthopedic Cohorts

This repository provides code snippets to load the dataset published as open source. It can be downloaded through [this publication link](https://doi.org/10.6084/m9.figshare.28806086) (~2.19 GB).

## Dataset overview

The dataset contains time-series signals recorded from wearable inertial sensors during clinical gait assessments in three cohorts: **healthy**, **neurological**, and **orthopedic** individuals. The data is organized by cohort, subject, and trial, and includes both raw and processed sensor data, as well as metadata and visualization outputs.

It provides 1356 gait trials from 260 participants equipped with four inertial measurement units placed on the head, lower back, and dorsal part of each foot. 
They followed a standardized protocol involving a basic sequence of activities: 
- standing still
- walking straight ahead
- turning around 180° (u-turn)
- walking back to the starting point
- stopping

The dataset is intended for researchers in gait analysis, biomedical signal processing, and clinical rehabilitation.

## Folder Structure

The repository is structured as follows:

```
.
├── data/
│   ├── healthy/
│   ├── neuro/
│   └── ortho/
├── quick_start/
│   ├── load_data.py
│   └── plot_data.py
```

- **Cohorts** (`healthy`, `neuro`, `ortho`) are stored in the `data/` directory.
- **Subjects** are organized under cohort-specific subfolders.
- **Trials** are named `<subject>_<trialID>` and contain:
  - Raw sensor files (`_HE`, `_LB`, `_LF`, `_RF`)
  - Processed data
  - Metadata (`.json`)
  - Optional visualizations (`.png`)

## File Descriptions

### Raw Sensor Data (`*.txt`)
Each raw file contains inertial measurements (e.g., angular velocity) recorded by a specific sensor location:
- `HE` – Head
- `LB` – Lower Back
- `LF` – Left Foot
- `RF` – Right Foot

Data is tab-delimited.

### Processed Data (`*_processed_data.txt`)
A cleaned and merged dataset with synchronized sensor signals and potentially extracted features.

### Metadata (`*_meta.json`)
Includes metadata such as:
- Patient information 
- Trial identifiers
- Pathology information
- Sampling frequency
- U-turn boundaries
- Detected gait events (toe-off and heel-strike)
See publication for more details.

### Plot (`*_plot.png`)
Graphical representation of the processed gait data with event segmentation.

---

## Quick Start

You can quickly load and visualize the dataset using the provided Python scripts in the `quick_start/` directory, also available in this GitHub repository. 

### 1. Loading the Data

Use `load_data.py` to explore the dataset:

```python
from load_data import load_bdd, load_cohort, load_patient, load_trial

base_path = "path/to/data"

# Load all cohorts
bdd = load_bdd(base_path)

# Load a specific trial
trial = load_trial(base_path, "HS_2_1")
```

This script returns structured dictionaries of the raw and processed data, plus metadata.

### 2. Visualizing Gait Events

Use `plot_data.py` to visualize the segmentation of gait events:

```python
from plot_data import plot_segmentation_gait_events, plot_segmentation

plot_segmentation_gait_events(trial)
plot_segmentation(trial)
```

These functions generate figures highlighting:
- Gait phases (go, u-turn, back)
- Swing and stance periods
- Toe-off and heel-strike events

---

## Processed Data

The code used to pre-process the data is available in this repository, in the `process_data/` directory, for reasons of reproducibility.


## License CC BY 4.0

Please cite the associated paper and respect the dataset’s intended use for academic, research, and non-commercial purposes only.
```
@article{,
  title = {},
  author = {},
  journal = {},
  pages = {},
  number = {},
  url = {},
  volume = {},
  year = {}
}
```
