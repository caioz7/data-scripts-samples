# Copiando arquivos do mesmo bucket

import boto3

bucketname = "BUCKET_NAME"
s3 = boto3.resource('s3')
my_bucket = s3.Bucket(bucketname)
source = "PASTA_ORIGEM"
target = "PASTA_DESTINO"

for obj in my_bucket.objects.filter(Prefix=source):
    source_filename = (obj.key).split('/')[-1]
    copy_source = {
        'Bucket': bucketname,
        'Key': obj.key
    }
    target_filename = "{}/{}".format(target, source_filename)
    s3.meta.client.copy(copy_source, bucketname, target_filename)
    # Descomentar para deletar o source
    # s3.Object(bucketname, obj.key).delete()