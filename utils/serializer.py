from datetime import datetime, date

def serialize(data):

    if isinstance(data, dict):
        return {
            k: serialize(v)
            for k, v in data.items()
        }

    if isinstance(data, list):
        return [serialize(v) for v in data]

    if isinstance(data, (datetime, date)):
        return data.isoformat()

    return data