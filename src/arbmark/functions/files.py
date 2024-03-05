# Glob for Unix style pathname pattern expansion.
import glob

# OS for interacting with the operating system
import os

# Dapla for cloud file client
from dapla import FileClient


def read_latest(path: str, name: str, dottype: str = ".parquet") -> str | None:
    """Finds the latest version of a specified file in a given directory and returns its name.

    This function searches for files in the specified path that match the given name and file
    type, sorts them by modification time, and returns the path of the latest version. If no
    files are found, it returns None.

    Args:
        path (str): The directory path where the files are located.
        name (str): The base name of the files to search for.
        dottype (str): The file extension to look for. Defaults to ".parquet".

    Returns:
        Optional[str]: The path of the latest version of the file if found, None otherwise.
    """
    # Inform the user about the file versions being checked
    print(f"Checking versions of file: {name}")

    # Define the pattern to search for files based on the provided name and file type
    file_name_pattern = f"{name}*{dottype}"

    # Join directory and file name
    file_path = os.path.join(path, file_name_pattern)

    # If path is a google cloud bucket
    if path[:4] in ["ssb-", "gs:/"]:

        # Get filesystem
        fs = FileClient.get_gcs_file_system()

        # Use glob to find all files matching the pattern
        file_list = fs.glob(file_path)

    else:

        # Use glob to find all files matching the pattern
        file_list = glob.glob(file_path)

    # Sorting key based on file version
    file_versions = sorted(
        file_list,
        key=lambda x: int(x.split("_v")[-1].split(".")[0]),
    )

    # Check if any files were found. If not, inform the user and return None
    if not file_versions:
        print("No files found.")
        return None

    # Select the last file from the sorted list as it is the most recently modified one
    latest_file = os.path.normpath(file_versions[-1])

    # Extract the name of the latest file for reporting.
    latest_file_name = os.path.basename(latest_file)

    # Inform the user about the number of versions found and the latest one being read
    print(f"Found {len(file_versions)} version(s).")
    print(f"Reading latest version: {latest_file_name}")

    # Return the path of the latest file
    return latest_file
