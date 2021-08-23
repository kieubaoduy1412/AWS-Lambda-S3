import json
import csv
import requests
import boto3
from datetime import datetime
import base64

print("Loading function")
s3 = boto3.client('s3')
def lambda_handler(event, context):
    print("Event")
    print(event)
    if event['httpMethod'] == 'GET':
        
        #1 ユーザーから送ったファイル名を取得し処理する
        fileName = event['queryStringParameters']['fileNameOfCSV']
        print("ファイル名：" + fileName)
        # ファイル名が存在しているかチェック用の変数
        booCheckFileNameIsValid = True
        
        # どのフォルダーをチェック対象にする変数
        bucket = "XXX"
        prefix  = "YYY/"
        try :
            s3Objects = s3.list_objects(Bucket=bucket, Prefix=prefix)
            if 'Contents' in s3Objects:
                keys = [content['Key'] for content in s3Objects['Contents']]
     
                keys.remove(prefix)
                for i in range(0, len(keys)):
                    if keys[i] == (prefix + fileName) :
                        booCheckFileNameIsValid = False
                        break
     
            else:
                booCheckFileNameIsValid = False
        except:
            booCheckFileNameIsValid = False
        
        #2 結果を準備する
        transactionResponse = {}
        transactionResponse['checkFileNameIsValid'] = booCheckFileNameIsValid
        
        #3 Httpsレスポンスを構築する
        responseObject = {}
        responseObject['statusCode'] = 200
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['headers']['Access-Control-Allow-Origin'] = '*'
        responseObject['headers']['Access-Control-Allow-Headers'] = 'Content-Type'
        responseObject['headers']['Access-Control-Allow-Methods'] = 'OPTIONS,POST,GET'
        responseObject['body'] = json.dumps(transactionResponse)

        #4 ユーザーに返却する
        return responseObject
    elif event['httpMethod'] == 'POST':
        print("POST")
        #メイン
        csvFromUser = event['body']

        #1 S3に保存する
        bucket = 'XXX'
        data = json.loads(csvFromUser)

        upload_key = 'YYY/' + data['fileNameOfCSV']
        # Generate the presigned URL for put requests
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': 'XXX',
                'Key': upload_key,
                'ContentType': 'text/csv', 
            }
        )
        
        #2 結果を準備する
        transactionResponse = {}
        transactionResponse['upload_url'] = presigned_url

        #3 Httpsレスポンスを構築する
        responseObject = {}
        responseObject['statusCode'] = 200
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['headers']['Access-Control-Allow-Origin'] = '*'
        responseObject['headers']['Access-Control-Allow-Headers'] = 'Content-Type'
        responseObject['headers']['Access-Control-Allow-Methods'] = 'OPTIONS,POST,GET'
        responseObject['body'] = json.dumps(transactionResponse)
        
        print("responseObject")
        print(responseObject)
        
        return responseObject
