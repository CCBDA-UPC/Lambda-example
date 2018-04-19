import boto3
import json

print('Loading function')
dynamo = boto3.client('dynamodb')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin':'*',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    # print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': lambda dynamo, x: dynamo.delete_item(**x),
        'GET': lambda dynamo, x: dynamo.scan(**x),
        'POST': lambda dynamo, x: dynamo.put_item(**x),
        'PUT': lambda dynamo, x: dynamo.update_item(**x),
    }

    operation = event['httpMethod']
    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else json.loads(event['body'])
        return respond(None, operations[operation](dynamo, payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
    
###### DO NOT COPY TO AWS LAMBDA CONSOLE FROM HERE
###### Less optimized version of lambda_handler()
#    operation = event['httpMethod']
#    if operation is 'GET':
#        return respond(None, dynamo.scan(event['queryStringParameters']))
#    elif operation is 'POST':
#        return respond(None, dynamo.put_item(json.loads(event['body'])))
#    elif operation is 'DELETE':
#        return respond(None, dynamo.delete_item(json.loads(event['body'])))
#    elif operation is 'PUT':
#        return respond(None, dynamo.update_item(json.loads(event['body'])))
#    else:
#        return respond(ValueError('Unsupported method "{}"'.format(operation)))
###### USE THE CODE BELOW TO TEST lambda_handler()

print('--------------------GET event test')
get_event = {
    "httpMethod": "GET",
    "queryStringParameters": {
        "TableName": "ccbda-example"
    }
}
result = lambda_handler(get_event, None)
print('--------------------RESULT')
print(json.dumps(result, indent=2))
print('--------------------RESULT body')
print(json.dumps(json.loads(result['body']), indent=2))



print('--------------------POST event test')

myvar = {
    'TableName': 'ccbda-example',
    'Item': {
        'thingid': {
            'S': 'no idea'
        }
    }
}

post_event = {
    "httpMethod": "POST",
    "body": json.dumps(myvar, separators=(',', ':'))
}
result = lambda_handler(post_event, None)
print('--------------------RESULT')
print(json.dumps(result, indent=2))
print('--------------------RESULT body')
print(json.dumps(json.loads(result['body']), indent=2))


