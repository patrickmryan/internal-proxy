from os.path import join
from aws_cdk import (
    Duration,
    Stack,
    Tags,
    RemovalPolicy,
    CfnOutput,
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_lambda as _lambda,
    aws_logs as logs,
)
from constructs import Construct


class InternalProxyStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        permissions_boundary_policy_arn = self.node.try_get_context(
            "PermissionsBoundaryPolicyArn"
        )

        if not permissions_boundary_policy_arn:
            permissions_boundary_policy_name = self.node.try_get_context(
                "PermissionsBoundaryPolicyName"
            )
            if permissions_boundary_policy_name:
                permissions_boundary_policy_arn = self.format_arn(
                    service="iam",
                    region="",
                    account=self.account,
                    resource="policy",
                    resource_name=permissions_boundary_policy_name,
                )

        if permissions_boundary_policy_arn:
            policy = iam.ManagedPolicy.from_managed_policy_arn(
                self, "PermissionsBoundary", permissions_boundary_policy_arn
            )
            iam.PermissionsBoundary.of(self).apply(policy)

        # apply tags to everything in the stack
        app_tags = self.node.try_get_context("Tags") or {}
        for key, value in app_tags.items():
            Tags.of(self).add(key, value)

        runtime = _lambda.Runtime.PYTHON_3_9
        log_retention = logs.RetentionDays.ONE_WEEK
        lambda_principal = iam.ServicePrincipal("lambda.amazonaws.com")
        lambda_root = "lambda"

        proxy_lambda = _lambda.Function(
            self,
            "ProxyLambda",
            runtime=runtime,
            code=_lambda.Code.from_asset(join(lambda_root, "serverless_proxy")),
            handler="serverless_proxy.lambda_handler",
            environment={
                "PROXY_URL": "http://172.31.2.255:3128",
                "PROXY_USERNAME": "proxyuser",
                "PROXY_PASSWORD": "pr0xy",
            },
            timeout=Duration.seconds(60),
            # role=service_role,
            log_retention=log_retention,
        )

        proxy_api = apigw.LambdaRestApi(
            self, "ProxyApi", handler=proxy_lambda, proxy=True
        )
