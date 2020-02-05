
from botocore.exceptions import ClientError

class ec2Manager:

    def __init__(self, session):
        self.ec2 = session.resource('ec2')
        self.current_region = session.region_name

    def stop_instances(self):
        """Stop all running ec2 instances"""
        # get only running instances
        instances = self.ec2.instances.filter(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running']
            }]
        )

        for inst in instances:
            inst.stop()
            print("Instance Stopped: {}".format(instance.id))

    def start_instances(self):
        """Start all stopped ec2 instances"""
        # get only stopped instances
        instances = self.ec2.instances.filter(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['stopped']
            }]
        )

        for inst in instances:
            inst.start()
            print("Instance Started: {}".format(instance.id))
