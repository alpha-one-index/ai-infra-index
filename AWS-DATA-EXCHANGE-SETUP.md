# AWS Data Exchange Setup Guide — ai-infra-index

This guide covers setting up the automated S3 upload and AWS Data Exchange (ADX) pipeline for hourly GPU cloud pricing data.

## Overview

The `update-pricing.yml` workflow now includes steps to:
1. Upload `cloud-pricing.json` to S3 every hour
2. Create a new ADX revision with the latest GPU pricing data
3. Auto-finalize the revision so subscribers get updates automatically

The AWS steps are **gated by secrets** — they only run when `ADX_DATASET_ID` is configured.

## Step 1: Create S3 Bucket

```bash
aws s3 mb s3://ai-infra-index-data --region us-east-1
aws s3api put-bucket-versioning \
  --bucket ai-infra-index-data \
  --versioning-configuration Status=Enabled
```

## Step 2: Create IAM User

Minimal permissions policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
      "Resource": ["arn:aws:s3:::ai-infra-index-data", "arn:aws:s3:::ai-infra-index-data/*"]
    },
    {
      "Effect": "Allow",
      "Action": ["dataexchange:CreateRevision", "dataexchange:CreateJob", "dataexchange:StartJob", "dataexchange:GetJob", "dataexchange:UpdateRevision"],
      "Resource": "*"
    }
  ]
}
```

## Step 3: Create ADX Dataset

1. Go to [AWS Data Exchange Console](https://console.aws.amazon.com/dataexchange/)
2. Create data set:
   - **Name**: AI Infrastructure GPU Cloud Pricing Index
   - **Description**: Hourly-updated GPU cloud pricing data across 20+ providers including AWS, GCP, Azure, Lambda Labs, CoreWeave, and more.
3. Note the **Dataset ID**

## Step 4: Add GitHub Secrets

Repo Settings > Secrets > Actions:

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key |
| `AWS_SECRET_ACCESS_KEY` | IAM user secret key |
| `ADX_DATASET_ID` | Dataset ID from Step 3 |

## S3 Structure

```
s3://ai-infra-index-data/
  gpu-pricing/
    latest/
      cloud-pricing.json
    snapshots/
      2026-03-08T06:00-cloud-pricing.json
      2026-03-08T07:00-cloud-pricing.json
      ...
    history/
      (synced from data/history/)
```

## Cost Estimate

- S3: ~$0.05/month (hourly snapshots, small JSON)
- ADX provider: Free
- GitHub Actions: ~720 runs/month (within free tier for public repos)
