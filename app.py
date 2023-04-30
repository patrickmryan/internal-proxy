import os
from aws_cdk import App, Environment

from internal_proxy.internal_proxy_stack import InternalProxyStack

app = App()
InternalProxyStack(
    app,
    "InternalProxyStack",
    env=Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION")
    ),
)

app.synth()
