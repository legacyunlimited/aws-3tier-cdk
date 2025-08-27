from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    CfnOutput
)
from constructs import Construct

class Aws3TierCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # -----------------------
        # Data Layer: S3 Bucket
        # -----------------------
        self.data_bucket = s3.Bucket(
            self, "DataBucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # -----------------------
        # VPC
        # -----------------------
        self.vpc = ec2.Vpc(
            self, "Vpc",
            max_azs=2,
            nat_gateways=1,
        )

        # -----------------------
        # Application Layer: Lambda
        # -----------------------
        self.app_lambda = _lambda.Function(
            self, "AppLambda",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="image_processor.handler",  # Make sure your lambda file has this
            code=_lambda.Code.from_asset("aws_3tier_cdk/lambdas")
        )

        # Lambda can read/write S3
        self.data_bucket.grant_read_write(self.app_lambda)

        # -----------------------
        # API Gateway to expose Lambda
        # -----------------------
        api = apigw.LambdaRestApi(
            self, "ApiGateway",
            handler=self.app_lambda,
            proxy=True
        )

        # Output the endpoint for frontend
        CfnOutput(
            self, "LambdaApiUrl",
            value=api.url,
            description="Public API Gateway endpoint for Lambda"
        )

        # -----------------------
        # Presentation Layer: EC2
        # -----------------------
        ec2_role = iam.Role(
            self, "EC2S3AccessRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )
        self.data_bucket.grant_read(ec2_role)

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "yum update -y",
            "amazon-linux-extras install -y nginx1.12",
            "systemctl enable nginx",
            "systemctl start nginx",
            "mkdir -p /var/www/html/images",
            "yum install -y aws-cli",
            f"(crontab -l 2>/dev/null; echo '* * * * * aws s3 sync s3://{self.data_bucket.bucket_name}/output/ /var/www/html/images/') | crontab -"
        )

        self.web_server = ec2.Instance(
            self, "WebServer",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=self.vpc,
            role=ec2_role,
            user_data=user_data
        )

        # Output EC2 public IP for testing
        CfnOutput(
            self, "EC2PublicIP",
            value=self.web_server.instance_public_ip,
            description="Public IP of EC2 Web Server"
        )
