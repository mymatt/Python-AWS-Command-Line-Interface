
from botocore.exceptions import ClientError

class ec2Manager:

    def __init__(self, session):
        self.ec2 = session.resource('ec2')
        self.current_region = session.region_name

    def stop_instances(self, tagValue):
        """Stop all running ec2 instances"""
        # get only running instances
        tagName = "Group"

        ec2Filters = [{
            'Name': 'instance-state-name',
            'Values': ['running']
        }]

        if tagValue:
            itemF = {
                'Name': tagName,
                'Values': [tagValue]
                }
            ec2Filters.append(itemF)

        instances = self.ec2.instances.filter(Filters=ec2Filters)

        for inst in instances:
            inst.stop()
            print("Instance Stopped: {}".format(instance.id))

    def start_instances(self, tag):
        """Start all stopped ec2 instances"""
        # get only stopped instances
        tagName = "Group"

        ec2Filters = [{
            'Name': 'instance-state-name',
            'Values': ['stopped']
        }]

        if tagValue:
            itemF = {
                'Name': tagName,
                'Values': [tagValue]
                }
            ec2Filters.append(itemF)

        instances = self.ec2.instances.filter(Filters=ec2Filters)

        for inst in instances:
            inst.start()
            print("Instance Started: {}".format(instance.id))


# restrict actions on ec2 intances based on tag
# AllowActionsIfYouAreTheOwner
# tag key 'Owner' must have value that matches ${aws:username}
# update start and stop instance functions above to allow for restrictions

# create an AMI policy -> as per lect
# attache to group

# create policy for self to ec2:CreateTags
#
