"""
Global clients and resources for the job worker.
"""

# --- IMPORTS ---
import boto3
import os


# --- CONSTANTS & DEFINITIONS ---
DYNAMO_DB = boto3.resource('dynamodb')
JOBS_TABLE = DYNAMO_DB.Table(os.environ['JOBS_TABLE'])
RESULTS_BUCKET = os.environ['RESULTS_BUCKET']
S3 = boto3.client('s3')
