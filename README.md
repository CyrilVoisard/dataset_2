# A Dataset of Clinical Gait and U-Turns Signals with Wearable Sensors from Hemiplegic Post-Stroke Patients

This repository provides code snippets to load the dataset published as open source. It can be downloaded through [XXXX](XXXX) (~1.07 GB).

## Description rapide du dataset publié

The dataset provides 180 gait trials from 30 hemiplegic post-stroke participants equipped with four inertial measurement units placed on the head, lower back, and dorsal part of each foot. 
They followed a standardized protocol involving a basic sequence of activities: 
- standing still
- walking straight ahead
- turning around 180° (u-turn)
- walking back to the starting point
- stopping

The published dataset comprises a comprehensive collection of kinematic and kinetic data obtained from hemiplegic patients performing u-turns before and after rotation, encompassing a detailed analysis of gait parameters. Its quality is also ensured by the breadth of metadata provided from clinical examinations and reference clinical scales. 

## Dependencies 

* numpy
* scipy

## Basic Scripts

* `process_error_vicon.py`: Iteratively evaluates the error of the five classical zero-velocity detectors when their optimized zero-velocity outputs are used. The results are saved in `results/vicon_results_raw.csv`.

* `train_motion_classifier.py`: Trains a three-class motion classifier (walk vs. run vs. stairs) using a subset of the training data, and will reproduce the accuracy of the classifier for the validation set.


## Reproduction of Paper Results

We have included two scripts that reproduce the main results in our paper:

* `process_error_hallway.py`

* `plot_hallway_data.py` 


## Citation

If you use this code in your research, please cite:

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
