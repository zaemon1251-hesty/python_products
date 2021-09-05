from aws_cdk import (
    core,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_iam as iam,
    aws_ecs_patterns as ecs_patterns,
    aws_logs,
)
import os


class Responder(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        vpc = vpc = ec2.Vpc(
            self, "responder-Vpc",
            max_azs=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                )
            ],
            nat_gateways=0,
        )

        # ec2.Vpc.from_lookup(
        #     self, 'responder-Vpc', vpc_id="vpc-e7a36481")

        role = iam.Role.from_role_arn(
            self, "Role", os.getenv("ARN_URI"))

        # <3>
        cluster = ecs.Cluster(
            self, "responder-Cluster",
            vpc=vpc,
        )

        cluster.add_capacity("AutoScalingCapacity",
                             instance_type=ec2.InstanceType("t2.micro"),
                             desired_capacity=3
                             )

        # <4>
        taskdef = ecs.FargateTaskDefinition(
            self, "responder-TaskDef",
            cpu=1024,  # 1 CPU
            memory_limit_mib=4096,  # 4GB RAM
        )

        ecr_repository = ecr.Repository(
            self, 'responder-Repository',
            repository_name='responder'
        )

        container = taskdef.add_container(
            "responder-Container",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repository),
            memory_limit_mib=4000,
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="responder",
                log_retention=aws_logs.RetentionDays.ONE_DAY
            ),
        )

        container.add_port_mappings(
            ecs.PortMapping(container_port=80, host_port=80)
        )

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "responder-FargateService",
            cluster=cluster,
            task_definition=taskdef,
            listener_port=80
        )

        # Store parameters in SSM
        ssm.StringParameter(
            self, "ECS_CLUSTER_NAME",
            parameter_name="ECS_CLUSTER_NAME",
            string_value=cluster.cluster_name,
        )
        ssm.StringParameter(
            self, "ECS_TASK_DEFINITION_ARN",
            parameter_name="ECS_TASK_DEFINITION_ARN",
            string_value=taskdef.task_definition_arn
        )
        ssm.StringParameter(
            self, "ECS_TASK_VPC_SUBNET_1",
            parameter_name="ECS_TASK_VPC_SUBNET_1",
            string_value=vpc.public_subnets[0].subnet_id
        )
        ssm.StringParameter(
            self, "CONTAINER_NAME",
            parameter_name="CONTAINER_NAME",
            string_value=container.container_name
        )
        ssm.StringParameter(
            self, "ECS_CLUSTER_ROLE",
            parameter_name="ECS_CLUSTER_ROLE",
            string_value=role.role_name,
        )

        core.CfnOutput(self,
                       "ClusterName",
                       value=cluster.cluster_name)
        core.CfnOutput(self,
                       "TaskDefinitionArn",
                       value=taskdef.task_definition_arn)
        core.CfnOutput(
            self,
            "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
        )


app = core.App()
