import os
import json

def lambda_handler(event, context):
    print(json.dumps(event))
    token = event['authorizationToken']
    arn = event['methodArn']
    return policy_generator(arn, token)

def policy_generator(resource, token):
    effect = 'Deny'
    auth_token = os.environ['auth_token']
    if token == auth_token:
        effect = 'Allow'
    return {
        "principalId": "principalId1",
        "policyDocument": {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": effect,
                "Action": "execute-api:Invoke",
                "Resource": resource
            }
        ]
    }
}
