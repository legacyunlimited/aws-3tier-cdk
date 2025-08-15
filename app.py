#!/usr/bin/env python3
import os

import aws_cdk as cdk

from aws_3tier_cdk.aws_3tier_cdk_stack import Aws3TierCdkStack


app = cdk.App()
Aws3TierCdkStack(app, "Aws3TierCdkStack")
app.synth()
