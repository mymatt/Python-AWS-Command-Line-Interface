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


@cli.command('upload-object')
@click.argument('bucket')
@click.argument('object')
@click.argument('key')
def upload_object(bucket, object, key):
    """Upload Object to bucket."""
    bucket_admin.create_object(bucket, object, key)


@cli.command('load-policy')
@click.argument('bucket')
def load_policy(bucket):
    """Load Policy to bucket."""
    bucket_admin.set_policy(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in bucket."""
    for obj in bucket_admin.objects_all(bucket):
        print(obj)
