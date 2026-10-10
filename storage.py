import json
import os


def load_data(filename):
    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Expected a JSON list.")

        return data

    except (json.JSONDecodeError, OSError, ValueError) as error:
        raise RuntimeError(
            f"Unable to load {filename}: {error}"
        ) from error


def save_data(filename, data):
    directory = os.path.dirname(filename)
    os.makedirs(directory, exist_ok=True)

    temporary_file = filename + ".tmp"

    try:
        with open(temporary_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        os.replace(temporary_file, filename)

    except OSError as error:
        if os.path.exists(temporary_file):
            try:
                os.remove(temporary_file)
            except OSError:
                pass

        raise RuntimeError(
            f"Unable to save {filename}: {error}"
        ) from error
