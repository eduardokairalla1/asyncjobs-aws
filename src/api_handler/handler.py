"""
API handler for job management.
"""

# --- IMPORTS ---
from jobs import create_job
from jobs import get_job
from utils import response

import json


# --- TYPES ---
from typing import Any
from typing import Dict


# --- CODE ---
def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Main entry point for the API Gateway.

    :param event: The event data from API Gateway.
    :param context: The Lambda execution context.

    :return: A response dictionary to be returned to API Gateway.
    """

    # extract HTTP method and path from the event
    method = event['httpMethod']
    path = event['path']

    # method is POST and the path is /jobs: create a new job
    if method == 'POST' and path == '/jobs':

        # parse the JSON body of the request
        try:
            body = json.loads(event['body'] or '{}')

        # invalid JSON body: return a 400 response
        except json.JSONDecodeError:
            return response(400, {'error': 'invalid JSON body'})

        # "payload" field is missing: return a 400 response
        if 'type' not in body:
            return response(400, {'error': 'field "type" is required'})

        # create the job and return the response
        return create_job(body)

    # method is GET and the path starts with /jobs/: get the status of a job
    if method == 'GET' and path.startswith('/jobs/'):

        # extract the job ID from the path parameters
        try:
            job_id = event['pathParameters']['id']

        # "id" parameter is missing: return a 400 response
        except KeyError:
            return response(400, {'error': 'parameter "id" is required'})

        # return the job status
        return get_job(job_id)

    # no route matches: return a 404 response
    return response(404, {'error': 'route not found'})
