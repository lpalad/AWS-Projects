# AWS CLI Commands for GitHub-S3 CI/CD Setup

Create IAM user for GitHub Actions:
aws iam create-user --user-name github-actions-s3-user

Create policy file contents:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name/*",
                "arn:aws:s3:::your-bucket-name"
            ]
        }
    ]
}

Create IAM policy:
aws iam create-policy --policy-name github-s3-sync-policy --description "Policy for GitHub Actions to sync with S3 bucket" --policy-document file://github-s3-policy.json

Attach policy to user:
aws iam attach-user-policy --user-name github-actions-s3-user --policy-arn arn:aws:iam:::policy/github-s3-sync-policy

Verify S3 bucket contents:
aws s3 ls s3://your-bucket-name

Test sync command:
aws s3 sync . s3://your-bucket-name --exclude ".git/*" --exclude ".github/*"

Security Notes:
- Replace placeholder AWS account ID
- Replace your-bucket-name with actual bucket name
- Never commit AWS credentials
- Store credentials in GitHub Secrets:
  - AWS_ACCESS_KEY_ID
  - AWS_SECRET_ACCESS_KEY

Verification Steps:
- Verify IAM user creation
- Check policy attachment
- Test S3 bucket access
- Confirm GitHub Actions permissions

Author  
Created: February 2025  
Author: Leonard Palad  
Blog site: https://aws.leonardspalad.com/  
LinkedIn: https://www.linkedin.com/in/leonardspalad/
