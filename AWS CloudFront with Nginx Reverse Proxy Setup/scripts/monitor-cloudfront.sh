#!/usr/bin/env bash
# monitor-cloudfront.sh
# Retrieves recent CloudFront metrics (requests, 4xx, 5xx) from CloudWatch.

DISTRIBUTION_ID="EXAMPLE123456"
START_TIME=$(date -u -d '15 minutes ago' +%Y-%m-%dT%H:%M:%SZ)
END_TIME=$(date -u +%Y-%m-%dT%H:%M:%SZ)

echo "CloudFront Metrics for $DISTRIBUTION_ID"
echo "Time Range: $START_TIME to $END_TIME"

# Requests
aws cloudwatch get-metric-statistics \
  --namespace AWS/CloudFront \
  --metric-name Requests \
  --dimensions Name=DistributionId,Value=$DISTRIBUTION_ID \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --period 300 \
  --statistics Sum

# 4xx Error Rate
aws cloudwatch get-metric-statistics \
  --namespace AWS/CloudFront \
  --metric-name 4xxErrorRate \
  --dimensions Name=DistributionId,Value=$DISTRIBUTION_ID \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --period 300 \
  --statistics Average

# 5xx Error Rate
aws cloudwatch get-metric-statistics \
  --namespace AWS/CloudFront \
  --metric-name 5xxErrorRate \
  --dimensions Name=DistributionId,Value=$DISTRIBUTION_ID \
  --start-time "$START_TIME" \
  --end-time "$END_TIME" \
  --period 300 \
  --statistics Average

