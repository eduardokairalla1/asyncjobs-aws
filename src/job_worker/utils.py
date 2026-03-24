"""
Utility functions for the job worker.
"""

# --- IMPORTS ---
from clients import RESULTS_BUCKET
from clients import S3
from datetime import datetime
from datetime import timezone

import json
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


def upload_to_s3(job_id: str, result: Dict[str, Any]) -> str:
    """
    Upload the result to S3 and return the presigned URL.

    :param job_id: The ID of the job.
    :param result: The result to upload.

    :return: The presigned URL of the uploaded object.
    """

    # define the S3 object key based on the job ID
    key = f'jobs/{job_id}/result.json'

    # upload the result to S3 as a JSON file
    S3.put_object(
        Bucket=RESULTS_BUCKET,
        Key=key,
        Body=json.dumps(result),
        ContentType='application/json',
    )

    # generate a presigned URL for the uploaded object, valid for 1 hour
    presigned_url = S3.generate_presigned_url(
        'get_object',
        Params={'Bucket': RESULTS_BUCKET, 'Key': key},
        ExpiresIn=3600,
    )

    # return the presigned URL
    return presigned_url
