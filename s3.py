#!/usr/bin/python

import boto3
import click

from bucket import BucketAdmin

session = None
bucket_admin = None

@click.group()
@click.option('--profile', default='s3play', help='AWS Profile')
def cli(profile):

    global session, bucket_admin

    # if profile not set, AWS looks for environmental variables
    session = boto3.Session(profile_name=profile)
    # s3 = session.resource('s3')
    bucket_admin = BucketAdmin(session)


@cli.command('create-bucket')
@click.argument('bucket')
def create_bucket(bucket):
    """Create bucket."""
    bucket_admin.setup_bucket(bucket)
