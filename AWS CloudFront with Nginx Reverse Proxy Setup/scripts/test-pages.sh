#!/usr/bin/env bash
# test-pages.sh
# Simple script to test multiple endpoints on CloudFront or your reverse proxy.

CLOUDFRONT_DOMAIN="d1234example.cloudfront.net"

PAGES=(
  "index.html"
  "about.html"
  "contact.html"
)

echo "Testing CloudFront distribution: $CLOUDFRONT_DOMAIN"
for page in "${PAGES[@]}"; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$CLOUDFRONT_DOMAIN/$page")
  if [[ "$STATUS" == "200" ]]; then
    echo "✅ $page => 200 OK"
  else
    echo "❌ $page => $STATUS"
  fi
done

