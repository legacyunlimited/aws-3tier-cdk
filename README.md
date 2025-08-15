![CDK Synth](https://github.com/legacyunlimited/aws-3tier-cdk/actions/workflows/cdk-synth.yml/badge.svg)


# AWS 3-Tier (CDK, Python): VPC (public/private), ALB → EC2 Auto Scaling (Amazon Linux), optional RDS. Includes Linux hardening (SSM, no SSH by default), Nginx, systemd, and full IaC deploy/teardown. Built as a portfolio-ready example for Solutions Architect / DevOps interviews.

## Overview
This project demonstrates a production-style **3-tier architecture** on AWS using the **AWS Cloud Development Kit (CDK)** in Python.  
It provisions infrastructure for:
- **Presentation Layer:** Amazon S3 + CloudFront for static content
- **Application Layer:** Amazon ECS Fargate or AWS Lambda (depending on configuration)
- **Data Layer:** Amazon RDS (PostgreSQL/MySQL)

The project is designed as a **portfolio-ready example** to showcase cloud infrastructure skills for Solutions Architect and DevOps roles.

---

## Architecture Diagram

        ┌─────────────────────────┐
        │     Presentation Layer  │
        │  S3 + CloudFront         │
        └───────────┬─────────────┘
                    │
        ┌───────────▼─────────────┐
        │    Application Layer    │
        │ ECS Fargate / Lambda    │
        └───────────┬─────────────┘
                    │
        ┌───────────▼─────────────┐
        │       Data Layer        │
        │ Amazon RDS (Postgres)   │
        └─────────────────────────┘


---

## Technologies Used
- **AWS CDK** (Python)
- **Amazon S3**
- **Amazon CloudFront**
- **Amazon ECS Fargate** or **AWS Lambda**
- **Amazon RDS**
- **Amazon VPC**

---

## Prerequisites
- AWS Account & CLI configured
- Python 3.10+
- AWS CDK CLI installed
- Node.js 18+ (CDK dependency)

---

## Setup Instructions

1. **Clone the repository**
    ```bash
    git clone https://github.com/<your-username>/aws-3tier-cdk.git
    cd aws-3tier-cdk
    ```

2. **Create and activate a virtual environment**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Bootstrap the environment**
    ```bash
    cdk bootstrap aws://<ACCOUNT_ID>/<REGION>
    ```

5. **Synthesize the CloudFormation template**
    ```bash
    cdk synth
    ```

6. **Deploy**
    ```bash
    cdk deploy
    ```

---

## Deployment Flow
1. Write or modify infrastructure in `aws_3tier_cdk_stack.py`
2. Run `cdk synth` to verify the CloudFormation template
3. Deploy to AWS with `cdk deploy`
4. Test and iterate

---

## License
This project is licensed under the MIT License.
