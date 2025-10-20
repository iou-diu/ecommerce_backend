

def validate_required_fields(required_fields, data):
    missing_fields = [field for field in required_fields if field not in data or data[field] is None]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, None