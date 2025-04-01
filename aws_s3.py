import boto3

def archive_s3_bucket(bucket_name, output_dir):
    s3 = boto3.client('s3')
    os.makedirs(output_dir, exist_ok=True)
    objects = s3.list_objects_v2(Bucket=bucket_name)
    for obj in objects.get('Contents', []):
        s3.download_file(bucket_name, obj['Key'], os.path.join(output_dir, obj['Key']))
