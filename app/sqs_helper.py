import boto3
import os
import logging


logger = logging.getLogger()

SQS_CLIENT = boto3.client('sqs')

url = os.environ['endpoint']
max_messages = os.environ['max_messages']
wait_time = os.environ['wait_time']
queue = SQS_CLIENT.Queue('url')

delete_error_message = "Delete failed for receipt handle: {0}, Error Code: {1}, Error message{2}"

def get_file_list_with_location():
    messages = poll_for_messages(max_messages, wait_time)
    return parse_message_contents(messages)


def poll_for_messages(max_messages=10, wait_time=20):
    return queue.receive_messages(
        AttributeNames = ["ALL"],
        MaxNumberOfMessages = max_messages,
        WaitTimeSeconds = wait_time
    )


def parse_message_contents(sqs_messages):
    output = []
    for message in sqs_messages:
        message_output = parse_message(message)
        output.append(message_output)
    return output


def parse_message(message):
    message_output = dict()
    message_output["Id"] = message.receipt_handle
    message_body = message.body
    message_output["Bucket"] = message_body["records"][0]["S3"]["bucket"]["name"]
    message_output["Key"] = message_body["records"][0]["S3"]["object"]["key"]
    return message_output


def delete_messages(receipt_handle_list):
    entries = generate_delete_entries(receipt_handle_list)
    response = delete_entries(entries)


def delete_entries(entries):
    return queue.delete_messages(Entries=entries)


def generate_delete_entries(receipt_handle_list):
    entries = []
    count = 0
    for receipt_handle in receipt_handle_list:
        entries.append(dict(Id=str(count), ReceiptHandle=receipt_handle))
        count += 1
    return entries


def handle_response(entries, response):
    retry_list = handle_failures(entries, response)
    if len(retry_list > 0):
        retry_entries = generate_delete_entries(retry_list)
        retry_failures = retry_failure(retry_entries)
        # todo return list of receipt handles with sucess/failure



def get_receipt_handle_for_failure(entries, failure):
    id_ = int(failure["Id"])
    return entries[id]["ReceiptHandle"]


def handle_failures(entries, response):
    retry_list=[]
    count = 0
    for failure in response["Failed"]:
        receipt_handle = get_receipt_handle_for_failure(entries, failure)
        if failure["SenderFault"]:
            log_failure(failure, receipt_handle)
        else:
            retry_list.append(receipt_handle)
            count += 1
    return retry_list


def log_failure(failure, receipt_handle):
    logger.error(delete_error_message.format(receipt_handle, failure["Code "], failure["Message "]))


def retry_failure(retry_list):
    response = delete_entries(retry_list)
    failures = []
    for failure in response["Failed"]:
        receipt_handle = get_receipt_handle_for_failure(retry_list, failure)
        failures.append(receipt_handle)
        log_failure(failure, receipt_handle)
    return failures

def update_responses()
            
            


