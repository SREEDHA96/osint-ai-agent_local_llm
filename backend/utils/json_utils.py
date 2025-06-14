import json
import re
from typing import List, Union, Optional

def extract_json(text: str, required_keys: Optional[List[str]] = None):

    """Attempt to parse and return a JSON object from a model response.

    Strips common prefixes and trailing code fences, then validates that all
    ``required_keys`` are present if provided.
    """
    text = text.strip()

    # Remove common prefixes like "Result:" that models sometimes include
    text = re.sub(r"^\s*Result:\s*", "", text, flags=re.IGNORECASE)

    # Strip surrounding code fences
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = text.rstrip("`")
        text = text.strip()
    # Handle trailing code fences even if no opening fence was detected
    text = re.sub(r"```$", "", text).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except json.JSONDecodeError:
                raise ValueError("Failed to parse JSON from response")
        else:
            raise ValueError("Failed to parse JSON from response")

    if required_keys and not all(k in data for k in required_keys):
        raise ValueError("Parsed JSON missing required keys")
    return data
