#!/usr/bin/python

import boto3
import click

from s3.bucket import BucketAdmin

session = None
bucket_admin = None
