import pandas as pd
from glob import glob
import re

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------


# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------


# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------


# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------


# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------


# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------

data_path = "../../data/raw/MetaMotion\\"
files = glob("../../data/raw/MetaMotion/*.csv")


def read_datea_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for f in files:
        participant = f.split("-")[0].replace(data_path, "")
        label = f.split("-")[1]
        category = f.split("-")[2]
        category = re.sub(r"\d+", "", category).split("_")[0]

        df = pd.read_csv(f)
        df[["participant", "label", "category"]] = participant, label, category

        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_df = acc_df.append(df)
            acc_set += 1
        elif "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_df = gyr_df.append(df)
            gyr_set += 1

    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    acc_df.drop(["epoch (ms)", "time (01:00)", "elapsed (s)"], axis=1, inplace=True)
    gyr_df.drop(["epoch (ms)", "time (01:00)", "elapsed (s)"], axis=1, inplace=True)
    return acc_df, gyr_df


if __name__ == "__main__":
    acc_df, gyr_df = read_datea_from_files(files)

data_merged = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)

data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "participant",
    "label",
    "category",
    "set",
]
sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "label": "last",
    "category": "last",
    "participant": "last",
    "set": "last",
}

days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat(
    [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
)

data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
