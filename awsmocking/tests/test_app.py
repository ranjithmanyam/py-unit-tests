import json
import os
import boto3
from moto import mock_sns, mock_sqs

from awsmocking.app.app import publish_message_to_sns, read_from_sqs_queue

test_message = "test_message"


@mock_sns
def test_public_message_to_sns():
    sns_resource = boto3.resource("sns", region_name="eu-west-1")

    topic = sns_resource.create_topic(Name="test-topic")

    os.environ["sns_topic_arn"] = topic.arn

    message_id = publish_message_to_sns(test_message)

    assert message_id


@mock_sns
@mock_sqs
def test_read_from_sqs_queue():
    sns_resource = boto3.resource("sns", region_name="eu-west-1")

    topic = sns_resource.create_topic(Name="test-topic")

    sqs_resource = boto3.resource("sqs", region_name="eu-west-1")

    queue = sqs_resource.create_queue(
        QueueName="test_queue"
    )

    os.environ["sns_topic_arn"] = topic.arn
    os.environ["sqs_queue_url"] = queue.url

    topic.subscribe(
        Protocol="sqs",
        Endpoint=queue.attributes["QueueArn"]
    )

    message_id = publish_message_to_sns(test_message)
    messages = read_from_sqs_queue()
    message_body = json.loads(messages["Messages"][0]["Body"])

    assert message_body["MessageId"] == message_id["MessageId"]
    assert message_body["Message"] == test_message
