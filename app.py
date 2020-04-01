#!/usr/bin/env python3

from aws_cdk import core

from secure_apigateway.secure_apigateway_stack import SecureApigatewayStack


app = core.App()
SecureApigatewayStack(app, "secure-apigateway", env={'region': 'ap-southeast-1'})

app.synth()
