import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import patches


def plot_segmentation_gait_events(trial):
    """Plot the final figure for step detection and save the fig in the output folder as png file.

    Parameters
    ----------
    trial {dict} -- dictionary with the trial data
        trial["metadata"] {dict} -- dictionary with the metadata from which are constructed :
            - gait_events {dictionary} -- dictionary with the detected gait events
            - seg {dict} -- dictionary with 4 segmentation limits ('gait start', 'uturn start', 'uturn end', 'gait end')
            - freq {int} -- acquisition frequency
        trial["data"] {dict} -- dictionary with pandas dataframe with raw data from the sensors

    """

    gait_events = {"LF": trial["metadata"]["leftGaitEvents"],
                   "RF": trial["metadata"]["rightGaitEvents"]}
    seg = {"gait start": min(np.min(trial["metadata"]["leftGaitEvents"]), np.min(trial["metadata"]["rightGaitEvents"])),
           "uturn start": trial["metadata"]["uturnBoundaries"][0],
           "uturn end": trial["metadata"]["uturnBoundaries"][1],
           "gait end": max(np.max(trial["metadata"]["leftGaitEvents"]), np.max(trial["metadata"]["rightGaitEvents"]))}
    freq = trial["metadata"]["freq"]

    data = trial["data_processed"]

    name = "Gait events detection - "

    fig, ax = plt.subplots(3, figsize=(20, 9), sharex=True, sharey=False, gridspec_kw={'height_ratios': [10, 1, 10]})

    ax[0].grid()
    ax[2].grid()

    # Phases segmentation
    # Phase 0: waiting
    ax[1].add_patch(patches.Rectangle((0, 0),  # (x,y)
                                      seg['gait start'] / freq,  # width
                                      1,  # height
                                      alpha=0.1, color="k"))
    ax[1].text(seg['gait start'] / (2 * freq), 0.5, 'waiting', fontsize=9, horizontalalignment='center',
               verticalalignment='center')

    # Phase 1: go
    ax[1].add_patch(patches.Rectangle((seg['gait start'] / freq, 0),  # (x,y)
                                      (seg['uturn start'] - seg['gait start']) / freq,  # width
                                      1,  # height
                                      alpha=0.2, color="k"))
    ax[1].text(seg['gait start'] / freq + (seg['uturn start'] - seg['gait start']) / (2 * freq), 0.5, 'straight (go)',
               fontsize=9,
               horizontalalignment='center', verticalalignment='center')

    # Phase 2: uturn
    ax[1].add_patch(patches.Rectangle((seg['uturn start'] / freq, 0),  # (x,y)
                                      (seg['uturn end'] - seg['uturn start']) / freq,  # width
                                      1,  # height
                                      alpha=0.3, color="k"))
    ax[1].text(seg['uturn start'] / freq + (seg['uturn end'] - seg['uturn start']) / (2 * freq), 0.5, 'uturn',
               fontsize=9,
               horizontalalignment='center', verticalalignment='center')

    # Phase 3: back
    ax[1].add_patch(patches.Rectangle((seg['uturn end'] / freq, 0),  # (x,y)
                                      (seg['gait end'] - seg['uturn end']) / freq,  # width
                                      1,  # height
                                      alpha=0.2, color="k"))
    ax[1].text(seg['uturn end'] / freq + (seg['gait end'] - seg['uturn end']) / (2 * freq), 0.5, 'straight (back)',
               fontsize=9,
               horizontalalignment='center', verticalalignment='center')

    # Phase 4: waiting
    ax[1].add_patch(patches.Rectangle((seg['gait end'] / freq, 0),  # (x,y)
                                      (len(data["PacketCounter"]) - seg['gait end']) / freq,  # width
                                      1,  # height
                                      alpha=0.1, color="k"))
    ax[1].text(seg['gait end'] / freq + (len(data["PacketCounter"]) - seg['gait end']) / (2 * freq), 0.5, 'waiting',
               fontsize=9,
               horizontalalignment='center', verticalalignment='center')

    ax[0].set(xlabel='Time (s)', ylabel='Angular velocity (rad/s)')
    ax[0].set_title(label=name + "Left Foot", weight='bold')
    ax[0].xaxis.set_tick_params(labelsize=12)
    ax[1].set(ylabel='Phases')
    ax[1].set_yticks([])
    ax[2].set(xlabel='Time (s)', ylabel='Angular velocity (rad/s)')
    ax[2].set_title(label=name + "Right Foot", weight='bold')
    ax[2].xaxis.set_tick_params(labelsize=12)

    # ----------------------- Feet -------------------------------------------
    t_sensor = data["PacketCounter"] / freq
    for sensor in ["RF", "LF"]:
        gyr_sensor = data[sensor + "_Gyr_Y"]
        if sensor == "LF":
            ax[0].plot(t_sensor, gyr_sensor)
            n_ax = 0
        else:
            ax[2].plot(t_sensor, gyr_sensor)
            n_ax = 2
        ma_sensor = max(gyr_sensor)
        mi_sensor = min(gyr_sensor)
        for i in range(len(gait_events[sensor])):
            to = int(gait_events[sensor][i][0])
            ax[n_ax].vlines(t_sensor[to], mi_sensor, ma_sensor, 'k', '--')
            hs = int(gait_events[sensor][i][1])
            ax[n_ax].vlines(t_sensor[hs], mi_sensor, ma_sensor, 'k', '--')
            ax[n_ax].add_patch(patches.Rectangle((t_sensor[to], mi_sensor),  # (x,y)
                                                 t_sensor[hs] - t_sensor[to],  # width
                                                 ma_sensor - mi_sensor,  # height
                                                 alpha=0.1,
                                                 facecolor='red', linestyle='dotted'))
            if i < len(gait_events[sensor]) - 1:
                to_ap = int(gait_events[sensor][i + 1][0])
                ax[n_ax].add_patch(patches.Rectangle((t_sensor[hs], mi_sensor),  # (x,y)
                                                     t_sensor[to_ap] - t_sensor[hs],  # width
                                                     ma_sensor - mi_sensor,  # height
                                                     alpha=0.1,
                                                     facecolor='green', linestyle='dotted'))

    # legend
    red_patch = mpatches.Patch(color='red', alpha=0.1, label='swing')
    green_patch = mpatches.Patch(color='green', alpha=0.1, label='stance')

    ax[0].legend(handles=[red_patch, green_patch], loc="upper left")
    ax[2].legend(handles=[red_patch, green_patch], loc="upper left")

    plt.show()


def plot_segmentation(trial):
    """Plot the uturn detection as a .png figure.

    Parameters
    ----------
    trial {dict} -- dictionary with the trial data
        trial["metadata"] {dict} -- dictionary with the metadata from which are extracted :
            - uturnBoundaries {list} -- ['uturn start', 'uturn end']
            - freq {int} -- acquisition frequency
        trial["data"] {dict} -- dictionary with pandas dataframe with raw data from the sensors

    """

    sensor = "LB"  # sensor to plot
    data = trial["data_processed"]
    freq = trial["metadata"]["freq"]
    seg = {"uturn start": trial["metadata"]["uturnBoundaries"][0],
           "uturn end": trial["metadata"]["uturnBoundaries"][1]}

    # data
    t = data["PacketCounter"]
    angle = (np.cumsum(data[sensor + "_Gyr_X"]) - np.cumsum(data[sensor + "_Gyr_X"])[0]) / freq
    angle = angle * 360 / (2 * np.pi)  # in degrees

    # fig initialization
    fig, ax = plt.subplots(2, figsize=(20, 8), sharex=True, sharey=False, gridspec_kw={'height_ratios': [20, 1]})
    ax[0].grid()
    ax[0].plot(t / freq, angle)
    ax[0].set_ylabel('Angular position (°)', fontsize=15)
    ax[0].set_title("uturn detection", fontsize=15, weight='bold')
    ax[0].set_xlabel('Time (s)', fontsize=15)

    # min and max
    mi = np.min(angle) - 0.05 * (np.max(angle) - np.min(angle))
    ma = np.max(angle) + 0.05 * (np.max(angle) - np.min(angle))

    # phases segmentation
    # Phase 1: go
    ax[0].add_patch(patches.Rectangle((0, mi),  # (x,y)
                                      seg['uturn start'] / freq,  # width
                                      ma - mi,  # height
                                      alpha=0.2, color="k"))
    ax[1].add_patch(patches.Rectangle((0, 0),  # (x,y)
                                      seg['uturn start'] / freq,  # width
                                      1,  # height
                                      alpha=0.2, color="k"))
    ax[1].text(seg['uturn start'] / (2 * freq), 0.5, 'straight (go)',
               fontsize=9,
               horizontalalignment='center', verticalalignment='center')

    # Phase 2: uturn
    ax[0].vlines(seg['uturn start'] / freq, mi, ma, 'black', '--', linewidth=3, label="uturn boundaries")
    ax[0].add_patch(patches.Rectangle((seg['uturn start'] / freq, mi),  # (x,y)
                                      (seg['uturn end'] - seg['uturn start']) / freq,  # width
                                      ma - mi,  # height
                                      alpha=0.3, color="k"))
    ax[1].add_patch(patches.Rectangle((seg['uturn start'] / freq, 0),  # (x,y)
                                      (seg['uturn end'] - seg['uturn start']) / freq,  # width
                                      1,  # height
                                      alpha=0.3, color="k"))
    ax[1].text(seg['uturn start'] / freq + (seg['uturn end'] - seg['uturn start']) / (2 * freq), 0.5, 'uturn',
               fontsize=9,
               horizontalalignment='center', verticalalignment='center')

    # Phase 3: back
    ax[0].vlines(seg['uturn end'] / freq, mi, ma, 'black', '--', linewidth=3)
    ax[0].add_patch(patches.Rectangle((seg['uturn end'] / freq, mi),  # (x,y)
                                      ((len(t) - 1) - seg['uturn end']) / freq,  # width
                                      ma - mi,  # height
                                      alpha=0.2, color="k"))
    ax[1].add_patch(patches.Rectangle((seg['uturn end'] / freq, 0),  # (x,y)
                                      ((len(t) - 1) - seg['uturn end']) / freq,  # width
                                      1,  # height
                                      alpha=0.2, color="k"))
    ax[1].text(seg['uturn end'] / freq + ((len(t) - 1) - seg['uturn end']) / (2 * freq), 0.5, 'straight (back)',
               fontsize=9,
               horizontalalignment='center', verticalalignment='center')

    ax[0].legend(loc="upper right")

    ax[1].set(ylabel='Phases')
    ax[1].set_yticks([])

    plt.show()
