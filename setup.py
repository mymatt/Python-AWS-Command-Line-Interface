from setuptools import setup

setup(
    name='s3',
    version='0.1',
    author='M Myers',
    author_email='myers1matthew@gmail.com',
    description='S3 AWS Command Line Interface',
    license='GPLv3+',
    packages=['s3'],
    url='https://github.com/mymatt/Python-AWS-Command-Line-Interface',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        s3=s3.s3.cli
    '''
)
