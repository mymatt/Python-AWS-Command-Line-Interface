#!/usr/bin/python

# list ec2 instances in current region
# stop ec2 instances
# start ec2 instances
# add tags
# restrict access via tag
# release unattached elastic IPs

# backup image, add tag remove:false
# remove image based on remove:true
# cron job

import boto3
import click

from ec2Manager import ec2Manager

session = None
ec2_manager = None


@click.group()
@click.option('--profile', default='ec2play', help='AWS Profile')
def cli(profile):
    global session, ec2_manager
    # if profile not set, AWS looks for environmental variables
    session = boto3.Session(profile_name=profile)
    ec2_manager = ec2Manager(session)

@cli.command('list-instances')
@click.argument('TagKey')
@click.argument('TagValue')
def list_instances(TagKey, TagValue):
    """List ec2 Instances by tag"""
    ec2_manager.list_instances(TagKey, TagValue)

@cli.command('stop-instances')
@click.option('--tag', default='', help='Tag Group of EC2 Instance')
def stop_instances(tag):
    """Stop running ec2 Instances of current region"""
    ec2_manager.stop_instances(tag)


@cli.command('start-instances')
@click.option('--tag', default='', help='Tag Group of EC2 Instance')
def start_instances(tag):
    """Start ec2 Instances of current region"""
    ec2_manager.start_instances(tag)


@cli.command('backup-instances')
def backup_instances():
    """Backup Instances with Tag:Backup"""
    ec2_manager.backup_instances()


@cli.command('cleanup-backups')
def cleanup_backups():
    """Delete Expired Backup Instances"""
    ec2_manager.cleanup_backups()
