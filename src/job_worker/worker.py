"""
Worker module for processing jobs from the SQS queue.
"""

# --- IMPORTS ---
from utils import generate_report
from utils import upload_to_s3
from utils import update_status

import time


# --- TYPES ---
from typing import Any
from typing import Dict


# --- CODE ---
def process_job(message: Dict[str, Any]) -> None:
    """
    Process a job message.

    :param message: The job message containing the job ID and payload.

    :return: None
    """

    # extract the job ID and payload from the message
    job_id = message['job_id']
    payload = message['payload']

    # log the start of job processing
    print(f'[worker] processing job {job_id}')

    # update the job status to 'processing'
    update_status(job_id, 'processing')

    # simulate a long-running job by sleeping for a few seconds
    time.sleep(3)

    # generate the report based on the payload
    result = generate_report(job_id, payload)

    # upload the result to S3 and get the presigned URL
    result_url = upload_to_s3(job_id, result)

    # update the job status to 'done' and store the result URL
    update_status(job_id, 'done', result_url=result_url)

    # log the completion of job processing
    print(f'[worker] job {job_id} completed — {result_url}')
