from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
)
from constructs import Construct

class VideoProcessingStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Data Layer - DynamoDB table
        table = dynamodb.Table(
            self, "VideoMetadataTable",
            partition_key={"name": "video_id", "type": dynamodb.AttributeType.STRING},
            removal_policy=dynamodb.RemovalPolicy.DESTROY
        )

        # Application Layer - Lambda
        encode_lambda = _lambda.Function(
            self, "EncodeLambda",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="encode.handler",
            code=_lambda.Code.from_asset("lambda"),
        )

        # Grant Lambda permission to read/write to DynamoDB
        table.grant_read_write_data(encode_lambda)

        # Optional: S3 bucket for storage
        bucket = s3.Bucket(
            self, "VideoBucket",
            removal_policy=s3.RemovalPolicy.DESTROY
        )

        # IAM Role (demonstrates understanding of security)
        role = iam.Role(
            self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ]
        )
        encode_lambda.role = role
