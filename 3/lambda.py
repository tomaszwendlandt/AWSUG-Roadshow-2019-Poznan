import json
from manager import *
from app_exceptions import *

def run(event, context):
   # print(json.dumps(event))
    try:
        #payload = event.get('body')
        payload = event
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
            manager = LicenceManager(payload)
            #manager = LicenceManager(json.loads(payload))
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
    
    

if __name__ == '__main__':
   run({"app_id" : "id1", "app_token" : "token1", "name" : "moje imie", "machine_key" : "key", "trial" : 30}, None)