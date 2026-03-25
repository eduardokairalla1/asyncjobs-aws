"""
Define types used in the API handler.
"""

# --- TYPES ---
from typing import Any
from typing import Optional
from typing import TypedDict


# --- CODE ---
class JobItem(TypedDict):
    """
    Type definition for a job item in DynamoDB.
    """
    job_id: str
    status: str
    payload: dict[str, Any]
    result_url: Optional[str]
    created_at: str
    updated_at: str
