import json
import generate_delete_request
import s3_helper
import sqs_helper


def lambda_handler(event, context):
    try:
        response_body = generate_download_response.get_response(sqs_helper, s3_helper)
    except Exception as e:
        # Send some context about this error to Lambda Logs
        print(e)
        raise e
    return {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
