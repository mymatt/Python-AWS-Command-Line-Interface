
from botocore.exceptions import ClientError
from datetime import date, timedelta

class ec2Manager:

    def __init__(self, session):
        self.ec2 = session.resource('ec2')


    def list_instances(self, tagKey, tagValue):
        paginator = self.ec2.meta.client.get_paginator('describe_instances')
        response = paginator.paginate(Filters=[
                {
                    'Name': 'tag:'+TagKey', 'Values': [tagValue]
                }
            ]
        )
        for reservation in response.get("Reservations"):
            for instance in reservation.get("Instances"):
                print("Instance ID: {0}".format(instance.id))
        # list by name, tag:Name, uptime, instance-id, state


    @staticmethod
    def filterEC2(tagValue, current_state):
        tagName = "Group"

        ec2Filters = [
            {
                'Name': 'instance-state-name',
                'Values': [current_state]
            }
        ]

        if tagValue:
            itemF = {
                'Name': 'tag:'+tagName,
                'Values': [tagValue]
                }
            ec2Filters.append(itemF)

        return ec2Filters


    def stop_instances(self, tagValue):
        """Stop all running ec2 instances"""
        # get only running instances and those with Group=tagValue e.g Group=Developers
        filter = filterEC2(tagValue, 'running')
        instances = self.ec2.instances.filter(Filters=filter)

        for inst in instances:
            inst.stop()
            print("Instance Stopped: {}".format(instance.id))


    def start_instances(self, tagValue):
        """Start all stopped ec2 instances"""
        # get only stopped instances and those with Group=tagValue
        filter = filterEC2(tagValue, 'stopped')
        instances = self.ec2.instances.filter(Filters=filter)

        for inst in instances:
            inst.start()
            print("Instance Started: {}".format(instance.id))


    def modify_tag(self):
        pass


    def backup_instances(self):
        # specify days until snapshot deletion
        daysUntilDelete = 30

        #  find instances with backup = true
        instances = self.ec2.instances.filter(
            Filters=[
                {
                    'Name': 'tag:Backup', 'Values': ['true']
                }
            ]
        )

        for i in instances.all():
            names = [tag.get('Value') for tag in i.tags if tag.get('Key') == 'Name']
            name = names[0] if names else None

            for v in i.volumes.all():

                timestamp = datetime.utcnow().replace(microsecond=0).isoformat()
                desc = 'Backup of volume:{0}, on EC2 Name:{1} id:{2}, created{3}'.format(v.id, name, i.id, timestamp)

                print('Creating snapshot for volume:{0}, on EC2 Name:{1} id:{2}, created{3}'.format(v.id, name, i.id, timestamp))
                snapshot = v.create_snapshot(Description=desc)
                print('Snapshot {} Complete'.format(snapshot.id))

                remove_timestamp = (datetime.datetime.utcnow() + timedelta(days=daysUntilDelete)).strftime('%Y%m%d')

                snapshot.create_tags(
                      Tags = [
                          {
                              'Key': 'Remove',
                              'Value': 'true'
                          },
                          {
                              'Key': 'RemoveDate',
                              'Value': remove_timestamp
                          },
                          {
                              'Key': 'CreatedOn',
                              'Value': timestamp
                          }
                      ]
                  )


    def cleanup_backups(self):
        # remove backup after n days and images > m
        snapshots = self.ec2.snapshots.filter(
                  Filters=[
                      {
                        'Name': 'tag:Remove', 'Values': ['true']
                      }
                  ]
              )

        current_date = datetime.datetime.utcnow().strftime('%Y%m%d')

        for snap in snapshots:
            remove = [tag.get('Value') for tag in snap.tags if tag.get('Key') == 'RemoveDate']
            remove_date = remove[0]

            create = [tag.get('Value') for tag in snap.tags if tag.get('Key') == 'CreatedOn']
            create_date = create[0]

            if remove_date <= current_date:
                print('Deleting Snapshot id {0} created on {1}...'.format(snap.id, create_date))
                snap.delete()
                print('Snapshot deleted')





# restrict actions on ec2 intances based on tag
# AllowActionsIfYouAreTheOwner
# tag key 'Owner' must have value that matches ${aws:username}
# update start and stop instance functions above to allow for restrictions

# create an AMI policy -> as per lect
# attache to group

# create policy for self to ec2:CreateTags
#
