import json

def convert_response(data):
    """Convert data to the same JSON format"""
    data = json.loads(data)
    data = json.dumps(data)
    return data