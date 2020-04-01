
# CDK deploy for Secure API gateway

##  Resources Used and deployed

### API Gateway
AWS API Gateway Rest API deployed with GET and POST calls proxies to AWS Lambda. AWS API Gateway authenticates the API using Lambda custom authoriser.

### AWS Lambda
Two AWS Lambda will be created
1. Lambda Proxy with S3 bucket to store the widgets
2. Edge Lambda is used a JWT authorizer integrates with Auth0 as IDP issuer

### Auth0
Opensource IDaaS to provide JWT t

### Pre-requisites
1. [Auth0](https://auth0.com/docs/integrations/aws-api-gateway/custom-authorizers/part-1)
2. AWS account
3. CDK binaries on laptop

### Installation
1. Download this repo locally
2. CDK deploy

### Post Installation Testing
Test Locally
```
curl  --request GET \
--url <API Endpoint>
--header 'authorization: Bearer <Bearer token from Auth0>'
```
### References
- https://auth0.com/docs/integrations/aws-api-gateway/custom-authorizers
- https://github.com/auth0-samples/jwt-rsa-aws-custom-authorizer
- https://github.com/aws-samples/aws-cdk-examples/tree/master/python/my-widget-service


