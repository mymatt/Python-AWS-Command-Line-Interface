
## Python Command Line Interface using Boto3, Click

### Set AWS Profile

1) Enter Profile on CLI
```
python3 s3.py --profile profilename
```
2) Update default in s3.py
```
@click.option('--profile', default='add_default_profile_name_here', help='AWS Profile')
```

### Options Available:

List buckets              
```
python3 s3.py --list-buckets
```

List bucket contents              
```
python3 s3.py --list-bucket-objects bucket
```

Create bucket
```
python3 s3.py --create-bucket bucket
```

Upload object
```
python3 s3.py --upload-object bucket object key
```

Sync bucket
```
python3 s3.py --sync-bucket path bucket
```

--load-policy




TODO
--download-object

--delete-bucket

--delete-object
