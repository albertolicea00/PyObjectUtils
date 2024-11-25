# serializers.py
This module provides functions to convert Python objects to dictionaries, omitting specified attributes and applying custom modifications to the keys and attribute values.

# ⚡How to Use 
To use the functions provided in this module, follow these steps:

1. Copy all the content of this module into your project's **helper** or **utility** functions folder. This will ensure that you have access to the necessary functions and enumerations. 

2. Import the functions and enumerations according to the needs of your project. For example:
```python
from your_project.helpers import object_to_dict, object_list_to_dict, GenericModificationTypes
```
**NOTE**: 
 You can merge all our code into one single file if necessary or also change files name (with prefix `serializer__...`) for better importing

# 🚀 Features

For more upcoming features, please refer to the [issue tab](https://github.com/albertolicea00/serializers.py/issues).

## 📜 Enumerations

#### `GenericModificationTypes`
This enumeration defines several utility tuples for modifications. Each tuple contains:
1. **Condition**: A string representing the condition to check.
2. **Function**: A function to execute if the condition is met.
3. **Import Statement**: A string containing the necessary import statement for the modification.

**Available Values**:
- **DATETIME_TO_STRING**: Converts `datetime` objects to ISO format strings.
- **STRIP_WHITESPACE**: Strips leading and trailing whitespace from strings.
- **TO_UPPERCASE**: Converts strings to uppercase.
- **TO_LOWERCASE**: Converts strings to lowercase.
- **ROUND_FLOAT**: Rounds float values to two decimal places.

## 🛠️ Functions

- **object_to_dict**: Converts a Python object to a dictionary, omitting specified attributes and handling nested objects.
- **object_list_to_dict**: Convert a list of Python objects to a list of dictionaries, omitting specified attributes from each object.

### Parameters
1. attributes_to_omit:

    - **Purpose**: This parameter is used to exclude certain attributes from each object that are not of interest. This is particularly useful for models in Django, Flask, and other frameworks that create internal attributes for their functionality.

    - **Usage**: Pass a set or list of attribute names you want to omit from the dictionary representation.

Example: attributes_to_omit = {"_sa_instance_state", "config", "gateway"}

1. modifications:

   - **Purpose**: This parameter is used to convert some data that comes in a non-JSON format, such as datetime, to a JSON-compatible format.

   - **Usage**: Pass a list of tuples where each tuple contains:

       a. Condition: A string representing the condition to check.

       b. Function: A function to execute if the condition is met.

       c. Module: A string representing the module to import for the condition or function.

   - Example
    ```python
    modifications = [
        ("isinstance(value, datetime)", lambda x: x.isoformat(), "from datetime import datetime"),
        ("isinstance(value, str)", lambda x: x.strip(), "")
    ]
    ```


## 🔩 Creating Modification Tuples
- **Condition**: The first element of the tuple is a string that represents the condition to check. This condition is evaluated using the eval function.

- **Function**: The second element is a function that modifies the value if the condition is met.

- Module: The third element is a string that contains the import statement for any required modules. If more modules are needed, they can be imported within the function, but this will not affect the condition.

### Modification-function Parameters
- **key**: The attribute name being processed.

- **value**: The attribute value being processed.

- **seen** (BETA): A set to keep track of already processed objects to prevent infinite recursion.

- **attributes_to_omit** (BETA): The set or list of attribute names to omit from the dictionary.

- **dictionary** (BETA): The dictionary being constructed.

- **obj_id** (BETA): The ID of the object being processed.

These parameters can be used within the modification functions to create more complex conditions and modifications.

## 📘 Example Usage
```python
customer = Customer()  # Assuming Customer is a defined class with attributes
attributes_to_omit = {"_sa_instance_state", "config", "gateway"}
modifications = [
    ("isinstance(value, datetime)", lambda x: x.isoformat(), "from datetime import datetime"),
    ("isinstance(value, str)", lambda x: x.strip(), "")
]
customer_dict = object_to_dict(customer, attributes_to_omit=attributes_to_omit, modifications=modifications)
```

This example demonstrates how to use the `attributes_to_omit` and `modifications` parameters to customize the conversion of a Python object to a dictionary. The `attributes_to_omit` parameter excludes specified attributes, while the `modifications` parameter applies custom transformations to the attribute values.


