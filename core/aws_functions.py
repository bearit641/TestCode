import logging
import os
import tempfile
import zipfile
from io import BytesIO

import boto3
from botocore.exceptions import ClientError

from django.conf import settings
from django.http import HttpResponse
from django.template.defaultfilters import filesizeformat


AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY

# Initialize AWS Resources here
s3 = boto3.resource(
    's3',
    region_name='eu-west-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
s3_client = boto3.client(
    's3',
    region_name='eu-west-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
ses_client = boto3.client(
    'ses', region_name='eu-west-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
sns = boto3.client(
    'sns',
    region_name='eu-west-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
ssm_client = boto3.client('ssm', region_name='eu-west-1')


def save_bytes_to_s3(file_contents, filename, bucket_name):
    """
    Save bytes as a file in S3 bucket with the provided key (file location)
    """
    s3.Bucket(bucket_name).put_object(Key=filename, Body=file_contents)


def save_to_s3(file_contents, filename, bucket_name):
    encoded_string = file_contents.encode("utf-8")
    """
    Save file as utf8-encoded string
    """
    s3.Bucket(bucket_name).put_object(Key=filename, Body=encoded_string)


def read_from_s3(filename, bucket_name):
    obj = s3.Object(bucket_name, filename)
    body = obj.get()['Body'].read()
    return body


def list_s3_bucket_objects(bucket_name):
    """
    Retrieve files from given S3 bucket
    """

    s3_objects = []
    files = s3_client.list_objects_v2(Bucket=bucket_name)

    # Check if the bucket is not empty.
    if files.get('Contents'):
        files = files['Contents']
        sorted_files = [
            obj
            for obj in sorted(
                files,
                key=lambda x: x['LastModified'],
                reverse=True
            )
        ]
        for obj in sorted_files:
            # Converts datetime format to Month name short version, day,
            # year and time. (Feb 26, 2021, 00:00:00)
            last_modified = obj['LastModified'].strftime('%b %d, %Y, %H:%M:%S')
            file_size = filesizeformat(obj['Size'])
            filename = obj['Key']
            s3_objects.append(
                {
                    'filename': filename,
                    'last_modified': last_modified,
                    'size': file_size
                }
            )
    return s3_objects


def publish_sns(sns_topic, subject, message):
    """
    Publush an SNS notification to a specified SNS topic
    """
    try:
        sns.publish(
            TopicArn=sns_topic,
            Subject=subject,
            Message=message
        )
    except Exception as e:
        # Log failure before raising exception.
        logging.error('Failed to send to SNS.')
        raise Exception(e)


def create_presigned_url(bucket_name, object_name):
    """
    Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name
            },
            ExpiresIn=3600
        )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def get_s3_objects_as_zip(bucket_name, filenames):
    """
    Get the files on s3, read each file then zip.
    Returns zip as byte object.

    :param bucket_name: string
    :param object_name: string

    Reference:
    https://www.botreetechnologies.com/blog/create-and-download-zip-file-in-django-via-amazon-s3/
    """

    byte = BytesIO()
    zip_file = zipfile.ZipFile(byte, "w")

    # Create a temporary directory so that the files inside this
    # can be compiled as zip.
    with tempfile.TemporaryDirectory() as directory:
        for filename in filenames:
            s3_object = s3.Object(bucket_name, filename)
            data = s3_object.get()['Body'].read()
            file_path = f'{directory}/{filename}'
            with open(file_path, 'wb') as f:
                f.write(data)
                zip_file.write(file_path, os.path.basename(file_path))
        zip_file.close()

    return byte


def delete_s3_objects(bucket_name, filenames):
    """
    Delete the filenames in the indicated bucket.

    :param bucket_name: string
    :param object_name: string
    """

    for filename in filenames:
        s3_client.delete_object(
            Bucket=bucket_name,
            Key=filename
        )


def get_parameter_from_ssm(name, decryption=True):
    """
    A generic function that will get a parameter on Amazon Systems
    Manager Agent(SSM) based on parameter name.

    How to use:
    value = get_parameter_from_ssm(name='/value/staging')
    """

    try:
        parameter = ssm_client.get_parameter(
            Name=str(name),
            WithDecryption=decryption
        )
        return parameter['Parameter']['Value']
    except Exception as e:
        logging.error('Failed to get the parameter from SSM.')
        raise e


def change_parameter_value(name, value, overwrite=False):
    """
    A generic function that will change a parameter value on Amazon
    Systems Manager Agent(SSM).

    Note:
    The default overwrite is False because this function is dangerous to
    use. Use with extra care.

    How to use:
    change_parameter_value(
        name='/value/staging',
        value='some string',
        overwrite=True
    )
    """

    try:
        ssm_client.put_parameter(
            Name=name,
            Value=value,
            Type='String',
            Overwrite=overwrite
        )
    except Exception as e:
        logging.error('Failed to change the parameter from SSM.')
        raise e
