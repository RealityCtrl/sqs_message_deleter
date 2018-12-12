import logging
logger = logging.getLogger()

def delete_messages(event, file_list_helper):
    list_ids = get_list_ids(event)
    response = file_list_helper.delete_messages()
    log_response(response)
    return response

def get_list_ids(event):
    # todo extract list ids from event


def log_response(response_list):
    log_message = "Receipt_handle: {0} ,Status: {1}"
    for response in response_list:
        logger.info(log_message.format(response[0],response[1]))

