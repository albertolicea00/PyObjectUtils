
def clean_dict(
    data, required_fields=None, optional_fields=None, exception=False, nested=True
):
    """
    Clean a dictionary by removing keys with empty values (None, [], ""). Recursively clean nested dictionaries and lists
    if `nested` is set to True. Raise an exception if a required field is missing or has an empty value, unless `exception` is set to False.

    Args:
        data (dict): The dictionary to be cleaned.
        required_fields (list, optional): A list of keys that are required. Defaults to all keys.
        optional_fields (list, optional): A list of keys that are optional. Defaults to empty.
        exception (bool, optional): If True, raises an error for empty required fields; if False, removes them.
        nested (bool, optional): If True, recursively clean nested dictionaries and lists; if False, skip nested cleaning.

    Returns:
        dict: The cleaned dictionary.

    Raises:
        ValueError: If a required field is missing or has an empty value, and `exception` is True.

    Example 1: Define required_fields
        >>> clean_dict(data, required_fields=["name", "email"])
    Example 2: Do not pass required_fields (all fields are considered required)
        >>> clean_dict(data)
    Example 3: Pass empty required_fields (no fields are considered required)
        >>> clean_dict(data, required_fields=[])
    Example 4: Define optional_fields, when there are more required than optional fields
        >>> clean_dict(data, optional_fields=["company"])
    Example 5: Use exception=False to remove required fields with empty values instead of raising an error
        >>> clean_dict(data, required_fields=["name", "email"], exception=False)
    """
    if required_fields is None:
        # If no required_fields provided, consider all fields as required except those marked optional
        required_fields = [
            key
            for key in data.keys()
            if not (optional_fields and key in optional_fields)
        ]

    cleaned_data = {}

    for key, value in data.items():
        if key in required_fields:
            # If nested cleaning is enabled and the value is a dictionary, clean it recursively
            if nested and isinstance(value, dict):
                nested_cleaned = clean_dict(
                    value,
                    required_fields=None,
                    optional_fields=None,
                    exception=exception,
                    nested=nested,
                )
                if not nested_cleaned:
                    if not exception:
                        continue  # Skip adding the key if exception is False
                    raise ValueError(
                        f"Required nested field '{key}' is empty after cleaning."
                    )
                cleaned_data[key] = nested_cleaned
            # If nested cleaning is enabled and the value is a list, clean it recursively
            elif nested and isinstance(value, list):
                cleaned_list = [
                    (
                        clean_dict(item, exception=exception, nested=nested)
                        if isinstance(item, dict)
                        else item
                    )
                    for item in value
                    if item not in (None, [], "")
                ]
                cleaned_list = [
                    item for item in cleaned_list if item
                ]  # Remove empty items
                if cleaned_list:
                    cleaned_data[key] = cleaned_list
                elif exception:
                    raise ValueError(f"Required field '{key}' has an empty list.")
            elif value in (None, [], ""):
                if not exception:
                    continue  # Skip adding the key if exception is False
                raise ValueError(
                    f"Required field '{key}' is missing or has an empty value."
                )
            else:
                cleaned_data[key] = value
        else:
            # Handle non-required fields
            if nested and isinstance(value, dict):
                nested_cleaned = clean_dict(
                    value,
                    required_fields=None,
                    optional_fields=None,
                    exception=exception,
                    nested=nested,
                )
                if nested_cleaned:
                    cleaned_data[key] = nested_cleaned
            elif nested and isinstance(value, list):
                cleaned_list = [
                    (
                        clean_dict(item, exception=exception, nested=nested)
                        if isinstance(item, dict)
                        else item
                    )
                    for item in value
                    if item not in (None, [], "")
                ]
                cleaned_list = [item for item in cleaned_list if item]
                if cleaned_list:
                    cleaned_data[key] = cleaned_list
            elif value not in (None, [], ""):
                cleaned_data[key] = value

    return cleaned_data
