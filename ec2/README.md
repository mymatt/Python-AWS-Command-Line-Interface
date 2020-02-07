
## Python EC2 Command Line Interface using Boto3, Click

### Set AWS Profile

1) Enter Profile on CLI
```
python3 ec2.py --profile profilename
```
2) Update default in ec2.py
```
@click.option('--profile', default='add_default_profile_name_here', help='AWS Profile')
```

### Options Available:

Stop All Instances              
```
python3 ec2.py stop-instances
```

Stop Instances by Group Tag (E.g Developer Instances, Test Instances)        
```
python3 ec2.py stop-instances --tag tagname
```

Start All Instances              
```
python3 ec2.py start-instances
```

Start Instances by Group Tag (E.g Developer Instances, Test Instances)        
```
python3 ec2.py start-instances --tag tagname
```

Backup Instances (sets remove tag (default in 30 days))            
```
python3 ec2.py backup-instances
```

Cleanup Backup Instances (after setting days til removal above)            
```
python3 ec2.py cleanup-backups
```
