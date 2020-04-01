from aws_cdk import (core,
                     aws_apigateway as apigateway,
                     aws_iam as iam,
                     aws_s3 as s3,
                     aws_lambda as lambda_)
import os,sys

class WidgetService(core.Construct):
    def __init__(self, scope: core.Construct, id: str):
        super().__init__(scope, id)

        bucket = s3.Bucket(self, "WidgetStore")
        # Environment Variables 
        aud = os.environ.get("AUDIENCE", os.environ["AUDIENCE"])
        jwks_url = os.environ.get("JWKS_URL", os.environ["JWKS_URL"])
        iss = os.environ.get("TOKEN_ISSUER", os.environ["TOKEN_ISSUER"])

        handler = lambda_.Function(self, "WidgetHandler",
                    runtime=lambda_.Runtime.NODEJS_10_X,
                    code=lambda_.Code.asset("resources"),
                    handler="widgets.main",
                     environment=dict(
                     BUCKET=bucket.bucket_name)
                    )
       # IAM Role creation for APIgateway

        role = iam.Role(self, "MyRole",
                assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com")
        )

        # role.add_to_policy(iam.PolicyStatement(
        #     resources=["*"],
        #     actions=["lambda:InvokeFunction"]
        # ))

        dirname = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

        bucket.grant_read_write(handler)

        api = apigateway.RestApi(self, "widgets-api",
                  rest_api_name="Widget Service",
                  description="This service serves widgets.",
                  cloud_watch_role=False
        )

        get_widgets_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        auth_fn = lambda_.Function(self, "jwtRsaCustomAuthorizer",
                    runtime=lambda_.Runtime.NODEJS_10_X,
                    code=lambda_.Code.from_asset(os.path.join(dirname, "lambda_custom_auth/custom-authorizer.zip")),
                    timeout=core.Duration.seconds(300),
                    memory_size=256,
                    handler="index.handler",
                    environment=dict(
                    # AUDIENCE="https://your-api-gateway",
                     AUDIENCE=aud,
                     JWKS_URI=jwks_url,
                     TOKEN_ISSUER=iss)
                    )
        
        auth = apigateway.TokenAuthorizer(self,"custom-authoriser",
                                        identity_source=None, 
                                        validation_regex="^Bearer [-0-9a-zA-z\.]*$",
                                        handler=auth_fn, 
                                        #handler="", 
                                        assume_role=role, 
                                        authorizer_name=None, 
                                        results_cache_ttl=None)

        api.root.add_method("GET", get_widgets_integration,authorizer=auth)   # GET /

        widget = api.root.add_resource("{id}")

        # Add new widget to bucket with: POST /{id}
        post_widget_integration = apigateway.LambdaIntegration(handler)

        # Get a specific widget from bucket with: GET /{id}
        get_widget_integration = apigateway.LambdaIntegration(handler)

        # Remove a specific widget from the bucket with: DELETE /{id}
        delete_widget_integration = apigateway.LambdaIntegration(handler)

        widget.add_method("POST", post_widget_integration);     # POST /{id}
        widget.add_method("GET", get_widget_integration);       # GET /{id}
        widget.add_method("DELETE", delete_widget_integration); # DELETE /{id}