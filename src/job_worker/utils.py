"""
Utility functions for the job worker.
"""

# --- IMPORTS ---
from datetime import datetime
from datetime import timezone

import random


# --- TYPES ---
from typing import Any
from typing import Dict


# --- CODE ---
def generate_report(job_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a report based on the job ID and payload.

    NOTE: This is a placeholder function that simulates report generation.
    In a real application, this would contain the actual logic to process the
    payload and generate the desired report.

    :param job_id: The ID of the job.
    :param payload: The payload containing the job data.

    :return: A dictionary containing the generated report.
    """
    return {
        'report_id': job_id,
        'type': payload.get('type'),
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'summary': {
            'total_sales': round(random.uniform(10000, 99999), 2),
            'transactions': random.randint(50, 500),
            'top_region': random.choice(['south', 'north', 'east', 'west']),
            'period': payload.get('data', {}).get('period', 'unknown'),
        },
    }
