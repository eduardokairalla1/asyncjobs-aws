"""
Global clients and resources for the API handler.
"""

# --- IMPORTS ---
import boto3
import os


# --- CONSTANTS & DEFINITIONS ---
DYNAMO_DB = boto3.resource('dynamodb')
JOBS_TABLE = DYNAMO_DB.Table(os.environ['JOBS_TABLE'])
JOBS_QUEUE_URL = os.environ['JOBS_QUEUE_URL']
SQS = boto3.client('sqs')
