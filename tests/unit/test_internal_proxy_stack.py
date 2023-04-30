import aws_cdk as core
import aws_cdk.assertions as assertions

from internal_proxy.internal_proxy_stack import InternalProxyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in internal_proxy/internal_proxy_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = InternalProxyStack(app, "internal-proxy")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
