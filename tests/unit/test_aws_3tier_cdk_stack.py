import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_3tier_cdk.aws_3tier_cdk_stack import Aws3TierCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_3tier_cdk/aws_3tier_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Aws3TierCdkStack(app, "aws-3tier-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
