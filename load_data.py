import json

def load_employee_data():
    """Load employee data from a JSON file."""
    # load json formatted employee data
    with open("employees_data.json", "r") as f:
        return json.load(f)
