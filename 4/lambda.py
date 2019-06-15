import json
from manager import *
from app_exceptions import *

def run(event, context):
    print(json.dumps(event))
    http_method = event.get('httpMethod')
    if (http_method == 'POST'):
        try:
            payload = event.get('body')
            if payload is None:
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": "Please add application data"
                }
            else:
                manager = LicenceManager(json.loads(payload))
                license = manager.getLicense()
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": json.dumps(license)
                }
            
        except AppDoesNotExists:
            print("Application does not exist")
            return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": "Application does not exist"
                }
        except AppDoesNotSupportAutoLicence:
            print("Application does not support trial license")
            return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": "Application does not support trial license"
                }
        except TokenDoesNotMatchToApp:
            print("App token mismatch")
            return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": "App token mismatch"
                }
    else:
        try:
            http_params = event.get('queryStringParameters')
            app_id = http_params.get('app_id')
            app_token = http_params.get('app_token')
            if app_id is None or app_token is None:
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": "Please add application data"
                }
            else:
                manager = LicenceManager(None)
                manager.app_id = app_id
                manager.app_token = app_token
                licenses = manager.getAllLicensesForApplication()
                return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": json.dumps(licenses)
                }
            
        except AppDoesNotExists:
            print("Application does not exist")
            return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": "Application does not exist"
                }
        except TokenDoesNotMatchToApp:
            print("App token mismatch")
            return {
                    "statusCode": 200,
                    "headers": {
                        "Access-Control-Allow-Origin" : "*",
                        "Access-Control-Allow-Credentials" : True
                    },
                    "body": "App token mismatch"
                }
    

if __name__ == '__main__':
   run({"app_id" : "id1", "app_token" : "token1", "name" : "moje imie", "machine_key" : "key", "trial" : 30}, None)