import json
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Tasks')

def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE'
        },
        'body': json.dumps(body)
    }

def lambda_handler(event, context):
    print("RECEIVED EVENT:", json.dumps(event))
    
    if event.get('httpMethod') == 'OPTIONS':
        return build_response(200, {'message': 'CORS preflight passed'})

    http_method = event.get('httpMethod')
    query_params = event.get('queryStringParameters') or {}
    
    try:
        if http_method == 'GET':
            response = table.scan()
            return build_response(200, response.get('Items', []))

        elif http_method == 'POST':
            body = json.loads(event.get('body') or '{}')
            if 'title' not in body:
                return build_response(400, {'error': 'Missing "title" field'})
                
            new_item = {
                'taskId': str(uuid.uuid4()),  # Updated to taskId
                'title': body['title'],
                'completed': False
            }
            table.put_item(Item=new_item)
            return build_response(201, new_item)

        elif http_method == 'PUT':
            task_id = query_params.get('taskId') # Updated to look for taskId
            if not task_id:
                return build_response(400, {'error': 'Missing "taskId" query parameter'})
                
            body = json.loads(event.get('body') or '{}')
            table.update_item(
                Key={'taskId': task_id},  # Updated to taskId
                UpdateExpression="set completed = :c",
                ExpressionAttributeValues={':c': body['completed']},
                ReturnValues="UPDATED_NEW"
            )
            return build_response(200, {'message': 'Task updated'})

        elif http_method == 'DELETE':
            task_id = query_params.get('taskId') # Updated to look for taskId
            if not task_id:
                return build_response(400, {'error': 'Missing "taskId" query parameter'})
                
            table.delete_item(Key={'taskId': task_id}) # Updated to taskId
            return build_response(200, {'message': 'Task deleted'})

        else:
            return build_response(405, {'error': f'Method {http_method} not allowed'})

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return build_response(500, {'error': 'Internal Server Error', 'details': str(e)})