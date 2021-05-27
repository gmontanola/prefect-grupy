from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3 as _s3,
    aws_ecs as ecs,
    core,
)

app = core.App()
stack = core.Stack(app, "prefect-grupyrp-free-tier")

s3 = _s3.Bucket(
    stack,
    "Bucket",
    bucket_name="prefect-grupyrp",
    block_public_access=_s3.BlockPublicAccess.BLOCK_ALL,
)

vpc = ec2.Vpc(stack, "Vpc", cidr="10.0.0.0/16", nat_gateways=0)
public_subnets = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
cluster_capacity = ecs.AddCapacityOptions(
    instance_type=ec2.InstanceType("t2.micro"),
    max_capacity=1,
    desired_capacity=1,
    vpc_subnets=public_subnets,
)
cluster = ecs.Cluster(
    stack,
    "prefect-cluster",
    vpc=vpc,
    capacity=cluster_capacity,
    cluster_name="prefect-grupy-cluster",
)

app.synth()
