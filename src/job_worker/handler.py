"""
Handler for the job worker Lambda function.
"""

# --- IMPORTS ---
from worker import process_job

import json


# --- TYPES ---
from typing import Any
from typing import Dict


# --- CODE ---
def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    """
    Handler function for the job worker Lambda function.

    :param event: The event data from SQS.
    :param context: The Lambda execution context.

    :return: None
    """

    # interate over all messages in the SQS event
    for record in event['Records']:

        # parse the message body as JSON and extract the job ID
        try:
            message = json.loads(record['body'])

        # invalid JSON body: log an error and skip the message
        except json.JSONDecodeError:
            print(f'[worker] invalid JSON in message {record["messageId"]}: '
                  f'{record["body"]}')
            continue

        # extract the job ID
        job_id = message['job_id']

        # log the start of job processing
        print(f'[worker] processing job {job_id}')

        # process the job
        try:
            process_job(message)

        # any error occurs during job processing: log the error and re-raise it
        except Exception as e:
            print(f'[worker] job {job_id} failed — {e}')
            raise
