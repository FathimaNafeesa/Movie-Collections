import boto3
import json


class SendMessage:

    def send_message_to_queue(self, message):
        # Get the current date & time

        sqs_client = boto3.client("sqs", region_name="ap-northeast-1")
        response = sqs_client.get_queue_url(
            QueueName="password-tasks",
        )
        # send sqs message with the current date & time
        message = sqs_client.send_message(
            QueueUrl=response["QueueUrl"],
            MessageBody=json.dumps(message)
        )
        return {

            json.dumps(message, indent=2)
        }

    def get_messages(self):
        sqs_client = boto3.resource("sqs", region_name="ap-northeast-1")

        # send sqs message with the current date & time
        queue = sqs_client.get_queue_by_name(QueueName="password-tasks")
        print(queue.receive_messages())





