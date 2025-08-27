All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-08-15
### Added
- Initial AWS CDK project scaffold (Python)
- Three-tier architecture structure defined in CDK app (`app.py` and stack file)
- `README.md` with architecture diagram, setup instructions, and deployment flow
- `.github/workflows/cdk-synth.yml` to run `cdk synth` on every push for CI validation
- Created `CHANGELOG.md` for tracking updates

### Notes
- No application logic or deployed AWS resources yet
- Next steps: add VPC, subnets, Security Groups

## [1.0.0] - 2025-08-22
### Added
- 3-tier CDK stack (`aws_3tier_cdk_stack.py`) with optional RDS, S3, and Lambda integration
- Lambda function `image_processor.py` with **mocked unit tests** for S3 access
- GitHub Actions workflow (`ci-cd.yml`) for:
  - Running unit tests
  - `cdk synth` and `cdk diff` validation
- Updated `README.md` to include architecture, setup instructions, and CI/CD flow

### Changed
- Refined folder structure for modularity
- Updated Python dependencies for Lambda layers

### Planned / Next Milestones
- Deploy VPC, subnets, and Security Groups in CDK
- Integrate fully functional RDS, S3, and other services
- Enhance CI/CD pipeline to include **sandbox deployment and teardown**
- Modularize stack files for better maintainability
