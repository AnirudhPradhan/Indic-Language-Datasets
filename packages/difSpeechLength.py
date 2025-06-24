import re

def compute_actual_speech(text):
    """
    Compute the actual speech duration from the 'Speaker Distribution' field.
    Returns 0.0 if data is missing/invalid.
    """
    try:
        # Handle empty input or non-strings
        if not text or not isinstance(text, str):
            return 0.0
        
        # Extract speaker durations
        matches = re.findall(r"\('([^']+)',\s*([0-9.]+)\)", text)
        total_duration = sum(round(float(tup[1]), 2) for tup in matches)
        return round(total_duration, 2)
    
    except Exception as e:
        print(f"Error computing speech: {e}")  # Removed reference to undefined `row`
        return 0.0
