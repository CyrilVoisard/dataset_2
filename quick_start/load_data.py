import os
import pandas as pd
import json

base_path = "paste/your/path"


def load_bdd(base_path):
    """
    Loads the complete structure of the database.

    Args:
        base_path (str): Path to the root of the database.

    Returns:
        dict: A dictionary containing the structure of cohorts, patients, and trials.
    """
    bdd_structure = {}
    for top_level in ["healthy", "ortho", "neuro"]:
        top_path = os.path.join(base_path, top_level)
        if os.path.exists(top_path):
            bdd_structure[top_level] = {}
            for cohort in os.listdir(top_path):
                cohort_path = os.path.join(top_path, cohort)
                if os.path.isdir(cohort_path):
                    bdd_structure[top_level][cohort] = [
                        patient for patient in os.listdir(cohort_path) if os.path.isdir(os.path.join(cohort_path, patient))
                    ]
    return bdd_structure


def load_cohort(base_path, cohort_name):
    """
    Loads information about a specific cohort.

    Args:
        base_path (str): Path to the root of the database.
        cohort_name (str): Name of the cohort to load.

    Returns:
        dict: A dictionary containing patients within the cohort.
    """
    cohort_path = None
    for top_level in ["healthy", "ortho", "neuro"]:
        top_path = os.path.join(base_path, top_level)
        if os.path.exists(top_path):
            for cohort in os.listdir(top_path):
                if cohort == cohort_name:
                    cohort_path = os.path.join(top_path, cohort)
                    cohort_top_level = top_level
                    break
    if not cohort_path:
        raise ValueError(f"The cohort '{cohort_name}' does not exist.")

    return cohort_top_level, {
        patient: os.listdir(os.path.join(cohort_path, patient))
        for patient in os.listdir(cohort_path) if os.path.isdir(os.path.join(cohort_path, patient))
    }


def load_patient(base_path, patient_name):
    """
    Loads information about a specific patient.

    Args:
        base_path (str): Path to the root of the database.
        cohort_name (str): Name of the cohort.
        patient_name (str): Name of the patient.

    Returns:
        str: Path to the patient's directory.
        list: List of trial directories for the specified patient.
    """
    cohort_name = patient_name.split("_")[0]
    top_level, cohort_data = load_cohort(base_path, cohort_name)
    if patient_name not in cohort_data:
        raise ValueError(f"The patient '{patient_name}' does not exist in cohort '{cohort_name}'.")

    patient_path = os.path.join(base_path, top_level, cohort_name, patient_name)
    return patient_path, os.listdir(patient_path)


def load_trial(base_path, trial_name):
    """
    Loads files for a specific trial.

    Args:
        base_path (str): Path to the root of the database.
        cohort_name (str): Name of the cohort.
        patient_name (str): Name of the patient.
        trial_name (str): Name of the trial.

    Returns:
        dict: A dictionary containing the trial :
            - "data_raw": Dictionary of raw sensor data organized by sensor type.
            - "data_processed": DataFrame of processed sensor data.
            - "metadata": Dictionary of metadata.
    """
    patient_name = trial_name.split("_")[0] + "_" + trial_name.split("_")[1]
    patient_path, patient_trials = load_patient(base_path, patient_name)
    if trial_name not in patient_trials:
        raise ValueError(f"The trial '{trial_name}' does not exist for patient '{patient_trials}'.")

    trial_path = os.path.join(patient_path, trial_name)

    # Load the data files
    data_raw = load_data_raw(trial_path)
    data_processed = load_data_processed(trial_path)

    # Load the metadata
    metadata = load_metadata(trial_path)

    return {"data_raw": data_raw, "data_processed": data_processed, "metadata": metadata}


def load_data_raw(trial_path):
    """
    Loads raw sensor data files from a trial directory and organizes them by sensor type.

    Args:
        trial_path (str): Path to the trial folder.

    Returns:
        dict: A dictionary where keys are sensor types ("HE", "LB", "RF", "LF")
              and values are pandas DataFrames with the corresponding sensor data.
    """
    raw_data = {}
    sensor_types = ["HE", "LB", "RF", "LF"]

    for sensor in sensor_types:
        # Look for a file ending with the current sensor type
        file_name = next((file for file in os.listdir(trial_path) if file.endswith(f"_{sensor}.txt")), None)
        if file_name:
            file_path = os.path.join(trial_path, file_name)
            raw_data[sensor] = pd.read_csv(file_path, sep='\t')
        else:
            raw_data[sensor] = None

    if None in raw_data:
        missing_sensors = [sensor for sensor, data in raw_data.items() if data is None]
        raise ValueError(f"Missing data for sensors: {', '.join(missing_sensors)}")

    return raw_data


def load_data_processed(trial_path):
    """
    Loads the processed sensor data file from a trial directory.

    Args:
        trial_path (str): Path to the trial folder.

    Returns:
        pandas.DataFrame: The processed sensor data.
    """
    processed_file = None
    for file in os.listdir(trial_path):
        if "processed" in file:
            processed_file = os.path.join(trial_path, file)
            break

    if not processed_file:
        raise ValueError(f"No processed sensor data file found in {trial_path}")

    return pd.read_csv(processed_file, sep='\t')


def load_metadata(trial_path):
    """
    Loads the metadata file from a trial directory.

    Args:
        trial_path (str): Path to the trial folder.

    Returns:
        dict: A dictionary containing metadata.
    """
    metadata_file = None
    for file in os.listdir(trial_path):
        if "meta" in file:
            metadata_file = os.path.join(trial_path, file)
            break

    if not metadata_file:
        raise ValueError(f"No metadata file found in {trial_path}")

    with open(metadata_file, 'r') as f:
        metadata = json.load(f)

    return metadata

