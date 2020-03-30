import json
import pytest

from aws_cdk import core
from secure-apigateway.secure_apigateway_stack import SecureApigatewayStack


def get_template():
    app = core.App()
    SecureApigatewayStack(app, "secure-apigateway")
    return json.dumps(app.synth().get_stack("secure-apigateway").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
