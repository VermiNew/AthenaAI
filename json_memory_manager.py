import json


def storeMemoryJson(file_path, key, value, logger):
    """
    Saves or updates a key-value pair in a JSON file. If the key already exists, its value is updated;
    otherwise, the key-value pair is added to the file.

    Parameters:
    - file_path (str): The path to the JSON file.
    - key (str): The key to save or update in the file.
    - value: The value associated with the key.
    """
    try:
        # Try to load the existing JSON data
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        # Update the data with the new key-value pair
        data[key] = value

        # Write the updated data back to the JSON file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

        logger.info(f"Data saved successfully: {key}: {value}")
    except json.JSONDecodeError:
        logger.error("Error reading the JSON file. Please ensure it contains valid JSON.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
