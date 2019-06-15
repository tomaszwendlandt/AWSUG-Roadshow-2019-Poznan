import boto3
import json

print('Loading function')


def lambda_handler(event, context):
    # Create an SNS client
    sns = boto3.client('sns')

    for record in event['Records']:
        print(record['eventID'])
        print(record['eventName'])
        print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))

        # Publish a simple message to the specified SNS topic
        response = sns.publish(
            TopicArn='<YOUR-SNS-TOPIC-ARN>',
            Message=json.dumps(record['dynamodb'], indent=2),
            )

        # Print out the response
        print(response)

    return 'Successfully processed {} records.'.format(len(event['Records']))

