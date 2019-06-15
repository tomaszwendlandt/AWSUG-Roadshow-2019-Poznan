from app_exceptions import *
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import datetime

BUCKET = "YOUR-BUCKET-NAME"
FILE = "apps.json"
DYNAMODB_TABLE = "YOUR-DYNAMODB-TABLE"

class Application():
    def __init__(self, data):
        self.app_id = data['appId']
        self.app_token = data['token']
        self.app_name = data['name']
        self.app_trial = data['trial']
    
    def __str__(self):
        return "Application Id: " + self.app_id + ", Application name: " +  self.app_name +", Application token: " + self.app_token + ", Trial Available: " + str(self.isTrial())
        
    def isTrial(self):
        return self.app_trial > 0
        

class LicenceManager():

    def __init__(self, data):
        if data is not None:
            self.app_id = data.get('app_id')
            self.app_token = data['app_token']
            self.name = data['name']
            self.machine_key = data['machine_key']
            self.user_name = data['name']

    def getLicense(self):
        app = self.authTokenMatchesToApp()
        license = self.loadLicense()
        if license is None:
            license = self.createTrialLicense(app)
        
        #Deserializing DynamoDB response
        boto3.resource('dynamodb')
        deserializer = boto3.dynamodb.types.TypeDeserializer()
        python_data = {k: deserializer.deserialize(v) for k,v in license.items()}
        return python_data
    
    def getAllLicensesForApplication(self):
        app = self.authTokenMatchesToApp()
        licenses = self.loadAllLicensesForApp()
        return licenses
    
    def createTrialLicense(self, app):
        if app.isTrial():
            expiration_date = datetime.date.today() + datetime.timedelta(days=app.app_trial)
            #Create trial license
            client = self.getDynamoDBClient()
            response = client.put_item(
            TableName = DYNAMODB_TABLE,
            Item = {
                'machine_key': {'S':self.machine_key},
                'application_id': {'S':app.app_id},
                'application_token' : {'S':app.app_token},
                'expiration_date': {'S':expiration_date.isoformat()},
                'user_name': {'S':self.user_name},
                'create_date' : {'S':datetime.date.today().isoformat()}
                
            }
            )
            license = self.loadLicense()
            return license
        else:
            raise AppDoesNotSupportAutoLicence

    def loadAllLicensesForApp(self):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.query(
            IndexName='application_id-index',
            KeyConditionExpression=Key('application_id').eq(self.app_id)
        )
        return response

    def loadLicense(self):
        client = self.getDynamoDBClient()
        key = {
        'machine_key': {'S': self.machine_key},
        'application_id': {'S': self.app_id}
            }
        response = client.get_item( TableName = DYNAMODB_TABLE, Key = key)
        item = response.get('Item')
        return item
        
        
    def getDynamoDBClient(self):
        return boto3.client('dynamodb')
    
    def authTokenMatchesToApp(self):
        app = self.getApp()
        if not self.app_token == app.app_token:
            raise TokenDoesNotMatchToApp
        return app


    def getApp(self):
        applications = self.loadFile()
        app = [item for item in applications['apps'] if item.get('appId')==self.app_id]
        if len(app) > 0:
            application = Application(app[0])
        else:
            raise AppDoesNotExists
        return application

    def loadFile(self):
        client = boto3.client('s3')
        try:
            result = client.get_object(Bucket=BUCKET, Key=FILE)
            text = result["Body"].read().decode()
            print(text)
            return json.loads(text)
        except Exception as Error:
            print(Error)
            raise AWSException(Error)