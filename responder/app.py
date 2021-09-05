#!/usr/bin/env python3

from aws_cdk import core
import os

from app.app_stack import Responder


app = core.App()
Responder(
    app, "Responder",
    env={
        "region": os.environ["CDK_DEFAULT_REGION"],
        "account": os.environ["CDK_DEFAULT_ACCOUNT"],
    }
)

app.synth()
