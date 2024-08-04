import json
from src.query import natural_language_to_sql, execute_query

def handler(event, context):
    try:
        body = json.loads(event['body'])
        user_query = body['query']

        sql_query = natural_language_to_sql(user_query)

        if sql_query:
            results = execute_query(sql_query)
            if results:
                return {
                    'statusCode': 200,
                    'body': json.dumps(results)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'message': 'No results found for your query.'})
                }
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': "I'm sorry, I couldn't understand that query. Could you rephrase it?"})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"An error occurred while processing your query: {str(e)}"})
        }