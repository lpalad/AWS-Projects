# GitHub to S3 Automated Deployment

## Project Overview
Automate website deployment using GitHub Actions to sync files with an AWS S3 bucket.

## Architecture
- GitHub Repository (Source)
- GitHub Actions (Automation)
- AWS S3 Bucket (Destination)
- Apache Reverse Proxy (Front-end)

## Implementation Steps
1. Create IAM User and Policy
2. Configure GitHub Repository
3. Set up GitHub Actions Secrets
4. Create Workflow File
5. Test Deployment

## Files
- `cli-commands.md` - AWS CLI commands used
- `workflow-files/s3-sync.yml` - GitHub Actions workflow configuration

## Security Considerations
- Use IAM roles with minimum required permissions
- Store AWS credentials in GitHub Secrets
- Never commit sensitive information
- Regular credential rotation

## Testing
- Push changes to trigger workflow
- Monitor GitHub Actions
- Verify S3 bucket updates

## Author
- Created: February 2025
- Author: Leonard Palad
- Blog site: https://aws.leonardspalad.com/
- LinkedIn: https://www.linkedin.com/in/leonardspalad/
