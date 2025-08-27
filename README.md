# AWS 3-Tier Architecture (CDK, Python): VPC, ALB → EC2 Auto Scaling, Lambda/S3, optional RDS

![CI/CD](https://github.com/legacyunlimited/aws-3tier-cdk/actions/workflows/ci-cd.yml/badge.svg)

This project demonstrates a **production-style 3-tier architecture** on AWS using the **AWS Cloud Development Kit (CDK)** in Python.  
It is **portfolio-ready** for Solutions Architect / DevOps roles and showcases **CI/CD, unit testing, IaC, and optional sandbox deployment**.

---

## Overview

This project provisions a secure, scalable architecture:

- **Presentation Layer:** Amazon S3 + CloudFront for static content  
- **Application Layer:** AWS Lambda (with mocked S3 tests) or Amazon ECS Fargate / EC2 Auto Scaling  
- **Data Layer:** Amazon RDS (PostgreSQL/MySQL) – optional  

**Key Features:**

- Full Infrastructure as Code (IaC) using **AWS CDK**
- Linux hardening: SSM access only, no SSH by default
- Nginx + systemd setup for EC2
- CI/CD pipeline with **GitHub Actions**:
  - Automated unit tests (`pytest` + mocked Lambda)
  - CDK synth & diff validation
  - Optional sandbox deploy and destroy

---

## Architecture Diagram

    ┌─────────────────────────┐
    │     Presentation Layer  │
    │  S3 + CloudFront         │
    └───────────┬─────────────┘
                │
    ┌───────────▼─────────────┐
    │    Application Layer    │
    │ Lambda / ECS / EC2      │
    └───────────┬─────────────┘
                │
    ┌───────────▼─────────────┐
    │       Data Layer        │
    │ Amazon RDS (Postgres)   │
    └─────────────────────────┘

---

## Technologies Used

- **AWS CDK** (Python)  
- **Amazon S3** + CloudFront  
- **AWS Lambda** (with unit tests)  
- **Amazon EC2 Auto Scaling** + ALB  
- **Amazon RDS** (optional)  
- **Amazon VPC** (public/private subnets)  
- **GitHub Actions** for CI/CD  

---

## Prerequisites

- AWS Account & CLI configured  
- Python 3.10+ (tested with 3.13)  
- AWS CDK CLI installed  
- Node.js 18+ (for CDK)  
- GitHub Actions secrets for `AWS_ACCOUNT_ID` & optional `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`  

---

## Setup & Deployment

Follow these steps to run locally, test, and optionally deploy:

1. **Clone the repository**
```bash
git clone https://github.com/<your-username>/aws-3tier-cdk.git
cd aws-3tier-cdk

2. **Create and activate a virtual environment**
python3 -m venv .venv
source .venv/bin/activate

3. **Install dependencies**
pip install -r requirements.txt
pip install -r lambda_layers/image_dependencies/python/lib/python3.13/site-packages

4. **Run unit tests (including mocked Lambda/S3)**
pytest -v tests/

5. **Bootstrap CDK environment**
cdk bootstrap aws://<ACCOUNT_ID>/<REGION>

6. **Synthesize & Diff**
cdk synth
cdk diff

7. **Optional: Deploy to sandbox**
cdk deploy --require-approval never

8. **Optional: Destroy stack after testing**
cdk destroy --force
