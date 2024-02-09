import json

def parse_jsons(text):
    """Parse all JSON objects from a given text and return them as a list."""
    json_objects = []
    start_index = text.find('{')  # Znajdź pierwszy znak '{'
    while start_index != -1:  # Dopóki znajdujemy znak '{'
        end_index = text.find('}', start_index) + 1  # Znajdź odpowiadający mu znak '}' i dodaj 1, aby uwzględnić ten znak
        if end_index != -1:
            try:
                json_str = text[start_index:end_index]  # Wyodrębnij string JSON
                json_obj = json.loads(json_str)  # Przekonwertuj string na obiekt JSON
                json_objects.append(json_obj)  # Dodaj obiekt do listy
                start_index = text.find('{', end_index)  # Szukaj kolejnego '{'
            except json.JSONDecodeError:
                start_index = text.find('{', start_index + 1)  # W przypadku błędu, kontynuuj szukanie
                json_objects.append({})  # Dodaj pusty słownik do listy w przypadku błędu
        else:
            break  # Jeśli nie ma więcej '}', zakończ pętlę

    return json_objects

def combine_json_objects(json_objects, selected_fields=None):
    """Combine fields from a list of JSON objects into a single JSON object."""
    selected_fields = selected_fields or ["content", "type"]
    combined = {field: [] for field in selected_fields}
    
    for obj in json_objects:
        for key, value in obj.items():
            if key in selected_fields:
                combined[key].append(value)
    return combined

def extract_from_json(json_data, key):
    """Extract values for a specified key from JSON data."""
    if key in json_data:
        return json_data[key]
    else:
        raise ValueError(f"Key '{key}' does not exist in the provided JSON data.")

def remove_word_from_list(word_list, word_to_remove):
    """Remove a specific word from a list."""
    return [word for word in word_list if word != word_to_remove]
