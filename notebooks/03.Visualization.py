from numpy import True_
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle("../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------

set_df = df[df["set"] == 1]
plt.plot(set_df["acc_x"])
plt.plot(set_df["acc_x"].reset_index(drop=True))

# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------

for label in df.label.unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()

for label in df.label.unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()


# --------------------------------------------------------------
# Adjust plot settings rcParams (globally) and style (locally)
# --------------------------------------------------------------

mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------

category_df = df.query("label == 'squat' and participant == 'A'").reset_index()
category_df = df.query("label == 'squat'").query("participant == 'A'").reset_index()

fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_ylabel = "acc_y"
ax.set_xlabel = "samples"
ax.legend()

# We see that in medium sets the participant is accelerateing faster


# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------

# We want the model to be able to generalize

participant_df = df.query("label == 'bench'").sort_values(by="participant").reset_index()
fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel = "acc_y"
ax.set_xlabel = "samples"
ax.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------

label = "squat"
participant = "A"

all_axes_df = df.query(f"label == '{label}' and participant == '{participant}'").reset_index()

# tha same as above

all_axes_df1 = df[(df["label"] == label) & (df["participant"] == participant)].reset_index()

fig, ax = plt.subplots()
all_axes_df[["acc_x", "acc_y", "acc_z"]].plot()
ax.set_ylabel = "acc_y"
ax.set_xlabel = "samples"
ax.legend()


# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------

labels = df.label.unique()
participants = df.participant.unique()

for label in labels:
    for participant in participants:
        all_axes_df = df[(df["label"] == label) & (df["participant"] == participant)].reset_index()

        if all_axes_df.shape[0] != 0:
            fig, ax = plt.subplots()
            all_axes_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
            ax.set_ylabel("acc_y")
            ax.set_xlabel("samples")
            ax.set_title(f"{label} - {participant}")
            ax.legend()


for label in labels:
    for participant in participants:
        all_axes_df = df[(df["label"] == label) & (df["participant"] == participant)].reset_index()

        if all_axes_df.shape[0] != 0:
            fig, ax = plt.subplots()
            all_axes_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax)
            ax.set_ylabel("gyr_y")
            ax.set_xlabel("samples")
            ax.set_title(f"{label} - {participant}")
            ax.legend()


# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------

label = "row"
participant = "A"
combined_df = df[(df["label"] == label) & (df["participant"] == participant)].reset_index()

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
combined_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
combined_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
ax[1].set_xlabel("samples")

# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------

labels = df.label.unique()
participants = df.participant.unique()

for label in labels:
    for participant in participants:
        combined_plot_df = df[(df["label"] == label) & (df["participant"] == participant)].reset_index()

        if combined_plot_df.shape[0] != 0:
            fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
            combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
            combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

            ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
            ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True)
            ax[1].set_xlabel("samples")

            plt.savefig(f"../reports/figures/{label.title()}_({participant}).png")

            # plt.show()
