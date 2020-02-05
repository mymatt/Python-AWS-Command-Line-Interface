
from botocore.exceptions import ClientError
from pathlib import Path

from hashlib import md5

class BucketAdmin:

    def __init__(self, session):
        self.s3 = session.resource('s3')
        self.current_region = session.region_name

        self.etags = {}

    def get_region(self, bucket):
        """Get the Buckets region name"""
        bucket_location = self.s3.meta.client.get_bucket_location(Bucket=bucket)
        return bucket_location["LocationConstraint"]

    def buckets_all(self):
        """Provide an Iterator for all buckets"""
        return self.s3.buckets.all()

    def objects_all(self, bucket):
        """Provide an Iterator for all objects in a bucket"""
        return self.s3.Bucket(bucket).objects.all()

    def setup_bucket(self, bucket):
        """Create bucket."""

        new_bucket = None

        try:
            new_bucket = self.s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={
            'LocationConstraint': self.current_region})
        except ClientError as err:
            print(err.response)
            if err.response['Error']['Code'] == '':
                print("Bucket {} already exists".format(bucket))
            else:
                raise err

        return new_bucket

    def create_object(self, bucket, object, key):
        # check etag of remote file (if exists) and compare with local
        # if match then do not upload
        self.get_etag(self.s3.Bucket(bucket))
        etag = self.create_etag(object)

        if self.etags.get(key, '') == etag:
            print("Etags match for file {}, upload skipped".format(key))
            return

        self.s3.Bucket(bucket).upload_file(object, key)

    def set_policy(self, bucket):
        # request user input multiple symbolize_names
        # import policy
        # add argument that enables, disables bucket policy
        policy = """
        {
            # policy PublicReadGetObject

        }
        """ % bucket.name

        policy = policy.strip()
        bucket_policy = self.s3.Bucket(bucket).Policy()
        bucket_policy.put(Policy=policy)

    def sync(self, path, bucket):
        root = Path(path).expanduser().resolve()

        self.get_etag(self.s3.Bucket(bucket))

        # recursion
        def process_dir(dir):
            for path in dir.iterdir():
                if path.is_dir():
                    process_dir(path)
                if path.is_file():
                    self.create_object(bucket, str(path), str(path.relative_to(root)))

        process_dir(root)

    # the returned data from list_objects_v2 contains
    # Etag -> hash
    # Key -> references filename
    # sift through data and extract only Key and Etag
    def get_etag(self, bucket):
        """Load manifest for caching purposes"""
        paginator = self.s3.meta.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket.name):
            for obj in page.get('Contents', []):
                self.etags[obj['Key']] = obj['ETag']

    @staticmethod
    def hash_data(data):
        hash = md5()
        hash.update(data)

        return hash

    def create_etag(self, path):
        hash = None
        # rb - reading in binary mode as hash deals with binary data
        with open(path, 'rb') as f:
            data = f.read()
            hash = self.hash_data(data)

            # double quotes around value used to match aws double quotes
            return '"{}"'.format(hash.hexdigest())

    def sync_bucket_check(self):
        """Check if files removed from bucket and sync local"""
        etag = create_etag(object)
        if self.etags.get(key, '') == etag:
            print("Etags match for file {}, upload skipped".format(key))
            return
