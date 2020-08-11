import json
from rezume import Rezume


def render(rezume: Rezume):
    """Returns a JSON string as the rendered representation of provided rezume.
    """
    data = rezume.dump_data()
    return json.dumps(data)
