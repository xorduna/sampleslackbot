import time

def want_something(slack_client, message, something):
    answer = "to get {something} you have to work hard!!!".format(
        something=something
    )
    # simulate a very long task
    time.sleep(10)
    slack_client.chat.post_message(message['channel'], answer, as_user=True)