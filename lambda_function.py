# lambda_function.py
import json
import boto3
import urllib.parse

def lambda_handler(event, context):
    # 指定区域（必须与 S3 存储桶区域一致！）
    region = 'us-east-2'  
    rekognition = boto3.client('rekognition', region_name=region)
    s3 = boto3.client('s3', region_name=region)
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table('FaceData')

    try:
        # 获取存储桶和文件路径
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

        # 验证 S3 对象可访问
        s3.head_object(Bucket=bucket, Key=key)  # 关键检查！
        print(f"正在处理文件：s3://{bucket}/{key}")

        # 调用 Rekognition
        response = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            Attributes=['ALL']
        )

        # 检查是否检测到人脸
        if not response['FaceDetails']:
            print("错误：未检测到人脸！")
            return {'statusCode': 400}

        # 提取数据并写入 DynamoDB
        face_details = response['FaceDetails'][0]
        table.put_item(Item={
            'FaceID': key, #需要和设定的变量一致
            'Age': face_details['AgeRange']['Low'],
            'Emotion': face_details['Emotions'][0]['Type']
        })
        print("数据写入成功！")
        return {'statusCode': 200}

    except Exception as e:
        print("错误：", str(e))
        return {'statusCode': 500}
