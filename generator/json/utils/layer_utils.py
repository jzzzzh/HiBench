def get_available_layers(scenario: str):
    """Get available layers for each scenario"""
    layers = {
        "university_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_structure_medium_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_structure_medium_2": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_structure_large_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_structure_large_2": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_bullshit_structure_small": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_bullshit_structure_medium_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_bullshit_structure_medium_2": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        },
        "university_bullshit_structure_large_1": {
            "layers": [0, 1, 2, 3, 4, 5],
            "names": ["Faculty", "Department", "Program", "Course", "Lecturer", "Student"]
        },
        "university_bullshit_structure_large_2": {
            "layers": [0, 1, 2],
            "names": ["Faculty", "Department", "Program"]
        }
    }
    return layers.get(scenario) 