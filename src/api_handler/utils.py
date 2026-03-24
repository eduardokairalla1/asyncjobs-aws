"""
Utility functions for the API handler.
"""

# --- IMPORTS ---
import json


# --- TYPES ---
from typing import Any
from typing import Dict


# --- CODE ---
def response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a standardized API response.

    :param status_code: The HTTP status code.
    :param body: The response body.

    :return: A dictionary representing the API response.
    """
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body),
    }
