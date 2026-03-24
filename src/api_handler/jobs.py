"""
Job management API handler.
"""

# --- IMPORTS ---
from clients import SQS
from clients import JOBS_TABLE
from clients import JOBS_QUEUE_URL
from datetime import datetime
from datetime import timezone
from utils import response

import json
import uuid


# --- TYPES ---
from models import JobItem
from typing import Any
from typing import Dict
from typing import Optional


# --- CODE ---
def create_job(body: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new job.

    :param body: The request body containing the job details.

    :return: A response dictionary to be returned to API Gateway.
    """

    # generate a unique job ID and get the current timestamp
    job_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    # create a job item with status "pending"
    item: JobItem = {
        'job_id': job_id,
        'status': 'pending',
        'payload': body,
        'result_url': None,
        'created_at': now,
        'updated_at': now,
    }

    # store the job item in the DynamoDB
    JOBS_TABLE.put_item(Item=item)

    # send a message to the SQS queue to trigger the job processing
    SQS.send_message(
        QueueUrl=JOBS_QUEUE_URL,
        MessageBody=json.dumps({'job_id': job_id, 'payload': body}),
    )

    # return the job ID and initial status to the client
    return response(202, {'job_id': job_id, 'status': 'pending'})


def get_job(job_id: str) -> Dict[str, Any]:
    """
    Retrieves the status of a job.

    :param job_id: The ID of the job to retrieve.

    :return: A response dictionary to be returned to API Gateway.
    """

    # query the DynamoDB for the job item
    result: Optional[JobItem] = JOBS_TABLE.get_item(Key={'job_id': job_id})

    # check if the job item exists
    item = result.get('Item')

    # job not found: return a 404 response
    if item is None:
        return response(404, {'error': 'job not found'})

    # return the job status and details to the client
    return response(200, {
        'job_id': item['job_id'],
        'status': item['status'],
        'result_url': item.get('result_url'),
        'created_at': item['created_at'],
        'updated_at': item['updated_at'],
    })
