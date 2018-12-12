import boto3
import botocore

s3_client = boto3.client("s3",
                         config=botocore.client.Config(signature_version='s3v4')
                         )

def get_download_url(object_dict):
    bucket = object_dict["Bucket"]
    key = object_dict["Key"]
    s3_client.head_bucket(Bucket=bucket)
    generate_presigned_url(bucket, key)

def generate_presigned_url(bucket, key):
    return s3_client.generate_presigned_url(
        ClientMethod='get_object',
        ExpiresIn=60,
        Params={
            'Bucket': bucket,
            'Key': key
        })

